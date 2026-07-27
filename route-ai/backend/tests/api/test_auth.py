"""Authentication and security automated tests."""

from fastapi import Depends, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.role import Role
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import RegisterRequest
from app.security.dependencies import require_role
from app.security.jwt import create_access_token, decode_access_token, verify_access_token
from app.security.password import hash_password, verify_password
from app.services.auth_service import auth_service


# Dummy protected route to test role-based authorization
@app.get("/api/v1/admin-only-test", tags=["Testing"])
def admin_only_endpoint(current_user: User = Depends(require_role("Admin"))):
    return {"message": f"Welcome Admin {current_user.full_name}"}


def test_password_hashing_and_verification():
    """Test password hashing and verification helper functions."""
    raw_password = "SuperSecretPassword123!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_generation_and_decoding():
    """Test JWT access token creation, verification, and payload decoding."""
    payload = {"sub": "42", "email": "test@routeai.com", "role": "User"}
    token = create_access_token(payload)

    assert isinstance(token, str)
    assert len(token) > 20

    decoded = decode_access_token(token)
    assert decoded["sub"] == "42"
    assert decoded["email"] == "test@routeai.com"
    assert decoded["role"] == "User"

    verified = verify_access_token(token)
    assert verified is not None
    assert verified["sub"] == "42"


def test_register_user_success(client: TestClient):
    """Test successful user registration endpoint POST /api/v1/auth/register."""
    payload = {
        "email": "john.doe@example.com",
        "password": "Password123!",
        "full_name": "John Doe",
        "phone": "+1234567890",
    }
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["phone"] == payload["phone"]
    assert data["is_active"] is True
    assert data["role_name"] == "User"
    assert "user_id" in data


def test_register_duplicate_email(client: TestClient):
    """Test duplicate email registration rejection."""
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
        "full_name": "Duplicate User",
    }
    response1 = client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response2.json()["detail"]


def test_login_success(client: TestClient):
    """Test successful user login POST /api/v1/auth/login."""
    register_payload = {
        "email": "login.user@example.com",
        "password": "SecurePassword123",
        "full_name": "Login User",
    }
    client.post("/api/v1/auth/register", json=register_payload)

    login_payload = {
        "email": "login.user@example.com",
        "password": "SecurePassword123",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == register_payload["email"]


def test_login_invalid_credentials(client: TestClient):
    """Test login with incorrect password and non-existent user email."""
    register_payload = {
        "email": "valid.user@example.com",
        "password": "CorrectPassword",
        "full_name": "Valid User",
    }
    client.post("/api/v1/auth/register", json=register_payload)

    # Wrong password
    response1 = client.post(
        "/api/v1/auth/login",
        json={"email": "valid.user@example.com", "password": "WrongPassword"},
    )
    assert response1.status_code == status.HTTP_401_UNAUTHORIZED

    # Non-existent email
    response2 = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "CorrectPassword"},
    )
    assert response2.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_me_protected_endpoint(client: TestClient):
    """Test GET /api/v1/auth/me with valid Bearer token."""
    register_payload = {
        "email": "me.user@example.com",
        "password": "Password123!",
        "full_name": "Me User",
    }
    client.post("/api/v1/auth/register", json=register_payload)

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "me.user@example.com", "password": "Password123!"},
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == register_payload["email"]
    assert data["full_name"] == register_payload["full_name"]


def test_unauthorized_requests(client: TestClient):
    """Test endpoints with missing or invalid Authorization token."""
    # No token provided
    response1 = client.get("/api/v1/auth/me")
    assert response1.status_code == status.HTTP_401_UNAUTHORIZED

    # Invalid token provided
    headers = {"Authorization": "Bearer invalid_token_string_xyz"}
    response2 = client.get("/api/v1/auth/me", headers=headers)
    assert response2.status_code == status.HTTP_401_UNAUTHORIZED


def test_role_based_authorization(client: TestClient, db: Session):
    """Test role-based access control (RBAC) permission checking."""
    # Create normal user
    register_payload = {
        "email": "regular.user@example.com",
        "password": "UserPass123",
        "full_name": "Regular User",
    }
    client.post("/api/v1/auth/register", json=register_payload)

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "regular.user@example.com", "password": "UserPass123"},
    )
    user_token = login_res.json()["access_token"]

    # Regular user attempting admin endpoint should receive 403 Forbidden
    res_user = client.get(
        "/api/v1/admin-only-test",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res_user.status_code == status.HTTP_403_FORBIDDEN

    # Create Admin role and user
    admin_role = user_repository.get_role_by_name(db, "Admin")
    if not admin_role:
        admin_role = user_repository.create_role(db, "Admin")

    admin_user = user_repository.create_user(
        db,
        email="admin@example.com",
        password_hash=hash_password("AdminPass123"),
        full_name="Admin User",
        role_id=admin_role.role_id,
    )

    admin_login = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "AdminPass123"},
    )
    admin_token = admin_login.json()["access_token"]

    # Admin user accessing admin endpoint should succeed
    res_admin = client.get(
        "/api/v1/admin-only-test",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res_admin.status_code == status.HTTP_200_OK
    assert "Welcome Admin Admin User" in res_admin.json()["message"]
