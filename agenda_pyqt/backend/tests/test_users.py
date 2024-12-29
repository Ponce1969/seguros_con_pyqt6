import requests
import json

def test_users():
    print("\nIniciando pruebas de endpoints de usuarios...")
    
    # URL base
    base_url = "http://localhost:8000/users"
    
    # Datos para crear un usuario administrador
    admin_data = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "admin123",
        "role": "admin"
    }
    
    # Crear usuario admin
    print("\nCreando usuario admin:")
    response = requests.post(f"{base_url}/", json=admin_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Login como admin
    print("\nLogin como admin:")
    login_data = {
        "username": admin_data["email"],
        "password": admin_data["password"]
    }
    response = requests.post(f"{base_url}/token", data=login_data)
    print(f"Status Code: {response.status_code}")
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear usuario normal
    user_data = {
        "name": "Normal User",
        "email": "user@example.com",
        "password": "user123",
        "role": "user"
    }
    
    print("\nCreando usuario normal:")
    response = requests.post(f"{base_url}/", json=user_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Listar usuarios
    print("\nListando usuarios:")
    response = requests.get(f"{base_url}/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nPruebas completadas.")
