import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import pandas as pd
import json

st.set_page_config(page_title="Encuesta de Capacitación", layout="centered")

st.markdown("""
    <style>
    /* Aumentar tamaño del texto en radio buttons */
    .stRadio > div {
        gap: 1rem;
    }

    .stRadio label {
        font-size: 1.3rem !important;
        line-height: 2;
        display: flex;
        align-items: center;
    }

    /* Aumentar tamaño del círculo (radio bullet) */
    .stRadio input[type="radio"] {
        width: 1.3rem;
        height: 1.3rem;
        margin-right: 0.6rem;
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
st.markdown(f"**Código de comisión detectado:** `{comision}`")

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

    st.markdown("##### 💬 COMENTARIOS O SUGERENCIAS QUE PUEDAN RESULTAR ÚTILES PARA FUTURAS CAPACITACIONES (OPCIONAL)")
    comentarios = st.text_area(
        "comentarios", 
        placeholder="Escribí aquí...", 
        label_visibility="collapsed"
    )

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
