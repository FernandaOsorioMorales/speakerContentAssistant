import re
from datetime import datetime
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class TalkHelper:
    @staticmethod
    def sanitize_title(title: str) -> str:
        """Limpia y formatea el título para usarlo en nombres de archivo."""
        return re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower().replace(' ', '_')

    @staticmethod
    def format_duration(minutes: int) -> str:
        """Formatea la duración en un formato legible."""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}min"
        return f"{mins}min"

    @staticmethod
    def get_current_datetime() -> str:
        """Retorna la fecha y hora actual en formato ISO."""
        return datetime.now().isoformat()

    @staticmethod
    def create_talk_sections(duration: int) -> List[Dict[str, int]]:
        """Genera una sugerencia de distribución de tiempo para la charla."""
        total_minutes = duration
        sections = {
            "Introducción": 0.1,
            "Contenido principal": 0.6,
            "Ejemplos/Demos": 0.2,
            "Q&A": 0.1
        }
        
        return [{k: round(v * total_minutes)} for k, v in sections.items()]

class ValidationHelper:
    @staticmethod
    def validate_talk_input(topic: str, duration: int) -> Tuple[bool, str]:
        """Valida los datos de entrada de la charla."""
        if not topic:
            return False, "El tema de la charla es obligatorio"
        if len(topic) < 5:
            return False, "El tema debe tener al menos 5 caracteres"
        if duration < 5:
            return False, "La duración mínima es de 5 minutos"
        if duration > 180:
            return False, "La duración máxima es de 180 minutos"
        return True, ""

    @staticmethod
    def validate_aws_credentials(settings) -> Tuple[bool, str]:
        """Valida las credenciales de AWS."""
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_DEFAULT_REGION
        ]):
            return False, "Faltan credenciales de AWS"
        return True, ""