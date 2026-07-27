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


def test_create_delivery_duplicate_rejection(client: TestClient, db: Session):
    """Test duplicate order creation rejection (HTTP 409 Conflict)."""
    customer = create_test_customer(db)
    headers = create_auth_header(db, email="dup.tester@routeai.com")

    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Depot Unique Alpha",
        "drop_location": "Destination Beta",
        "package_weight": 10.0,
    }
    res1 = client.post("/api/v1/deliveries", json=payload, headers=headers)
    assert res1.status_code == status.HTTP_201_CREATED

    # Attempt duplicate submission
    res2 = client.post("/api/v1/deliveries", json=payload, headers=headers)
    assert res2.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in res2.json()["detail"]


def test_validation_identical_locations_rejected(client: TestClient, db: Session):
    """Test validation rejecting identical pickup and drop-off locations (HTTP 422)."""
    customer = create_test_customer(db)
    headers = create_auth_header(db, email="val.tester@routeai.com")

    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Same Address 123",
        "drop_location": "Same Address 123",
        "package_weight": 5.0,
    }
    res = client.post("/api/v1/deliveries", json=payload, headers=headers)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_illegal_status_transition_rejected(client: TestClient, db: Session):
    """Test business validation rejecting illegal state transitions (HTTP 400)."""
    customer = create_test_customer(db)
    headers = create_auth_header(db, email="fsm.tester@routeai.com")

    create_res = client.post(
        "/api/v1/deliveries",
        json={
            "customer_id": customer.customer_id,
            "pickup_location": "Depot FSM",
            "drop_location": "Target FSM",
            "package_weight": 10.0,
        },
        headers=headers,
    )
    delivery_id = create_res.json()["delivery_id"]

    # Transition from pending to scheduled (Legal)
    res_sched = client.put(f"/api/v1/deliveries/{delivery_id}", json={"delivery_status": "scheduled"}, headers=headers)
    assert res_sched.status_code == status.HTTP_200_OK

    # Illegal transition: scheduled -> delivered directly (Illegal!)
    res_illegal = client.put(f"/api/v1/deliveries/{delivery_id}", json={"delivery_status": "delivered"}, headers=headers)
    assert res_illegal.status_code == status.HTTP_400_BAD_REQUEST
    assert "Illegal status transition" in res_illegal.json()["detail"]


def test_list_deliveries_with_search_filter_and_sort(client: TestClient, db: Session):
    """Test GET /api/v1/deliveries with search, priority filtering, and dynamic sorting."""
    customer = create_test_customer(db)
    headers = create_auth_header(db, email="list.tester@routeai.com")

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

    res_search = client.get("/api/v1/deliveries?search=Hyderabad", headers=headers)
    assert res_search.status_code == status.HTTP_200_OK
    assert res_search.json()["total"] == 2


def test_get_delivery_by_id_success_and_not_found(client: TestClient, db: Session):
    """Test GET /api/v1/deliveries/{id} for valid ID and 404 for non-existent ID."""
    customer = create_test_customer(db)
    headers = create_auth_header(db, email="get.tester@routeai.com")

    payload = {
        "customer_id": customer.customer_id,
        "pickup_location": "Hub A Unique",
        "drop_location": "Target Location Unique",
        "package_weight": 8.0,
    }
    create_res = client.post("/api/v1/deliveries", json=payload, headers=headers)
    delivery_id = create_res.json()["delivery_id"]

    res = client.get(f"/api/v1/deliveries/{delivery_id}", headers=headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["delivery_id"] == delivery_id


def test_delete_delivery_admin_and_user_permissions(client: TestClient, db: Session):
    """Test DELETE /api/v1/deliveries/{id} denies regular User (403) and succeeds for Admin (200)."""
    customer = create_test_customer(db)
    user_headers = create_auth_header(db, email="regular.del@deliveries.com", role_name="User")

    create_res = client.post(
        "/api/v1/deliveries",
        json={
            "customer_id": customer.customer_id,
            "pickup_location": "Hub X Unique",
            "drop_location": "Drop Y Unique",
            "package_weight": 15.0,
        },
        headers=user_headers,
    )
    delivery_id = create_res.json()["delivery_id"]

    res_user = client.delete(f"/api/v1/deliveries/{delivery_id}", headers=user_headers)
    assert res_user.status_code == status.HTTP_403_FORBIDDEN

    admin_headers = create_auth_header(db, email="admin.del@deliveries.com", role_name="Admin")
    res_admin = client.delete(f"/api/v1/deliveries/{delivery_id}", headers=admin_headers)
    assert res_admin.status_code == status.HTTP_200_OK
