import streamlit as st
import streamlit.components.v1 as components
import json

# =====================================================================
# 1. CONFIGURACIÓN INICIAL Y MODULO DE PANTALLA COMPLETA EN MÓVILES
# =====================================================================
st.set_page_config(
    page_title="GHS - Catálogo Inmobiliario",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección CSS: Oculta barras de Streamlit y adapta el viewport a 100dvh para móviles
st.markdown("""
    <style>
        /* Ocultar elementos nativos de interfaz de Streamlit */
        header, footer, #MainMenu, div[data-testid="stToolbar"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        /* Viewport dinámico en móviles */
        html, body, [data-testid="stAppViewContainer"], .main {
            height: 100dvh !important;
            width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
            touch-action: manipulation;
        }

        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
        }

        /* Botón flotante discreto de apoyo para usuarios (+30 años) */
        .fs-btn {
            position: fixed;
            bottom: 15px;
            right: 15px;
            z-index: 999999;
            background: rgba(0, 0, 0, 0.75);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 13px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            cursor: pointer;
            backdrop-filter: blur(5px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# JavaScript: Disparo automático al primer toque (tap/swipe) o pulsación manual del botón
components.html("""
    <button class="fs-btn" id="fullScreenToggle" onclick="toggleFullScreen()">
        ⛶ Pantalla Completa
    </button>

    <script>
        function enableFullScreen() {
            var doc = window.parent.document.documentElement;
            if (doc.requestFullscreen) {
                doc.requestFullscreen();
            } else if (doc.webkitRequestFullscreen) { /* Safari / iOS / Android */
                doc.webkitRequestFullscreen();
            } else if (doc.msRequestFullscreen) {
                doc.msRequestFullscreen();
            }
        }

        function toggleFullScreen() {
            var doc = window.parent.document;
            if (!doc.fullscreenElement && !doc.webkitFullscreenElement) {
                enableFullScreen();
            } else {
                if (doc.exitFullscreen) {
                    doc.exitFullscreen();
                } else if (doc.webkitExitFullscreen) {
                    doc.webkitExitFullscreen();
                }
            }
        }

        // Activación automática e imperceptible al primer toque del usuario
        window.parent.document.addEventListener('touchstart', function() {
            enableFullScreen();
        }, { once: true });

        window.parent.document.addEventListener('click', function() {
            enableFullScreen();
        }, { once: true });
    </script>
""", height=0, width=0)

# =====================================================================
# 2. GESTIÓN DE AUTENTICACIÓN Y SESIÓN
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# Base de datos local de propiedades
if "properties" not in st.session_state:
    st.session_state["properties"] = [
        {
            "id": 1,
            "title": "Exclusiva Residencia Fibo Circle",
            "location": "Valencia, España",
            "price": "850.000 €",
            "description": "Exclusiva propiedad de diseño orgánico con estancias circulares, mobiliario modular a medida en acabado boucle crudo y acabados de lujo.",
            "description_en": "Exclusive organic design property with circular rooms, custom modular furniture in raw boucle finish and luxury fittings.",
            "images": [
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80"
            ],
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ"
        }
    ]

# Formulario de Acceso
def login():
    st.markdown("<div style='padding: 40px 20px; text-align: center;'>", unsafe_allow_html=True)
    st.title("GHS Gestión Integral de Proyectos")
    st.subheader("Acceso al Catálogo Inmobiliario")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            # Compatibilidad con credenciales de desarrollo y producción
            if username == "admin" and password in ["admin123", "Admin2026Password"]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "admin"
                st.rerun()
            elif username in ["cliente", "demo"] and password in ["cliente123", "demo", "Cliente2026"]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "client"
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state["authenticated"]:
    login()
    st.stop()

# =====================================================================
# 3. COMPONENTE DE CARRUSEL TÁCTIL INTERACTIVO (SWIPER.JS)
# =====================================================================
def render_property_carousel(prop, lang="es"):
    images_js = json.dumps(prop["images"])
    desc = prop["description_en"] if lang == "en" else prop["description"]
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0e1117; color: #fff; height: 100vh; overflow: hidden; }}
            .container {{ display: flex; flex-direction: column; height: 100vh; width: 100vw; }}
            
            /* Carrusel táctil Swiper */
            .swiper {{ width: 100%; height: 52vh; }}
            .swiper-slide img {{ width: 100%; height: 100%; object-fit: cover; }}
            
            /* Detalle de la propiedad */
            .details {{ flex: 1; padding: 20px; overflow-y: auto; background: #161b22; border-top-left-radius: 20px; border-top-right-radius: 20px; margin-top: -15px; position: relative; z-index: 10; }}
            .header-line {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
            .title {{ font-size: 20px; font-weight: 700; color: #ffffff; }}
            .price {{ font-size: 22px; font-weight: 800; color: #2ea043; }}
            .location {{ font-size: 13px; color: #8b949e; margin-bottom: 15px; }}
            .desc {{ font-size: 14px; line-height: 1.5; color: #c9d1d9; margin-bottom: 20px; }}
            
            /* Botón de Contacto por WhatsApp */
            .whatsapp-btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                background-color: #25D366;
                color: #ffffff;
                text-decoration: none;
                font-weight: 700;
                font-size: 15px;
                padding: 14px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="swiper">
                <div class="swiper-wrapper" id="swiper-wrapper"></div>
                <div class="swiper-pagination"></div>
                <div class="swiper-button-next"></div>
                <div class="swiper-button-prev"></div>
            </div>
            
            <div class="details">
                <div class="header-line">
                    <div class="title">{prop["title"]}</div>
                    <div class="price">{prop["price"]}</div>
                </div>
                <div class="location">📍 {prop["location"]}</div>
                <div class="desc">{desc}</div>
                
                <a class="whatsapp-btn" href="https://wa.me/34637128212?text=Hola,%20estoy%20interesado%20en%20la%20propiedad:%20{prop['title']}" target="_blank">
                    💬 Contactar por WhatsApp
                </a>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            const images = {images_js};
            const wrapper = document.getElementById('swiper-wrapper');
            
            images.forEach(imgUrl => {{
                const slide = document.createElement('div');
                slide.className = 'swiper-slide';
                slide.innerHTML = `<img src="${{imgUrl}}" alt="Propiedad" />`;
                wrapper.appendChild(slide);
            }});

            const swiper = new Swiper('.swiper', {{
                loop: true,
                pagination: {{ el: '.swiper-pagination', clickable: true }},
                navigation: {{ nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }},
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=750, scrolling=False)

# =====================================================================
# 4. INTERFAZ DE USUARIO SEGÚN ROL (ADMIN Y CLIENTE)
# =====================================================================
# Menú Lateral / Configuración
lang = st.sidebar.radio("Idioma / Language", ["ES", "EN"])
selected_lang = "es" if lang == "ES" else "en"

if st.sidebar.button("Cerrar Sesión"):
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = None
    st.rerun()

# PANEL DE ADMINISTRADOR
if st.session_state["user_role"] == "admin":
    st.sidebar.title("Panel de Control")
    st.title("Gestión de Inmuebles")
    
    with st.expander("➕ Agregar Nueva Propiedad"):
        new_title = st.text_input("Título de la Propiedad")
        new_loc = st.text_input("Ubicación", "Valencia")
        new_price = st.text_input("Precio", "0 €")
        new_desc_es = st.text_area("Descripción (Español)")
        new_desc_en = st.text_area("Descripción (Inglés)")
        new_imgs = st.text_area("URLs de Imágenes (una por línea)")
        
        if st.button("Guardar Propiedad"):
            img_list = [url.strip() for url in new_imgs.split("\n") if url.strip()]
            new_prop = {
                "id": len(st.session_state["properties"]) + 1,
                "title": new_title,
                "location": new_loc,
                "price": new_price,
                "description": new_desc_es,
                "description_en": new_desc_en,
                "images": img_list if img_list else ["https://images.unsplash.com/photo-1600585154340-be6161a56a0c"],
                "video_url": ""
            }
            st.session_state["properties"].append(new_prop)
            st.success("Propiedad agregada correctamente.")
            st.rerun()

    st.subheader("Vista Previa del Catálogo")
    for prop in st.session_state["properties"]:
        render_property_carousel(prop, lang=selected_lang)

# VISTA DE CLIENTE
else:
    for prop in st.session_state["properties"]:
        render_property_carousel(prop, lang=selected_lang)
