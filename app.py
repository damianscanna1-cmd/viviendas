import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ADAPTACIÓN PANTALLA COMPLETA + TÁCTIL
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gestión Inmobiliaria | Catálogo Interactivo",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="auto"
)

# CSS con protección Anti-Scroll Involuntario, Ajuste Móvil y Estilo WhatsApp
st.markdown("""
    <style>
        /* 1. ANTI-SCROLL INVOLUNTARIO Y REBOTE MÓVIL */
        html, body, .main {
            overscroll-behavior-y: contain !important;
            touch-action: pan-x pan-y;
        }

        /* 2. Pantalla completa sin márgenes desaprovechados */
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            max-width: 100% !important;
        }

        /* Ocultar elementos nativos innecesarios */
        #MainMenu, footer, header {visibility: hidden;}

        /* Bordes redondeados para tarjetas */
        .stExpander {
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 1rem;
        }

        /* Botón personalizado estilo WhatsApp */
        .whatsapp-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #25D366;
            color: white !important;
            font-weight: bold;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none !important;
            width: 100%;
            text-align: center;
            box-shadow: 0 4px 8px rgba(37, 211, 102, 0.3);
            transition: background-color 0.3s ease;
            margin-top: 10px;
            margin-bottom: 15px;
        }
        .whatsapp-btn:hover {
            background-color: #128C7E;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.4rem !important;
                padding-right: 0.4rem !important;
            }
            .stButton>button {
                width: 100% !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# NÚMERO DE CONTACTO FIJO (WHATSAPP)
WHATSAPP_NUMBER = "34637128212"

# -----------------------------------------------------------------------------
# COMPONENTE: CARRUSEL TÁCTIL (Touch Swipe + Anti-Scroll Lateral)
# -----------------------------------------------------------------------------
def render_touch_carousel(photo_list):
    """
    Renderiza un carrusel táctil nativo para móviles utilizando Swiper.js.
    """
    slides_html = "".join([f'<div class="swiper-slide"><img src="{url}" /></div>' for url in photo_list])
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <style>
            body {{
                margin: 0;
                background: transparent;
                touch-action: pan-y;
            }}
            .swiper {{
                width: 100%;
                height: 380px;
                border-radius: 12px;
                touch-action: pan-x;
            }}
            .swiper-slide img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 12px;
            }}
            .swiper-button-next, .swiper-button-prev {{
                color: #ffffff;
                filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.6));
            }}
            .swiper-pagination-bullet-active {{
                background: #ffffff !important;
            }}
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                {slides_html}
            </div>
            <div class="swiper-button-next"></div>
            <div class="swiper-button-prev"></div>
            <div class="swiper-pagination"></div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            var swiper = new Swiper(".mySwiper", {{
                loop: true,
                grabCursor: true,
                touchEventsTarget: 'wrapper',
                preventClicksPropagation: true,
                pagination: {{
                    el: ".swiper-pagination",
                    clickable: true,
                }},
                navigation: {{
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                }},
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=400)

# -----------------------------------------------------------------------------
# GESTIÓN DE ESTADO Y DATOS
# -----------------------------------------------------------------------------
if "properties" not in st.session_state:
    st.session_state.properties = [
        {
            "id": 1,
            "title": "Ático Exclusivo con Terraza",
            "location": "Valencia Centro",
            "price": "450.000 €",
            "description": "Lujoso ático reformado con acabados de alta gama, iluminación natural y vistas despejadas.",
            "photos": [
                "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80"
            ],
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "client_pass": "cliente123"
        }
    ]

if "authenticated_role" not in st.session_state:
    st.session_state.authenticated_role = None

# -----------------------------------------------------------------------------
# AUTENTICACIÓN
# -----------------------------------------------------------------------------
def login_sidebar():
    st.sidebar.title("🔑 Acceso al Sistema")
    role = st.sidebar.radio("Selecciona tu rol:", ["Cliente", "Administrador"])
    
    if role == "Administrador":
        admin_pass = st.sidebar.text_input("Contraseña de Admin", type="password")
        if st.sidebar.button("Entrar como Admin"):
            if admin_pass == "admin123":
                st.session_state.authenticated_role = "admin"
                st.sidebar.success("Sesión iniciada como Admin")
                st.rerun()
            else:
                st.sidebar.error("Contraseña incorrecta")
                
    elif role == "Cliente":
        client_pass = st.sidebar.text_input("Contraseña de Acceso", type="password")
        if st.sidebar.button("Ver Inmuebles"):
            valid = any(p["client_pass"] == client_pass for p in st.session_state.properties)
            if valid or client_pass == "demo":
                st.session_state.authenticated_role = "client"
                st.sidebar.success("Acceso concedido")
                st.rerun()
            else:
                st.sidebar.error("Contraseña inválida")

    if st.session_state.authenticated_role is not None:
        st.sidebar.divider()
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.authenticated_role = None
            st.rerun()

# -----------------------------------------------------------------------------
# VISTA: CLIENTE (Con Botón WhatsApp Directo)
# -----------------------------------------------------------------------------
def show_client_view():
    st.title("🏡 Catálogo Exclusivo de Propiedades")
    
    if not st.session_state.properties:
        st.info("No hay propiedades disponibles en este momento.")
        return

    for prop in st.session_state.properties:
        with st.expander(f"📍 {prop['title']} — {prop['location']} ({prop['price']})", expanded=True):
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.write(f"*Descripción:* {prop['description']}")
                
                # Carrusel Táctil
                if prop["photos"]:
                    st.subheader("🖼️ Galería de Fotos (Desliza con el dedo 👈👉)")
                    render_touch_carousel(prop["photos"])

            with col2:
                # Botón directo WhatsApp con mensaje preconfigurado
                message = f"Hola, estoy interesado en obtener más información sobre la propiedad: '{prop['title']}' (ID #{prop['id']})."
                encoded_message = urllib.parse.quote(message)
                wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
                
                st.subheader("📲 Contactar por WhatsApp")
                st.markdown(
                    f'<a href="{wa_link}" target="_blank" class="whatsapp-btn">💬 Consultar sobre este inmueble</a>', 
                    unsafe_allow_html=True
                )
                
                if prop.get("youtube_url"):
                    st.subheader("🎥 Recorrido Virtual")
                    st.video(prop["youtube_url"])
                
                st.caption(f"ID Propiedad: #{prop['id']}")

# -----------------------------------------------------------------------------
# VISTA: ADMINISTRADOR
# -----------------------------------------------------------------------------
def show_admin_view():
    st.title("🛠️ Panel de Administración Inmobiliaria")
    
    tabs = st.tabs(["➕ Añadir Propiedad", "✏️ Gestionar Propiedades", "💾 Código Fuente"])
    
    with tabs[0]:
        st.subheader("Registrar nuevo inmueble")
        with st.form("new_property_form"):
            title = st.text_input("Título de la Propiedad")
            location = st.text_input("Ubicación")
            price = st.text_input("Precio")
            description = st.text_area("Descripción detallada")
            photos_raw = st.text_area("URLs de fotos (una por línea)")
            youtube_url = st.text_input("URL del vídeo de YouTube (opcional)")
            client_pass = st.text_input("Contraseña para el cliente", value="cliente123")
            
            submitted = st.form_submit_button("Guardar Propiedad")
            if submitted:
                photos_list = [p.strip() for p in photos_raw.split("\n") if p.strip()]
                new_prop = {
                    "id": len(st.session_state.properties) + 1,
                    "title": title,
                    "location": location,
                    "price": price,
                    "description": description,
                    "photos": photos_list if photos_list else ["https://via.placeholder.com/800x600"],
                    "youtube_url": youtube_url,
                    "client_pass": client_pass
                }
                st.session_state.properties.append(new_prop)
                st.success("¡Propiedad añadida con éxito!")
                st.rerun()

    with tabs[1]:
        st.subheader("Propiedades Registradas")
        for idx, prop in enumerate(st.session_state.properties):
            with st.container():
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    st.markdown(f"### {prop['title']} (ID #{prop['id']})")
                    st.write(f"*Ubicación:* {prop['location']} | *Precio:* {prop['price']}")
                    st.write(f"*Clave Cliente:* {prop['client_pass']}")
                
                with col_actions:
                    if st.button("❌ Eliminar", key=f"del_{prop['id']}"):
                        st.session_state.properties.pop(idx)
                        st.rerun()
                st.divider()

    with tabs[2]:
        st.subheader("📦 Descargar Script Fuente (app.py)")
        try:
            with open(__file__, "r", encoding="utf-8") as f:
                code_content = f.read()
            st.download_button(
                label="⬇️ Descargar app.py",
                data=code_content,
                file_name="app.py",
                mime="text/x-python"
            )
        except Exception:
            st.info("Descarga no disponible en entorno directo.")

# -----------------------------------------------------------------------------
# FLUJO PRINCIPAL
# -----------------------------------------------------------------------------
def main():
    login_sidebar()
    
    role = st.session_state.authenticated_role
    if role == "admin":
        show_admin_view()
    elif role == "client":
        show_client_view()
    else:
        st.title("🏡 Portal Inmobiliario")
        st.info("Abre la barra lateral para iniciar sesión como Cliente o Administrador.")

if __name__ == "__main__":
    main()
