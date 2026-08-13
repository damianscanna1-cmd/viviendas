import streamlit as st
import json
import os

# Configuración de página
st.set_page_config(
    page_title="Dossier Inmobiliario Privado",
    page_icon="🏠",
    layout="wide"
)

# Estilo personalizado oscuro y elegante
st.markdown("""
    <style>
    .main { background-color: #0f1115; color: #f3f4f6; }
    stApp { background-color: #0f1115; }
    h1, h2, h3 { color: #c5a880 !important; }
    .stButton>button { background-color: #c5a880; color: #0f1115; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Archivo de base de datos local (JSON)
DATA_FILE = "propiedades.json"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "propiedades": {
            "vivienda-01": {
                "titulo_es": "Ático / Dúplex de Lujo",
                "titulo_en": "Luxury Penthouse / Duplex",
                "ubicacion": "Valencia, España",
                "precio": "485.000 €",
                "superficie": "180 m²",
                "habitaciones": "3",
                "banos": "2",
                "descripcion_es": "Exclusiva vivienda reformada con acabados de primera calidad...",
                "descripcion_en": "Exclusive fully renovated property with top-quality finishes...",
                "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                "password_cliente": "Cliente2026",
                "imagenes": []
            }
        },
        "admin_password": "Admin2026Password"
    }

def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = cargar_datos()

# Selector lateral: Modo Cliente vs Modo Admin
st.sidebar.title("🚪 Acceso")
modo = st.sidebar.radio("Navegación", ["Vista Cliente", "Panel de Administración"])

# ==========================================
# 1. VISTA CLIENTE
# ==========================================
if modo == "Vista Cliente":
    st.sidebar.markdown("---")
    # Selector de Idioma
    lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español 🇪🇸", "English 🇬🇧"])
    is_es = "Español" in lang

    prop_keys = list(db["propiedades"].keys())
    if prop_keys:
        prop_sel = st.sidebar.selectbox("Selecciona la Propiedad", prop_keys)
        prop_data = db["propiedades"][prop_sel]

        st.title("🔒 Dossier Inmobiliario Privado")
        
        # Verificación de contraseña de cliente
        pass_input = st.text_input("Introduce la contraseña para ver la propiedad:", type="password")

        if pass_input == prop_data["password_cliente"]:
            st.success("Acceso autorizado" if is_es else "Access granted")
            st.markdown("---")

            # Encabezado
            titulo = prop_data["titulo_es"] if is_es else prop_data["titulo_en"]
            st.header(titulo)
            st.caption(f"📍 {prop_data['ubicacion']}")

            # KPIs principales
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Superficie / Area", prop_data["superficie"])
            col2.metric("Habitaciones / Beds", prop_data["habitaciones"])
            col3.metric("Baños / Baths", prop_data["banos"])
            col4.metric("Precio / Price", prop_data["precio"])

            # Descripción
            st.subheader("Descripción" if is_es else "Description")
            desc = prop_data["descripcion_es"] if is_es else prop_data["descripcion_en"]
            st.write(desc)

            # Recorrido en Vídeo
            if prop_data.get("video_url"):
                st.subheader("Recorrido en Vídeo" if is_es else "Video Tour")
                st.video(prop_data["video_url"])

            # Contacto
            st.markdown("---")
            st.link_button(
                "💬 Contactar por WhatsApp" if is_es else "💬 Contact via WhatsApp",
                "https://wa.me/34000000000"
            )
        elif pass_input != "":
            st.error("Contraseña incorrecta." if is_es else "Incorrect password.")
    else:
        st.info("No hay propiedades disponibles.")

# ==========================================
# 2. PANEL DE ADMINISTRACIÓN
# ==========================================
elif modo == "Panel de Administración":
    st.title("🛠️ Panel de Control - Administración")
    
    admin_pass = st.text_input("Contraseña de Administrador:", type="password")
    
    if admin_pass == db["admin_password"]:
        st.success("Sesión de administrador activa.")
        
        tab1, tab2 = st.tabs(["Editar Propiedad", "Crear Nueva Propiedad"])

        with tab1:
            prop_keys = list(db["propiedades"].keys())
            if prop_keys:
                prop_edit = st.selectbox("Seleccionar Inmueble para Modificar:", prop_keys)
                p_data = db["propiedades"][prop_edit]

                with st.form("edit_form"):
                    col_a, col_b = st.columns(2)
                    p_data["titulo_es"] = col_a.text_input("Título (ES)", p_data["titulo_es"])
                    p_data["titulo_en"] = col_b.text_input("Título (EN)", p_data["titulo_en"])

                    p_data["precio"] = col_a.text_input("Precio", p_data["precio"])
                    p_data["ubicacion"] = col_b.text_input("Ubicación", p_data["ubicacion"])

                    p_data["superficie"] = col_a.text_input("Superficie", p_data["superficie"])
                    p_data["habitaciones"] = col_b.text_input("Habitaciones", p_data["habitaciones"])
                    p_data["banos"] = col_a.text_input("Baños", p_data["banos"])
                    
                    # Contraseña exclusiva del cliente para este inmueble
                    p_data["password_cliente"] = col_b.text_input("Contraseña para el Cliente", p_data["password_cliente"])

                    p_data["descripcion_es"] = st.text_area("Descripción (ES)", p_data["descripcion_es"])
                    p_data["descripcion_en"] = st.text_area("Descripción (EN)", p_data["descripcion_en"])

                    p_data["video_url"] = st.text_input("URL del Vídeo (YouTube/Vimeo/MP4)", p_data.get("video_url", ""))

                    submitted = st.form_submit_button("💾 Guardar Cambios")
                    if submitted:
                        guardar_datos(db)
                        st.toast("¡Propiedad actualizada correctamente!")

        with tab2:
            st.subheader("Añadir Inmueble al Portafolio")
            # Lógica para registrar nuevas claves e inmuebles...