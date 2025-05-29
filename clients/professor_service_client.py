import requests

PROFESSORES_SERVICE_URL = "http://localhost:8000/api/professores"

class ProfessorServiceClient:
    @staticmethod
    def verificar_professor(id_professor):
        url = f"{PROFESSORES_SERVICE_URL}/api/professores{id_professor}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('professor', False) 
        except requests.RequestException as e:
            print(f"Erro ao acessar o professor_service: {e}")
            return False
