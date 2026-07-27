"""Delivery Management API automated unit and integration tests."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.role import Role
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.security.jwt import create_access_token
from app.security.password import hash_password


def create_test_customer(db: Session) -> Customer:
    """Helper to seed a test Customer in the database."""
    customer = Customer(
        company_name="Acme Logistics Corp",
        contact_name="Alice Smith",
        phone="+15550199",
        email="alice@acme.com",
        address="100 Industrial Parkway, City Center",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def create_auth_header(db: Session, email: str = "dispatcher@routeai.com", role_name: str = "User") -> dict[str, str]:
    """Helper to seed a user and return Bearer token authorization header."""
    role = user_repository.get_role_by_name(db, role_name)
    if not role:
        role = user_repository.create_role(db, role_name)

    user = user_repository.get_by_email(db, email)
    if not user:
        user = user_repository.create_user(
            db,
            email=email,
            password_hash=hash_password("SecurePass123!"),
            full_name="Test User",
            role_id=role.role_id,
        )

    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": role.role_name})
    return {"Authorization": f"Bearer {token}"}


def test_create_delivery_success(client: TestClient, db: Session):
    """Test POST /api/v1/deliveries creates a new delivery order."""
    customer = create_test_customer(db)
    headers = create_auth_header(db)

    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Depot A - Central Logistics Hub",
        "drop_location": "742 Evergreen Terrace, Springfield",
        "package_weight": 12.5,
        "priority": "high",
    }
    response = client.post("/api/v1/deliveries", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_id"] == customer.customer_id
    assert data["pickup_location"] == payload["pickup_location"]
    assert data["drop_location"] == payload["drop_location"]
    assert data["package_weight"] == 12.5
    assert data["priority"] == "high"
    assert data["delivery_status"] == "pending"
    assert "delivery_id" in data


def test_create_delivery_unauthorized(client: TestClient, db: Session):
    """Test POST /api/v1/deliveries fails without Bearer token."""
    customer = create_test_customer(db)
    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Depot A",
        "drop_location": "123 Main St",
        "package_weight": 5.0,
    }
    response = client.post("/api/v1/deliveries", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_deliveries_with_search_filter_and_sort(client: TestClient, db: Session):
    """Test GET /api/v1/deliveries with search, priority filtering, and dynamic sorting."""
    customer = create_test_customer(db)
    headers = create_auth_header(db)

    # Seed three deliveries
    p1 = {
        "customer_id": customer.customer_id,
        "pickup_location": "Hyderabad Central Depot",
        "drop_location": "Gachibowli Tech Park, Hyderabad",
        "package_weight": 5.0,
        "priority": "urgent",
    }
    p2 = {
        "customer_id": customer.customer_id,
        "pickup_location": "Bengaluru Warehouse",
        "drop_location": "Whitefield Hub, Bengaluru",
        "package_weight": 25.0,
        "priority": "normal",
    }
    p3 = {
        "customer_id": customer.customer_id,
        "pickup_location": "Hyderabad Outer Ring Road Depot",
        "drop_location": "Hitec City, Hyderabad",
        "package_weight": 15.0,
        "priority": "urgent",
    }
    client.post("/api/v1/deliveries", json=p1, headers=headers)
    client.post("/api/v1/deliveries", json=p2, headers=headers)
    client.post("/api/v1/deliveries", json=p3, headers=headers)

    # 1. Test Search for "Hyderabad"
    res_search = client.get("/api/v1/deliveries?search=Hyderabad", headers=headers)
    assert res_search.status_code == status.HTTP_200_OK
    assert res_search.json()["total"] == 2

    # 2. Test Priority Filter "urgent"
    res_priority = client.get("/api/v1/deliveries?priority=urgent", headers=headers)
    assert res_priority.status_code == status.HTTP_200_OK
    assert res_priority.json()["total"] == 2

    # 3. Test Sorting by package_weight asc
    res_sort = client.get("/api/v1/deliveries?sort=package_weight&order=asc", headers=headers)
    assert res_sort.status_code == status.HTTP_200_OK
    items = res_sort.json()["items"]
    weights = [item["package_weight"] for item in items]
    assert weights == sorted(weights)


def test_get_delivery_by_id_success_and_not_found(client: TestClient, db: Session):
    """Test GET /api/v1/deliveries/{id} for valid ID and 404 for non-existent ID."""
    customer = create_test_customer(db)
    headers = create_auth_header(db)

    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Hub A",
        "drop_location": "Target Location",
        "package_weight": 8.0,
    }
    create_res = client.post("/api/v1/deliveries", json=payload, headers=headers)
    delivery_id = create_res.json()["delivery_id"]

    # Fetch valid delivery
    res = client.get(f"/api/v1/deliveries/{delivery_id}", headers=headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["delivery_id"] == delivery_id

    # Fetch non-existent delivery
    res_404 = client.get("/api/v1/deliveries/99999", headers=headers)
    assert res_404.status_code == status.HTTP_404_NOT_FOUND


def test_update_delivery_success(client: TestClient, db: Session):
    """Test PUT /api/v1/deliveries/{id} updates attributes and delivery status."""
    customer = create_test_customer(db)
    headers = create_auth_header(db)

    create_res = client.post(
        "/api/v1/deliveries",
        json={
            "customer_id": customer.customer_id,
            "pickup_location": "Old Hub",
            "drop_location": "Old Address",
            "package_weight": 5.0,
        },
        headers=headers,
    )
    delivery_id = create_res.json()["delivery_id"]

    update_payload = {
        "drop_location": "New Updated Address",
        "delivery_status": "in_transit",
    }
    update_res = client.put(f"/api/v1/deliveries/{delivery_id}", json=update_payload, headers=headers)

    assert update_res.status_code == status.HTTP_200_OK
    data = update_res.json()
    assert data["drop_location"] == "New Updated Address"
    assert data["delivery_status"] == "in_transit"


def test_delete_delivery_admin_and_user_permissions(client: TestClient, db: Session):
    """Test DELETE /api/v1/deliveries/{id} denies regular User (403) and succeeds for Admin (200)."""
    customer = create_test_customer(db)

    # Headers for Regular User
    user_headers = create_auth_header(db, email="regular.user@deliveries.com", role_name="User")

    create_res = client.post(
        "/api/v1/deliveries",
        json={
            "customer_id": customer.customer_id,
            "pickup_location": "Hub X",
            "drop_location": "Drop Y",
            "package_weight": 15.0,
        },
        headers=user_headers,
    )
    delivery_id = create_res.json()["delivery_id"]

    # Regular user attempt -> 403 Forbidden
    res_user = client.delete(f"/api/v1/deliveries/{delivery_id}", headers=user_headers)
    assert res_user.status_code == status.HTTP_403_FORBIDDEN

    # Headers for Admin User
    admin_headers = create_auth_header(db, email="admin@deliveries.com", role_name="Admin")

    # Admin user attempt -> 200 OK
    res_admin = client.delete(f"/api/v1/deliveries/{delivery_id}", headers=admin_headers)
    assert res_admin.status_code == status.HTTP_200_OK

    # Confirm deletion (404 Not Found)
    res_confirm = client.get(f"/api/v1/deliveries/{delivery_id}", headers=admin_headers)
    assert res_confirm.status_code == status.HTTP_404_NOT_FOUND
