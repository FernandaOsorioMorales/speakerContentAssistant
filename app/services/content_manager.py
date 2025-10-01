import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

class ContentManager:
    def __init__(self):
        self.settings = Settings()
        self.ensure_data_file()

    def ensure_data_file(self):
        """Asegura que el archivo de datos existe."""
        if not self.settings.TALKS_FILE.exists():
            self.settings.TALKS_FILE.write_text("[]")

    def load_talks(self) -> List[Dict[str, Any]]:
        """Carga todas las charlas guardadas."""
        try:
            with open(self.settings.TALKS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading talks: {str(e)}")
            return []

    def save_talk(self, talk_data: Dict[str, Any]) -> bool:
        """Guarda una nueva charla."""
        try:
            talks = self.load_talks()
            
            # Agregar timestamp si no existe
            if 'date' not in talk_data:
                talk_data['date'] = datetime.now().isoformat()
            
            talks.append(talk_data)
            
            with open(self.settings.TALKS_FILE, 'w') as f:
                json.dump(talks, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Error saving talk: {str(e)}")
            return False

    def get_talk(self, talk_id: str) -> Dict[str, Any]:
        """Obtiene una charla específica por ID."""
        talks = self.load_talks()
        for talk in talks:
            if talk.get('id') == talk_id:
                return talk
        return None

    def update_talk(self, talk_id: str, updated_data: Dict[str, Any]) -> bool:
        """Actualiza una charla existente."""
        try:
            talks = self.load_talks()
            for i, talk in enumerate(talks):
                if talk.get('id') == talk_id:
                    talks[i].update(updated_data)
                    with open(self.settings.TALKS_FILE, 'w') as f:
                        json.dump(talks, f, indent=2)
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating talk: {str(e)}")
            return False

    def delete_talk(self, talk_id: str) -> bool:
        """Elimina una charla."""
        try:
            talks = self.load_talks()
            talks = [talk for talk in talks if talk.get('id') != talk_id]
            with open(self.settings.TALKS_FILE, 'w') as f:
                json.dump(talks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error deleting talk: {str(e)}")
            return False