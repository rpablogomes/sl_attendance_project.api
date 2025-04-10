from flask_jwt_extended import create_access_token
from src.models.employee import Employee


def test_register_success(client, db, new_employee):
    response = client.post("/api/v1/employee/register", json=new_employee)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Employee created successfully"
    assert data["email"] == new_employee["email"]

def test_register_existing_email(client, db, new_employee):
    # Create first user
    client.post("/api/v1/employee/register", json=new_employee)

    # Try registering again
    response = client.post("/api/v1/employee/register", json=new_employee)
    assert response.status_code == 400
    assert response.get_json()["message"] == "Email already exists"

def test_me_success(client, db, new_employee, app):
    # Register and create user
    response = client.post("/api/v1/employee/register", json=new_employee)
    employee = Employee.query.filter_by(email=new_employee["email"]).first()

    with app.app_context():
        token = create_access_token(identity=employee.id)

    # Get own profile
    response = client.get(
        "/api/v1/employee/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == new_employee["email"]

def test_me_unauthorized(client):
    response = client.get("/api/v1/employee/me")
    assert response.status_code == 401  # Not authorized
