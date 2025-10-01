import boto3
import json
from config.settings import Settings
from templates.prompts import Prompts
import logging

logger = logging.getLogger(__name__)

# inicializamos la conexión con Q service tomando las credenciales y definiendo el modelo
class AmazonQService:
    ## establecemos todas las definiciones disponibles
    def __init__(self):
        self.settings = Settings()
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.settings.AWS_DEFAULT_REGION
        )
        self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
    
    def generate_content(self, topic: str, audience: str, duration: int, event_type: str) -> str:
        """
        Generamos el contenido para la charla usando Amazon Bedrock con Claude 3.
        """
        try:
            prompt = Prompts.get_prompt_by_type(
                "technical",
                topic=topic,
                audience=audience,
                duration=duration,
                event_type=event_type
            )

            # Preparamos el promt que le pasaremos a Claude
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            # Llamar a Bedrock con Claude 3
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": messages,
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "top_p": 0.9
                })
            )

            # Procesamos la respuesta
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body:
                return response_body['content'][0]['text']
            else:
                logger.error(f"Unexpected response format: {response_body}")
                raise Exception("Formato de respuesta inesperado")

        except Exception as e:
            logger.error(f"Error generating content with Bedrock: {str(e)}")
            raise Exception(f"Error generating content: {str(e)}")

    def test_connection(self) -> bool:
        """
        Prueba la conexión con Bedrock y el acceso al modelo.
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": "Hello, this is a test."
                }
            ]
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": messages,
                    "max_tokens": 50,
                    "temperature": 0.7
                })
            )
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False