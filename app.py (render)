import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import pandas as pd
import json
import threading

st.set_page_config(page_title="Encuesta de Capacitación", layout="centered")

# === ESTILOS CUSTOM ===
st.markdown("""
<style>
div.row-widget.stRadio > div {
    flex-direction: column;
    gap: 20px !important;
}
div.row-widget.stRadio > div[role="radiogroup"] > label {
    margin-top: 22px !important;
    margin-bottom: 22px !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}
div[data-testid="stRadio"] label {
    padding-top: 8px !important;
    padding-bottom: 8px !important;
    margin-bottom: 15px !important;
}
.st-emotion-cache-1qg05tj:not(:last-child) {
    margin-bottom: 20px !important;
}
div[data-baseweb="radio"] label {
    font-size: 1.5rem !important;
    line-height: 1.8;
}
textarea {
    min-height: 150px !important;
    font-size: 1.05rem !important;
}
div.stButton > button {
    font-size: 1.5rem;
    padding: 0.6rem 1.5rem;
    background-color: #e24c4b;
    color: white;
    border: none;
    border-radius: 10px;
    transition: background-color 0.3s;
    width: 100% !important;
    display: block !important;
    box-sizing: border-box !important;
}
div.stButton > button:hover {
    background-color: #c03d3c;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# === LOCK GLOBAL PARA GUARDADO SEGURO ===
@st.cache_resource
def get_global_lock():
    return threading.Lock()

lock = get_global_lock()

# === CACHE DE HOJA GOOGLE ===
# Este bloque tenía como función conectarse a una hoja de Google Sheets usando credenciales de servicio.
# La conexión se cacheaba con @st.cache_resource, lo que permitía que Streamlit la reutilice en vez de crear una nueva
# cada vez que un usuario accedía a la app.
# Sin embargo, al no tener protección adicional con un lock, este código era vulnerable a errores si varias sesiones
# intentaban conectarse a la hoja al mismo tiempo. Por eso, esta versión fue reemplazada por una versión mejorada
# que incluye un bloqueo con `threading.Lock()` para manejar concurrencia de forma segura.

#@st.cache_resource
#def get_hoja_google():
#    scope = ["https://www.googleapis.com/auth/spreadsheets"]
#    credenciales_dict = json.loads(st.secrets["GOOGLE_CREDS"])
#    creds = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
#    gc = gspread.authorize(creds)
#    return gc.open_by_key("1440OXxY-2bw7NAFr01hGeiVYrbHu_G47u9IIoLfaAjM")


# === CACHE DE HOJA GOOGLE ===
# Este bloque se encarga de establecer una conexión segura y eficiente con una hoja de Google Sheets,
# usando credenciales de servicio y protegiendo el acceso con un "lock global".
# El decorador @st.cache_resource permite que Streamlit reutilice esta conexión entre sesiones,
# evitando que se vuelva a ejecutar cada vez que un nuevo usuario abre la app.
# Además, al usar `with get_global_lock()`, evitamos que múltiples sesiones ejecuten la conexión al mismo tiempo,
# lo cual podría saturar la API de Google y causar errores cuando hay muchos usuarios concurrentes.

@st.cache_resource  # Streamlit guarda esta función como recurso compartido entre sesiones activas
def get_hoja_google():
    with get_global_lock():  # Solo una sesión a la vez puede ejecutar este bloque (protección contra concurrencia)
        scope = ["https://www.googleapis.com/auth/spreadsheets"]  # Definimos los permisos necesarios para acceder a Google Sheets
      #  credenciales_dict = json.loads(st.secrets["GOOGLE_CREDS"])  # Cargamos las credenciales de servicio desde el archivo secreto
        with open("/etc/secrets/GOOGLE_CREDS.json") as f:
            credenciales_dict = json.load(f)        
        creds = Credentials.from_service_account_info(credenciales_dict, scopes=scope)  # Creamos el objeto de credenciales con permisos
        gc = gspread.authorize(creds)  # Autorizamos la conexión a Google Sheets usando las credenciales
        return gc.open_by_key("1440OXxY-2bw7NAFr01hGeiVYrbHu_G47u9IIoLfaAjM")  # Abrimos la hoja por su ID único y la devolvemos

# === INTENTAR CARGAR HOJA ===
try:
    sheet = get_hoja_google()
except Exception as e:
    st.error("❌ No se pudo cargar el formulario. Intentalo nuevamente en unos minutos.")
    st.stop()

# === OBTENER PARÁMETRO DE COMISIÓN ===
params = st.query_params
comision = params.get("curso", "sin_codigo")

# === TÍTULO SIMPLIFICADO ===
st.title("📝 Encuesta de Opinión")
st.markdown("<br>", unsafe_allow_html=True)

# === FORMULARIO ===
if "enviado" not in st.session_state or not st.session_state.enviado:

    st.markdown("##### 📌 ¿TENÍAS CONOCIMIENTOS PREVIOS SOBRE LOS TEMAS DESARROLLADOS EN ESTA CAPACITACIÓN?")
    conocimientos_previos = st.radio("", ["CONOCÍA BIEN LOS TEMAS", "TENÍA ALGÚN CONOCIMIENTO", "DESCONOCÍA LOS TEMAS"], index=None)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 📌 ¿CÓMO CALIFICARÍAS ESTA CAPACITACIÓN EN GENERAL?")
    valoracion_curso = st.radio("", ["EXCELENTE", "MUY BUENA", "BUENA", "REGULAR", "MALA"], index=None)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 📌 ¿CREÉS QUE VAS A APLICAR A TUS TAREAS HABITUALES LOS CONOCIMIENTOS ADQUIRIDOS EN ESTE CURSO?")
    conocimientos_aplicables = st.radio("", ["TOTALMENTE DE ACUERDO", "DE ACUERDO", "PARCIALMENTE DE ACUERDO", "EN DESACUERDO"], index=None)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 📌 ¿CÓMO CALIFICARÍAS EL DESEMPEÑO DEL/LOS DOCENTE/S?")
    valoracion_docente = st.radio("", ["EXCELENTE", "MUY BUENO", "BUENO", "REGULAR", "MALO"], index=None)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 💬 CONTANOS QUÉ APRENDIZAJES ADQUIRISTE EN ESTA CAPACITACIÓN.")
    aprendizajes_adquiridos = st.text_area("aprendizajes", placeholder="Escribí aquí...", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 💬 COMENTARIOS O SUGERENCIAS QUE PUEDAN RESULTAR ÚTILES PARA FUTURAS CAPACITACIONES (OPCIONAL)")
    comentarios = st.text_area("comentarios", placeholder="Escribí aquí...", label_visibility="collapsed")
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    if st.button("📤 ENVIAR RESPUESTA"):
        if not all([conocimientos_previos, valoracion_curso, conocimientos_aplicables, valoracion_docente, aprendizajes_adquiridos]):
            st.warning("⚠️ Por favor, completá todas las preguntas obligatorias antes de enviar.")
        else:
            try:
                with lock:
                    worksheet = sheet.worksheet("respuestas")
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    fila = [
                        fecha,
                        comision,
                        conocimientos_previos,
                        valoracion_curso,
                        conocimientos_aplicables,
                        valoracion_docente,
                        aprendizajes_adquiridos,
                        comentarios
                    ]
                    worksheet.append_row(fila)
                    st.session_state.enviado = True
                    st.rerun()
            except Exception as e:
                st.error("❌ Hubo un error al guardar tu respuesta. Por favor, intentá nuevamente.")
                st.exception(e)

else:
    st.success("✅ ¡GRACIAS! TU OPINIÓN FUE ENVIADA CORRECTAMENTE.")
