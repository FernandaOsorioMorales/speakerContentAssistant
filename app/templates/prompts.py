class Prompts:
    BASE_TALK_TEMPLATE = """
    Actúa como un experto asesor de speakers y crea una estructura detallada para una charla.
    
    INFORMACIÓN DE LA CHARLA:
    - Tema: {topic}
    - Audiencia: {audience}
    - Duración: {duration} minutos
    - Tipo de evento: {event_type}
    
    ESTRUCTURA REQUERIDA:
    
    1. TÍTULO Y DESCRIPCIÓN
    - Título atractivo y memorable
    - Subtítulo explicativo
    - Descripción corta (2-3 líneas)
    
    2. OBJETIVOS DE APRENDIZAJE
    - 3 objetivos específicos y medibles
    - Valor principal para la audiencia
    
    3. ESTRUCTURA DETALLADA
    [Distribuye el tiempo total de {duration} minutos]
    - Introducción y gancho inicial
    - Secciones principales con tiempos
    - Momentos de interacción
    - Conclusiones y llamada a la acción
    
    4. RECURSOS Y MATERIALES
    - Tipos de slides necesarios
    - Demos o ejemplos prácticos
    - Recursos adicionales recomendados
    
    5. TIPS DE PRESENTACIÓN
    - Consejos específicos para esta audiencia
    - Puntos de énfasis recomendados
    - Manejo de preguntas difíciles
    """

    TECHNICAL_TEMPLATE = BASE_TALK_TEMPLATE + """
    ELEMENTOS TÉCNICOS ADICIONALES:
    - Requisitos técnicos previos
    - Arquitectura o diagramas necesarios
    - Puntos de código importantes
    - Consideraciones de implementación
    """

    WORKSHOP_TEMPLATE = BASE_TALK_TEMPLATE + """
    ELEMENTOS DE WORKSHOP:
    - Ejercicios prácticos
    - Checkpoints de progreso
    - Soluciones guiadas
    - Materiales descargables
    """

    KEYNOTE_TEMPLATE = BASE_TALK_TEMPLATE + """
    ELEMENTOS DE KEYNOTE:
    - Historias inspiradoras
    - Datos y tendencias clave
    - Visión de futuro
    - Momentos memorables
    """

    @staticmethod
    def get_prompt_by_type(talk_type: str, **kwargs) -> str:
        """
        Retorna el prompt adecuado según el tipo de charla.
        """
        templates = {
            "technical": Prompts.TECHNICAL_TEMPLATE,
            "workshop": Prompts.WORKSHOP_TEMPLATE,
            "keynote": Prompts.KEYNOTE_TEMPLATE,
            "default": Prompts.BASE_TALK_TEMPLATE
        }
        
        template = templates.get(talk_type, templates["default"])
        return template.format(**kwargs)