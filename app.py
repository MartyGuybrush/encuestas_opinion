import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import pandas as pd
import json

st.set_page_config(page_title="Encuesta de Capacitación", layout="centered")

st.markdown("""
<style>
/* Opciones de radio */
div[data-baseweb="radio"] label {
    display: block;
    font-size: 1.2rem !important;
    line-height: 1.6;
    margin-bottom: 0.5rem; /* Aumentá este valor para más separación */
}

/* Bullets (círculos) */
div[data-baseweb="radio"] svg {
    width: 1.4rem;
    height: 1.4rem;
    margin-right: 0.5rem;
}

/* TextArea más alto */
textarea {
    min-height: 150px !important;
    font-size: 1.05rem !important;
}

/* Botón estilizado */
div.stButton > button {
    font-size: 1.3rem;
    padding: 0.6rem 1.5rem;
    background-color: #e24c4b;
    color: white;
    border: none;
    border-radius: 10px;
    transition: background-color 0.3s;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
}
div.stButton > button:hover {
    background-color: #c03d3c;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Leer código desde URL
params = st.query_params
comision = params.get("curso", "sin_codigo")

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credenciales_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key("1440OXxY-2bw7NAFr01hGeiVYrbHu_G47u9IIoLfaAjM")

# Obtener nombre de actividad desde hoja "comisiones"
hoja_comisiones = sheet.worksheet("comisiones")
df_comisiones = pd.DataFrame(hoja_comisiones.get_all_records())
nombre_actividad = df_comisiones.loc[df_comisiones["comision"] == comision, "nombre_actividad"].values
nombre_actividad = nombre_actividad[0] if len(nombre_actividad) > 0 else "Actividad sin nombre"

st.title(f"📝 Encuesta de Opinión - {nombre_actividad}")
#st.markdown(f"**Código de comisión detectado:** `{comision}`")

# Mostrar formulario
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
    aprendizajes_adquiridos = st.text_area(
        "aprendizajes", 
        placeholder="Escribí aquí...", 
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("##### 💬 COMENTARIOS O SUGERENCIAS QUE PUEDAN RESULTAR ÚTILES PARA FUTURAS CAPACITACIONES (OPCIONAL)")
    comentarios = st.text_area(
        "comentarios", 
        placeholder="Escribí aquí...", 
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📤 ENVIAR RESPUESTA"):
        if not all([conocimientos_previos, valoracion_curso, conocimientos_aplicables, valoracion_docente, aprendizajes_adquiridos]):
            st.warning("⚠️ Por favor, completá todas las preguntas obligatorias antes de enviar.")
        else:
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

else:
    st.success("✅ ¡Gracias! Tu opinión fue enviada correctamente.")
