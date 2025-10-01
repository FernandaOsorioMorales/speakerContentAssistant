import streamlit as st
from services.amazon_q import AmazonQService
from services.content_manager import ContentManager
from utils.helpers import TalkHelper, ValidationHelper
from config.settings import Settings
import logging

# configuramos la página
st.set_page_config(
    page_title="Speaker Content Assistant",
    page_icon="🎤",
    layout="wide"
)

# generamos estilos personalizados
st.markdown("""
    <style>
    .stHeader {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .talk-info {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .content-section {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Configuramos el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_session_state():
    """Inicializa el estado de la sesión"""
    if 'talks' not in st.session_state:
        st.session_state.talks = []
    if 'current_talk' not in st.session_state:
        st.session_state.current_talk = None
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None

def process_talk_content(content: str) -> str:
    """
    Procesa el contenido de la charla para mostrar solo las secciones deseadas.
    """
    sections = {
        "estructura": "ESTRUCTURA DETALLADA",
        "recursos": "RECURSOS Y MATERIALES",
        "tips": "TIPS DE PRESENTACIÓN"
    }
    
    processed_content = []
    current_section = None
    
    for line in content.split('\n'):
        for section_key, section_header in sections.items():
            if section_header in line:
                current_section = section_key
                processed_content.append(f"\n## {line.strip()}")
                break
        else:
            if current_section:
                processed_content.append(line)
    
    return '\n'.join(processed_content)

def main():
    init_session_state()
    
    settings = Settings()
    q_service = AmazonQService()
    content_manager = ContentManager()
    talk_helper = TalkHelper()

    st.title("🎤 Speaker Content Assistant")
    
    # mostramos un sidebar con las charlas que se han generado antes
    with st.sidebar:
        st.header("Charlas guardadas")
        talks = content_manager.load_talks()
        for talk in talks:
            with st.expander(f"{talk['topic']} - {talk['date']}"):
                st.write(f"Audiencia: {talk['audience']}")
                st.write(f"Duración: {talk_helper.format_duration(talk['duration'])}")
                if st.button("Cargar", key=f"load_{talk['date']}"):
                    st.session_state.current_talk = talk

    # Formulario de los inputs para generar la charla
    with st.form("talk_details"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Tema de la charla")
            audience = st.selectbox(
                "Audiencia",
                settings.AUDIENCE_TYPES
            )

        with col2:
            duration = st.number_input(
                "Duración (minutos)", 
                min_value=5, 
                max_value=180, 
                value=30
            )
            event_type = st.selectbox(
                "Tipo de evento",
                settings.EVENT_TYPES
            )

        submitted = st.form_submit_button("Generar contenido")

    # Si todo salió bien, comenzamos con la generación de contenido
    if submitted:
        is_valid, error_message = ValidationHelper.validate_talk_input(topic, duration)
        if not is_valid:
            st.error(error_message)
        else:
            with st.spinner("Generando contenido..."):
                try:
                    content = q_service.generate_content(
                        topic=topic,
                        audience=audience,
                        duration=duration,
                        event_type=event_type
                    )
                    
                    if content:
                        st.success("¡Contenido generado!")
                        
                        # Guardar charla
                        talk_data = {
                            "topic": topic,
                            "content": content,
                            "audience": audience,
                            "duration": duration,
                            "event_type": event_type,
                            "date": talk_helper.get_current_datetime()
                        }
                        
                        content_manager.save_talk(talk_data)
                        st.session_state.current_talk = talk_data
                        st.session_state.generated_content = content
                        
                except Exception as e:
                    logger.error(f"Error generating content: {str(e)}")
                    st.error("Hubo un error generando el contenido. Por favor, intenta de nuevo.")

    # Mostramos el contenido generado
    if st.session_state.current_talk:
        st.header("Charla actual")
        
        # Mostramos la información en columnas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Tema:**", st.session_state.current_talk['topic'])
        with col2:
            st.write("**Audiencia:**", st.session_state.current_talk['audience'])
        with col3:
            st.write("**Duración:**", talk_helper.format_duration(st.session_state.current_talk['duration']))
        
        st.markdown("---")
        
        # Procedemos a mostrar el output del promt generado
        if 'content' in st.session_state.current_talk:
            content = st.session_state.current_talk['content']
            processed_content = process_talk_content(content)
            st.markdown(processed_content)

    # permitimos limpiar el contenido o descargar como txr
    if st.session_state.generated_content:
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Descargar como TXT",
                st.session_state.generated_content,
                file_name=f"charla_{talk_helper.sanitize_title(topic)}.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("Limpiar contenido"):
                st.session_state.generated_content = None
                st.rerun()

if __name__ == "__main__":
    main()