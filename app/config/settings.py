from pathlib import Path
from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv()
        
     ## tomamos las credenciales de nuestro usuario en Consola
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        
    # seleccionamos el modelo que usaremos (debemos probar que tenemos acceso a él)
        self.BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
        self.MAX_TOKENS = 4096
        self.TEMPERATURE = 0.7
        
    # Especificamos donde se guardará la información generada
        self.DATA_DIR = Path("data")
        self.TALKS_FILE = self.DATA_DIR / "talks.json"
        
        self.DATA_DIR.mkdir(exist_ok=True)
        
    # Tipos de audiencia y eventos que podremos seleccionar
        self.AUDIENCE_TYPES = [
            "Desarrolladores",
            "Ejecutivos",
            "Estudiantes",
            "Público general",
            "Técnico avanzado"
        ]
       
        self.EVENT_TYPES = [
            "Conferencia técnica",
            "Meetup",
            "Webinar",
            "Workshop",
            "Keynote"
        ]