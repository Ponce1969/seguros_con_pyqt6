import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def test_crear_corredor():
    """Prueba la creación de un corredor"""
    corredor_data = {
        "numero": 1271,
        "nombres": "FERNANDO",
        "apellidos": "BERVEJILLO",
        "documento": "212702370017",
        "direccion": "AV. BOLIVIA 1863",
        "localidad": "MONTEVIDEO",
        "telefonos": "26838859",
        "movil": "098435838",
        "mail": "fberve@gmail.com",
        "observaciones": "fberve@adinet.com.uy\n094435838"
    }
    
    # Crear corredor
    response = requests.post(f"{BASE_URL}/corredores/", json=corredor_data)
    print("\nCreando corredor:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.status_code < 300 else response.text}")

def test_listar_corredores():
    """Prueba listar todos los corredores"""
    response = requests.get(f"{BASE_URL}/corredores/")
    print("\nListando corredores:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_obtener_corredor():
    """Prueba obtener un corredor específico"""
    numero = 1271
    response = requests.get(f"{BASE_URL}/corredores/{numero}")
    print(f"\nObteniendo corredor {numero}:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.status_code < 300 else response.text}")

def test_actualizar_corredor():
    """Prueba actualizar un corredor"""
    numero = 1271
    update_data = {
        "telefonos": "26838860",
        "movil": "098435839"
    }
    response = requests.put(f"{BASE_URL}/corredores/{numero}", json=update_data)
    print("\nActualizando corredor:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.status_code < 300 else response.text}")

if __name__ == "__main__":
    print("Iniciando pruebas de endpoints de corredores...")
    test_crear_corredor()
    test_listar_corredores()
    test_obtener_corredor()
    test_actualizar_corredor()
    print("\nPruebas completadas.")
