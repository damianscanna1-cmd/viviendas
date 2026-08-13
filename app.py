import streamlit as st
import json
import os
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Propiedades - Real Estate Admin",
    page_icon="🏠",
    layout="wide"
)

# Estilos visuales personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar Estado de Sesión para las propiedades
if "properties" not in st.session_state:
    st.session_state.properties = {
        "vivienda-01": {
            "title": "Vivienda 01 - Residencial Exclusivo",
            "price": 285000,
            "surface": 85,
            "rooms": 3,
            "baths": 2,
            "description": "Exclusivo apartamento recién reformado con acabados de alta calidad, excelente iluminación natural y terraza.",
            "images": []  # Lista de imágenes subidas en bytes
        },
        "vivienda-02": {
            "title": "Vivienda 02 - Ático Luminoso",
            "price": 340000,
            "surface": 110,
            "rooms": 4,
            "baths": 2,
            "description": "Ático de diseño contemporáneo con vistas panorámicas y amplia distribución funcional.",
            "images": []
        }
    }

# Encabezado principal
st.markdown('<div class="main-header">Panel de Gestión Inmobiliaria</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Administración de catálogo de propiedades y gestión multimedia</div>', unsafe_allow_html=True)

# Pestañas de navegación
tab_edit, tab_create, tab_catalog = st.tabs(["✏️ Editar Propiedad", "➕ Crear Nueva Propiedad", "📋 Catálogo General"])

# ---------------------------------------------------------
# PESTAÑA 1: EDITAR PROPIEDAD Y GESTIÓN DE FOTOS
# ---------------------------------------------------------
with tab_edit:
    prop_keys = list(st.session_state.properties.keys())
    
    if not prop_keys:
        st.info("No hay propiedades registradas en el sistema.")
    else:
        selected_key = st.selectbox("Seleccionar Inmueble para Modificar:", prop_keys)
        prop_data = st.session_state.properties[selected_key]

        col1, col2 = st.columns([1, 1], gap="medium")

        # Columna Izquierda: Formulario de datos
        with col1:
            st.subheader("📝 Datos del Inmueble")
            updated_title = st.text_input("Título de la propiedad", value=prop_data["title"])
            updated_price = st.number_input("Precio (€)", value=int(prop_data["price"]), step=5000)
            
            c_surf, c_room, c_bath = st.columns(3)
            with c_surf:
                updated_surface = st.number_input("Superficie (m²)", value=int(prop_data["surface"]))
            with c_room:
                updated_rooms = st.number_input("Habitaciones", value=int(prop_data["rooms"]))
            with c_bath:
                updated_baths = st.number_input("Baños", value=int(prop_data["baths"]))

            updated_desc = st.text_area("Descripción detallada", value=prop_data["description"], height=120)

            if st.button("💾 Guardar Cambios de la Propiedad", type="primary", key="save_prop"):
                st.session_state.properties[selected_key].update({
                    "title": updated_title,
                    "price": updated_price,
                    "surface": updated_surface,
                    "rooms": updated_rooms,
                    "baths": updated_baths,
                    "description": updated_desc
                })
                st.success("¡Datos actualizados correctamente!")

        # Columna Derecha: Carga y cuadrícula de fotos
        with col2:
            st.subheader("📸 Gestión de Fotografías")

            uploaded_files = st.file_uploader(
                "Subir nuevas fotografías (JPG, PNG)", 
                type=["jpg", "jpeg", "png"], 
                accept_multiple_files=True,
                key="image_uploader"
            )

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    if bytes_data and len(bytes_data) > 0:
                        st.session_state.properties[selected_key]["images"].append(bytes_data)
                st.success(f"Se han añadido {len(uploaded_files)} fotografía(s) a {selected_key}.")

            st.write("---")
            st.markdown("##### Fotos actuales:")

            images_list = st.session_state.properties[selected_key]["images"]

            if not images_list:
                st.info("No hay fotografías subidas para este inmueble todavía.")
            else:
                # Cuadrícula de 4 columnas
                grid_cols = st.columns(4)
                
                # --- SOLUCIÓN DEL ERROR (LÍNEA 172) ---
                for i, img_bytes in enumerate(images_list):
                    col_target = grid_cols[i % 4]
                    
                    # Validación para asegurar que img_bytes contenga datos
                    if img_bytes is not None and len(img_bytes) > 0:
                        try:
                            # Sintaxis actualizada
                            col_target.image(img_bytes, use_container_width=True)
                        except Exception:
                            # Respaldo por compatibilidad
                            try:
                                col_target.image(img_bytes, use_column_width=True)
                            except Exception:
                                col_target.error("Error al cargar imagen")
                    
                    # Botón para borrar foto individual
                    if col_target.button(f"🗑️ Borrar #{i+1}", key=f"del_img_{selected_key}_{i}"):
                        st.session_state.properties[selected_key]["images"].pop(i)
                        st.rerun()

# ---------------------------------------------------------
# PESTAÑA 2: CREAR NUEVA PROPIEDAD
# ---------------------------------------------------------
with tab_create:
    st.subheader("➕ Añadir Nueva Propiedad")
    with st.form("create_property_form"):
        new_id = st.text_input("Código / Identificador único (Ej: vivienda-03)")
        new_title = st.text_input("Título de la Propiedad")
        
        c1, c2, c3, c4 = st.columns(4)
        new_price = c1.number_input("Precio (€)", min_value=0, value=250000, step=5000)
        new_surface = c2.number_input("Superficie (m²)", min_value=0, value=90)
        new_rooms = c3.number_input("Habitaciones", min_value=0, value=3)
        new_baths = c4.number_input("Baños", min_value=0, value=2)

        new_desc = st.text_area("Descripción")
        
        submitted = st.form_submit_button("Registrar Propiedad", type="primary")
        
        if submitted:
            if not new_id or not new_title:
                st.error("Por favor, completa el identificador y el título de la propiedad.")
            elif new_id in st.session_state.properties:
                st.error("Ya existe una propiedad con ese identificador.")
            else:
                st.session_state.properties[new_id] = {
                    "title": new_title,
                    "price": new_price,
                    "surface": new_surface,
                    "rooms": new_rooms,
                    "baths": new_baths,
                    "description": new_desc,
                    "images": []
                }
                st.success(f"¡Propiedad {new_id} registrada con éxito!")

# ---------------------------------------------------------
# PESTAÑA 3: VISTA DE CATÁLOGO
# ---------------------------------------------------------
with tab_catalog:
    st.subheader("📋 Resumen del Catálogo Activo")
    
    for p_id, p_info in st.session_state.properties.items():
        with st.expander(f"🏡 {p_info['title']} ({p_id}) - {p_info['price']:,} €"):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.write(f"*Precio:* {p_info['price']:,} €")
                st.write(f"*Superficie:* {p_info['surface']} m² | *Habitaciones:* {p_info['rooms']} | *Baños:* {p_info['baths']}")
                st.write(f"*Descripción:* {p_info['description']}")
                st.write(f"*Fotos adjuntas:* {len(p_info['images'])}")
            
            with col_b:
                if p_info['images']:
                    first_img = p_info['images'][0]
                    if first_img:
                        st.image(first_img, caption="Vista previa principal", use_container_width=True)
                else:
                    st.info("Sin fotografías disponibles.")
