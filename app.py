import streamlit as st
import json
import os

# -----------------------------------------------------------------------------
# BLOQUEO ABSOLUTO DE ELEMENTOS DE STREAMLIT (CSS FORZADO)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Dossier GHS", layout="wide")

st.markdown("""
    <style>
    /* Ocultamiento agresivo de todos los elementos de la plataforma Streamlit */
    #MainMenu, header, footer, 
    [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    .stAppDeployButton, div[class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        height: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LÓGICA DE DATOS
# -----------------------------------------------------------------------------
DATA_FILE = "propiedades.json"
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"propiedades": {"ejemplo": {"password_cliente": "1234"}}, "admin_password": "admin"}

db = cargar_datos()

# -----------------------------------------------------------------------------
# NAVEGACIÓN Y AUTENTICACIÓN
# -----------------------------------------------------------------------------
st.title("🔑 Acceso al Dossier GHS")

# Radio button para el usuario
opcion = st.radio("Seleccione su tipo de acceso:", ["Cliente", "Administrador"])

if opcion == "Cliente":
    st.subheader("Acceso a Propiedades")
    clave = st.text_input("Introduzca su contraseña de cliente:", type="password")
    
    # Verificación de acceso para cliente
    acceso_concedido = False
    prop_permitida = None
    
    for id_prop, datos in db["propiedades"].items():
        if clave == datos["password_cliente"]:
            acceso_concedido = True
            prop_permitida = datos
            break
            
    if acceso_concedido:
        st.success("Acceso autorizado.")
        st.write("Bienvenido, aquí puede visualizar el dossier privado.")
        # Aquí renderizas los datos de prop_permitida
    elif clave != "":
        st.error("Contraseña incorrecta.")

elif opcion == "Administrador":
    st.subheader("Panel de Gestión")
    clave_admin = st.text_input("Clave de administrador:", type="password")
    if clave_admin == db["admin_password"]:
        st.success("Sesión administrativa iniciada.")
        # Aquí renderizas las funciones de edición
    elif clave_admin != "":
        st.error("Clave denegada.")
