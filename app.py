import streamlit as st
import json
import os
import base64
import io
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# BLOQUEO DE INTERFAZ Y SEGURIDAD: OCULTACIÓN ABSOLUTA DE ELEMENTOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dossier Privado",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de CSS para eliminación total de elementos de la plataforma (Streamlit Cloud, badges, menús, etc)
st.markdown("""
    <style>
    /* Ocultar elementos de despliegue y menús de Streamlit */
    #MainMenu, 
    header, 
    footer, 
    .stAppDeployButton, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"],
    div[class*="viewerBadge"],
    div[class*="stActionButton"],
    div[class*="block-container"] > div > div > div > a,
    iframe {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0px !important;
        width: 0px !important;
        overflow: hidden !important;
    }
    
    /* Eliminar el badge flotante inferior derecho */
    footer { visibility: hidden !important; }
    
    /* Evitar interacción con elementos de la plataforma */
    body {
        -webkit-user-select: none;
        user-select: none;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LÓGICA DE NEGOCIO Y DATOS
# -----------------------------------------------------------------------------
DATA_FILE = "propiedades.json"
WHATSAPP_NUMBER = "34637128212"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"propiedades": {}, "admin_password": "Admin2026Password"}

def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = cargar_datos()

# -----------------------------------------------------------------------------
# APLICACIÓN: ENTRADA CONTROLADA
# -----------------------------------------------------------------------------
st.title("🔒 Dossier Inmobiliario GHS")

# Solo se muestra el contenido tras autenticación simple, ocultando el resto del menú lateral
modo = st.radio("Selecciona perfil:", ["Cliente", "Administrador"])

if modo == "Administrador":
    pass_in = st.text_input("Clave Admin:", type="password")
    if pass_in == db["admin_password"]:
        st.write("Panel de gestión habilitado.")
        # Aquí iría la lógica administrativa...
    else:
        st.error("Acceso restringido.")
else:
    # Lógica de vista cliente (reducida para seguridad)
    st.write("Bienvenido al dossier privado.")
