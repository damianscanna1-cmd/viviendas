import streamlit as st
import json
import os
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# CONFIGURACIÓN Y BLOQUEO CSS DE ELEMENTOS NATIVOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dossier Inmobiliario Privado",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Ocultamiento estricto y bloqueo absoluto de elementos flotantes, badges y toolbar */
    #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stDecoration"], [data-testid="stStatusWidget"], .stAppDeployButton {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0px !important;
        max-height: 0px !important;
    }
    
    div[class*="viewerBadge"], 
    div[class*="stActionButton"], 
    div[class*="viewerBadge_container"],
    iframe[src*="streamlit"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        z-index: -999999 !important;
    }
    
    html, body, .stApp {
        background-color: #0f1115;
        color: #f3f4f6;
        max-width: 100vw;
        overflow-x: hidden !important;
    }
    
    .main { 
        background-color: #0f1115; 
        color: #f3f4f6;
        padding-top: 1rem !important;
    }

    h1, h2, h3 { color: #c5a880 !important; }
    .stButton>button { 
        background-color: #c5a880; 
        color: #0f1115; 
        font-weight: bold; 
        border-radius: 8px; 
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "propiedades.json"
WHATSAPP_NUMBER = "34637128212"

# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------
def image_to_base64(image_file):
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail((1600, 1200))
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

# -----------------------------------------------------------------------------
# COMPONENTE GALERÍA
# -----------------------------------------------------------------------------
def render_galeria(imagenes, is_es=True, height=480):
    imgs_json = json.dumps(imagenes)
    expand_txt = "🔍 Ampliar Foto" if is_es else "🔍 Enlarge Photo"
    close_txt = "✖ Cerrar" if is_es else "✖ Close"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <style>
      * {{ box-sizing: border-box; }}
      html, body {{ 
        margin: 0; padding: 0; width: 100%; height: 100%;
        background-color: #0f1115; font-family: system-ui, -apple-system, sans-serif; 
        color: #f3f4f6; overflow: hidden; touch-action: manipulation; 
      }}
      .gallery-container {{
        position: relative; width: 100%; height: 100vh; max-height: 480px;
        margin: 0 auto; background: #0f1115; border-radius: 10px; overflow: hidden;
        display: flex; align-items: center; justify-content: center; user-select: none;
      }}
      .img-wrapper {{
        width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #0f1115;
      }}
      .img-wrapper img {{
        max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain;
      }}
      .click-zone {{
        position: absolute; top: 0; height: 100%; width: 30%; cursor: pointer; display: flex; align-items: center; z-index: 5;
      }}
      .click-zone-left {{ left: 0; justify-content: flex-start; padding-left: 10px; }}
      .click-zone-right {{ right: 0; justify-content: flex-end; padding-right: 10px; }}
      .arrow-btn {{
        background: rgba(15, 17, 21, 0.75); color: #c5a880; font-size: 20px; font-weight: bold;
        width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        border: 1px solid #c5a880; opacity: 0.85;
      }}
      .bottom-bar {{
        position: absolute; bottom: 12px; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: 10px; z-index: 6;
      }}
      .counter-badge {{
        background: rgba(15, 17, 21, 0.85); color: #c5a880; padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; border: 1px solid #c5a880;
      }}
      .expand-btn {{
        background: rgba(197, 168, 128, 0.95); color: #0f1115; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; border: 1px solid #c5a880; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      }}
    </style>
    </head>
    <body>
      <div class="gallery-container">
        <div class="img-wrapper">
          <img id="slide" src="" alt="Galería" onclick="openModal()" style="cursor: zoom-in;">
        </div>
        <div class="click-zone click-zone-left" onclick="prevSlide(event)"><div class="arrow-btn">&#10094;</div></div>
        <div class="click-zone click-zone-right" onclick="nextSlide(event)"><div class="arrow-btn">&#10095;</div></div>
        <div class="bottom-bar">
          <div id="badge" class="counter-badge">1/1</div>
          <button class="expand-btn" onclick="openModal()">{expand_txt}</button>
        </div>
      </div>
      <script>
        const photos = {imgs_json};
        let current = 0;
        function getTargetDoc() {{
          try {{ if (window.top && window.top.document && window.top.document.body) return window.top.document; }} catch(e) {{}}
          return document;
        }}
        function render() {{
          if (photos.length === 0) return;
          const src = "data:image/jpeg;base64," + photos[current];
          document.getElementById('slide').src = src;
          const label = (current + 1) + "/" + photos.length;
          document.getElementById('badge').innerText = label;
          const doc = getTargetDoc();
          const modalImg = doc.getElementById('ghs-modal-img');
          const modalBadge = doc.getElementById('ghs-modal-badge');
          if (modalImg) modalImg.src = src;
          if (modalBadge) modalBadge.innerText = label;
        }}
        function nextSlide(e) {{ if(e) e.stopPropagation(); current = (current + 1) % photos.length; render(); }}
        function prevSlide(e) {{ if(e) e.stopPropagation(); current = (current - 1 + photos.length) % photos.length; render(); }}
        function openModal() {{
          if (photos.length === 0) return;
          const doc = getTargetDoc();
          let overlay = doc.getElementById('ghs-mobile-fullscreen-modal');
          if (!overlay) {{
            overlay = doc.createElement('div');
            overlay.id = 'ghs-mobile-fullscreen-modal';
            overlay.style.cssText = 'position: fixed !important; top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important; background-color: #000000 !important; z-index: 2147483647 !important; display: flex !important; align-items: center !important; justify-content: center !important;';
            overlay.innerHTML = `
              <button id="ghs-modal-close" style="position: absolute; top: 20px; right: 20px; background: rgba(197, 168, 128, 0.95); color: #0f1115; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; z-index: 2147483647;">{close_txt}</button>
              <div id="ghs-modal-prev" style="position: absolute; top: 50%; left: 15px; transform: translateY(-50%); background: rgba(15, 17, 21, 0.85); color: #c5a880; border: 1px solid #c5a880; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2147483647;">&#10094;</div>
              <img id="ghs-modal-img" src="" style="width: 100vw; height: 100vh; object-fit: contain; background: #000;">
              <div id="ghs-modal-next" style="position: absolute; top: 50%; right: 15px; transform: translateY(-50%); background: rgba(15, 17, 21, 0.85); color: #c5a880; border: 1px solid #c5a880; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 2147483647;">&#10095;</div>
              <div id="ghs-modal-badge" style="position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%); background: rgba(15, 17, 21, 0.85); color: #c5a880; padding: 6px 18px; border-radius: 20px; font-weight: bold; border: 1px solid #c5a880; z-index: 2147483647;">1/1</div>
            `;
            doc.body.appendChild(overlay);
            doc.getElementById('ghs-modal-close').onclick = closeModal;
            doc.getElementById('ghs-modal-prev').onclick = (e) => prevSlide(e);
            doc.getElementById('ghs-modal-next').onclick = (e) => nextSlide(e);
          }}
          overlay.style.display = 'flex';
          render();
        }}
        function closeModal() {{
          const doc = getTargetDoc();
          const overlay = doc.getElementById('ghs-mobile-fullscreen-modal');
          if (overlay) overlay.style.display = 'none';
        }}
        render();
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

# -----------------------------------------------------------------------------
# APLICACIÓN PRINCIPAL CON SEGURIDAD ESTRICTA (BLOQUEO DE CREACIÓN / ADMIN)
# -----------------------------------------------------------------------------
st.sidebar.title("🚪 Navegación")
modo = st.sidebar.radio("Modo de Acceso", ["Vista Cliente", "Panel de Administración (Crear/Editar)"])
st.sidebar.markdown("---")

if modo == "Vista Cliente":
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

            titulo = prop_data["titulo_es"] if is_es else prop_data["titulo_en"]
            st.header(titulo)
            st.caption(f"📍 {prop_data['ubicacion']}")

            imagenes = prop_data.get("imagenes", [])
            if imagenes:
                st.subheader("📸 Galería de Fotografías" if is_es else "📸 Photo Gallery")
                render_galeria(imagenes, is_es=is_es)
            else:
                st.info("No hay fotos subidas para esta propiedad." if is_es else "No photos uploaded yet.")

            if prop_data.get("video_url"):
                st.subheader("Recorrido en Vídeo" if is_es else "Video Tour")
                st.video(prop_data["video_url"])

            st.markdown("---")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Superficie / Area", prop_data["superficie"])
            col2.metric("Habitaciones / Beds", prop_data["habitaciones"])
            col3.metric("Baños / Baths", prop_data["banos"])
            col4.metric("Precio / Price", prop_data["precio"])

            st.subheader("Descripción" if is_es else "Description")
            desc = prop_data["descripcion_es"] if is_es else prop_data["descripcion_en"]
            st.write(desc)

            st.markdown("---")
            st.link_button(
                "💬 Contactar por WhatsApp" if is_es else "💬 Contact via WhatsApp",
                f"https://wa.me/{WHATSAPP_NUMBER}"
            )
        elif pass_input != "":
            st.error("Contraseña incorrecta." if is_es else "Incorrect password.")
    else:
        st.info("No hay propiedades disponibles.")

elif modo == "Panel de Administración (Crear/Editar)":
    st.title("🛠️ Panel de Control - Administración")
    
    admin_pass = st.text_input("Contraseña exclusiva de Administrador (para Crear y Editar):", type="password")
    
    if admin_pass == db["admin_password"]:
        st.success("Sesión de administrador activa. Funciones de creación y edición desbloqueadas.")
        
        tab1, tab2 = st.tabs(["Editar Propiedad", "Crear Nueva Propiedad"])

        with tab1:
            prop_keys = list(db["propiedades"].keys())
            if prop_keys:
                prop_edit = st.selectbox("Seleccionar Inmueble para Modificar:", prop_keys)
                p_data = db["propiedades"][prop_edit]

                st.subheader("📸 Gestión de Fotografías")
                if "imagenes" not in p_data:
                    p_data["imagenes"] = []
                
                if p_data["imagenes"]:
                    st.write("Fotos actuales (la número 1 es la **Foto Principal**):")
                    grid_cols = st.columns(4)
                    for i, img_b64 in enumerate(p_data["imagenes"]):
                        img_bytes = base64.b64decode(img_b64)
                        grid_cols[i % 4].image(img_bytes, use_container_width=True)
                        
                        if i == 0:
                            grid_cols[i % 4].info("⭐ Principal")
                        else:
                            if grid_cols[i % 4].button(f"⭐ Fijar como 1ª", key=f"main_{prop_edit}_{i}"):
                                p_data["imagenes"].insert(0, p_data["imagenes"].pop(i))
                                guardar_datos(db)
                                st.rerun()

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

                with st.form("edit_form"):
                    st.subheader("📝 Datos del Inmueble")
                    col_a, col_b = st.columns(2)
                    p_data["titulo_es"] = col_a.text_input("Título (ES)", p_data["titulo_es"])
                    p_data["titulo_en"] = col_b.text_input("Título (EN)", p_data["titulo_en"])

                    p_data["precio"] = col_a.text_input("Precio", p_data["precio"])
                    p_data["ubicacion"] = col_b.text_input("Ubicación", p_data["ubicacion"])

                    p_data["superficie"] = col_a.text_input("Superficie", p_data["superficie"])
                    p_data["habitaciones"] = col_a.text_input("Habitaciones", p_data["habitaciones"])
                    p_data["banos"] = col_b.text_input("Baños", p_data["banos"])
                    
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
    elif admin_pass != "":
        st.error("Clave de administrador incorrecta. Acceso denegado a la creación y gestión.")
