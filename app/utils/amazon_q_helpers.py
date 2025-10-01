from typing import Dict, Any, Optional
import boto3
import json
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

class AmazonQHelper:
    def __init__(self):
        self.settings = Settings()
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.settings.AWS_DEFAULT_REGION
        )

    def format_request(self, prompt: str) -> Dict[str, Any]:
        """Formatea la solicitud para Amazon Bedrock."""
        return {
            "prompt": prompt,
            "max_tokens": self.settings.MAX_TOKENS,
            "temperature": self.settings.TEMPERATURE
        }

    def process_response(self, response: Dict[str, Any]) -> str:
        """Procesa la respuesta de Amazon Bedrock."""
        try:
            return response['completion']
        except KeyError as e:
            logger.error(f"Invalid response format: {e}")
            raise ValueError("Respuesta inválida de Amazon Bedrock")

    def validate_response(self, content: str) -> bool:
        """Valida que la respuesta tenga el contenido esperado."""
        required_sections = ["título", "objetivos", "estructura"]
        return all(section in content.lower() for section in required_sections)

    def clean_response(self, content: str) -> str:
        """Limpia y formatea la respuesta."""
        # Eliminar espacios extra y líneas vacías
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return '\n'.join(lines)