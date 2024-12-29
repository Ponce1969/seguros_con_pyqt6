import requests
import json

def test_tipos_seguros():
    print("\nIniciando pruebas de endpoints de tipos de seguros...")
    
    # URL base
    base_url = "http://localhost:8000/tipos-seguros"
    
    # Datos de prueba
    tipo_seguro_data = {
        "id_tipo": 100,
        "aseguradora": "SURA",
        "codigo": "C",
        "descripcion": "HURTO E INCENDIO COMERCIALES"
    }
    
    # Crear tipo de seguro
    print("\nCreando tipo de seguro:")
    response = requests.post(base_url + "/", json=tipo_seguro_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Listar tipos de seguros
    print("\nListando tipos de seguros:")
    response = requests.get(base_url + "/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Obtener tipo de seguro específico
    print(f"\nObteniendo tipo de seguro {tipo_seguro_data['id_tipo']}:")
    response = requests.get(f"{base_url}/{tipo_seguro_data['id_tipo']}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Actualizar tipo de seguro
    print("\nActualizando tipo de seguro:")
    update_data = {
        "descripcion": "HURTO E INCENDIO COMERCIALES ACTUALIZADO"
    }
    response = requests.put(f"{base_url}/{tipo_seguro_data['id_tipo']}", json=update_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nPruebas completadas.")
