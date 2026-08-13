import streamlit as st
import json
import os
import base64
from PIL import Image
import io

# Configuración de la página
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

DATA_FILE = "propiedades.json"

# Función para optimizar y convertir imágenes a Base64
def image_to_base64(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail((1600, 1200)) # Redimensionar para optimizar espacio
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()

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
                "descripcion_es": "Exclusiva vivienda reformada con acabados de primera calidad, diseño minimalista e iluminación natural óptima en todas sus estancias.",
                "descripcion_en": "Exclusive fully renovated property with top-quality finishes, minimalist design, and optimal natural light throughout.",
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

# Selector lateral: Vista Cliente vs Panel Admin
st.sidebar.title("🚪 Acceso")
modo = st.sidebar.radio("Navegación", ["Vista Cliente", "Panel de Administración"])

# ==========================================
# 1. VISTA CLIENTE
# ==========================================
if modo == "Vista Cliente":
    st.sidebar.markdown("---")
    lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español 🇪🇸", "English 🇬🇧"])
    is_es = "Español" in lang

    prop_keys = list(db["propiedades"].keys())
    if prop_keys:
        prop_sel = st.sidebar.selectbox("Selecciona la Propiedad", prop_keys)
        prop_data = db["propiedades"][prop_sel]

        st.title("🔒 Dossier Inmobiliario Privado")
        
        pass_input = st.text_input("Introduce la contraseña para ver la propiedad:", type="password")

        if pass_input == prop_data["password_cliente"]:
            st.success("Acceso autorizado" if is_es else "Access granted")
            st.markdown("---")

            # Encabezado
            titulo = prop_data["titulo_es"] if is_es else prop_data["titulo_en"]
            st.header(titulo)
            st.caption(f"📍 {prop_data['ubicacion']}")

            # GALERÍA DE FOTOS
            imagenes = prop_data.get("imagenes", [])
            if imagenes:
                st.subheader("Galería de Imágenes" if is_es else "Photo Gallery")
                cols = st.columns(2)
                for idx, img_b64 in enumerate(imagenes):
                    img_bytes = base64.b64decode(img_b64)
                    cols[idx % 2].image(img_bytes, use_container_width=True)
            else:
                st.info("No hay fotos subidas para esta propiedad." if is_es else "No photos uploaded yet.")

            st.markdown("---")

            # DATOS TÉCNICOS Y PRECIO
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Superficie / Area", prop_data["superficie"])
            col2.metric("Habitaciones / Beds", prop_data["habitaciones"])
            col3.metric("Baños / Baths", prop_data["banos"])
            col4.metric("Precio / Price", prop_data["precio"])

            # DESCRIPCIÓN
            st.subheader("Descripción" if is_es else "Description")
            desc = prop_data["descripcion_es"] if is_es else prop_data["descripcion_en"]
            st.write(desc)

            # RECORRIDO EN VÍDEO
            if prop_data.get("video_url"):
                st.subheader("Recorrido en Vídeo" if is_es else "Video Tour")
                st.video(prop_data["video_url"])

            # CONTACTO
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

                # SECCIÓN FOTOGRAFÍAS
                st.subheader("📸 Gestión de Fotografías")
                
                if "imagenes" not in p_data:
                    p_data["imagenes"] = []
                
                if p_data["imagenes"]:
                    st.write("Fotos actuales:")
                    grid_cols = st.columns(4)
                    for i, img_b64 in enumerate(p_data["imagenes"]):
                        img_bytes = base64.b64decode(img_b64)
                        grid_cols[i % 4].image(img_bytes, use_container_width=True)
                        if grid_cols[i % 4].button(f"🗑️ Eliminar #{i+1}", key=f"del_{prop_edit}_{i}"):
                            p_data["imagenes"].pop(i)
                            guardar_datos(db)
                            st.rerun()

                nuevas_fotos = st.file_uploader(
                    "Añadir nuevas imágenes (JPG, PNG, WEBP)", 
                    type=["jpg", "jpeg", "png", "webp"], 
                    accept_multiple_files=True
                )
                
                if nuevas_fotos:
                    if st.button("⬆️ Subir e Integrar Fotos"):
                        for f in nuevas_fotos:
                            b64_str = image_to_base64(f)
                            p_data["imagenes"].append(b64_str)
                        guardar_datos(db)
                        st.success(f"¡{len(nuevas_fotos)} fotos añadidas correctamente!")
                        st.rerun()

                st.markdown("---")

                # FORMULARIO DE TEXTOS Y PARÁMETROS
                with st.form("edit_form"):
                    st.subheader("📝 Datos del Inmueble")
                    col_a, col_b = st.columns(2)
                    p_data["titulo_es"] = col_a.text_input("Título (ES)", p_data["titulo_es"])
                    p_data["titulo_en"] = col_b.text_input("Título (EN)", p_data["titulo_en"])

                    p_data["precio"] = col_a.text_input("Precio", p_data["precio"])
                    p_data["ubicacion"] = col_b.text_input("Ubicación", p_data["ubicacion"])

                    p_data["superficie"] = col_a.text_input("Superficie", p_data["superficie"])
                    p_data["habitaciones"] = col_a.text_input("Habitaciones", p_data["habitaciones"])
                    p_data["banos"] = col_a.text_input("Baños", p_data["banos"])
                    
                    p_data["password_cliente"] = col_b.text_input("Contraseña para el Cliente", p_data["password_cliente"])

                    p_data["descripcion_es"] = st.text_area("Descripción (ES)", p_data["descripcion_es"])
                    p_data["descripcion_en"] = st.text_area("Descripción (EN)", p_data["descripcion_en"])

                    p_data["video_url"] = st.text_input("URL del Vídeo (YouTube/Vimeo/MP4)", p_data.get("video_url", ""))

                    submitted = st.form_submit_button("💾 Guardar Datos y Textos")
                    if submitted:
                        guardar_datos(db)
                        st.toast("¡Datos del inmueble guardados!")

        with tab2:
            st.subheader("Añadir Nueva Propiedad al Portafolio")
            new_id = st.text_input("Identificador único (ej: piso-gran-via, atico-patacona)")
            if st.button("Crear Inmueble"):
                if new_id and new_id not in db["propiedades"]:
                    db["propiedades"][new_id] = {
                        "titulo_es": "Nueva Propiedad",
                        "titulo_en": "New Property",
                        "ubicacion": "Valencia, España",
                        "precio": "0 €",
                        "superficie": "0 m²",
                        "habitaciones": "0",
                        "banos": "0",
                        "descripcion_es": "Descripción...",
                        "descripcion_en": "Description...",
                        "video_url": "",
                        "password_cliente": "1234",
                        "imagenes": []
                    }
                    guardar_datos(db)
                    st.success(f"Propiedad '{new_id}' creada correctamente.")
                    st.rerun()
                elif new_id in db["propiedades"]:
                    st.error("Ese identificador ya existe.")
