# 🎤 Speaker Content Assistant: Boost Your Presentations with AI
##  Creator: Fer Osorio

Speaker Content Assistant is an innovative tool that uses Amazon Bedrock and Claude 3 to transform the way we prepare presentations and technical talks. Designed specifically for developers and technical speakers, this application helps you structure, organize, and optimize your content in a professional manner.

## Key Features

### Intelligent Content Generation
You are provided with a customized structure for different types of talks (Workshops, Keynotes, MeetUp) with an automatic distribution of the time you set for your talk to last. You are also given suggestions for visual resources and examples, adapted at all times to the target audience.

### Professional Management
You can save your generated chats, organizing them by category and version. You can also download them as .txt files.

### Types of Supported Talks
- 💻 Technical Talks
- 🎓 Workshops
- 🎪 Keynotes
- 🤝 Meetups
- 🌐 Webinars


## Technical Requirements

### Software
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### AWS services
- Cuenta AWS activa
- Acceso a Amazon Bedrock
- Credenciales AWS configuradas
- Región compatible con Bedrock

## Quick Start Guide

### 1. Preparing the Environment
```bash
# Cloning the repo
git clone https://github.com/tu-usuario/speaker-assistant.git
cd speaker-assistant

# Create and activate the Virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. AWS configuration
```bash
# Configurar credenciales AWS
aws configure
```

### 3. Running the app
```bash
streamlit run app/main.py
```

## Content related with the app
### AWS builder Center Article:
### Instagram Reel: 