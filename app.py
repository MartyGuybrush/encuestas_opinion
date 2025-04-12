
import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Encuesta de Capacitación", layout="centered")

# Leer código desde URL
params = st.query_params
comision = params.get("curso", "sin_codigo")

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credenciales_google_encuestas.json", scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key("1440OXxY-2bw7NAFr01hGeiVYrbHu_G47u9IIoLfaAjM")

# Obtener nombre de actividad desde la hoja "comisiones"
hoja_comisiones = sheet.worksheet("comisiones")
df_comisiones = pd.DataFrame(hoja_comisiones.get_all_records())

nombre_actividad = df_comisiones.loc[df_comisiones["comision"] == comision, "nombre_actividad"].values
nombre_actividad = nombre_actividad[0] if len(nombre_actividad) > 0 else "Actividad sin nombre"

st.title(f"📝 Encuesta de Opinión - {nombre_actividad}")
st.markdown(f"**Código de comisión detectado:** `{comision}`")

# Si no fue enviado, mostrar el formulario
if "enviado" not in st.session_state or not st.session_state.enviado:
    conocimientos_previos = st.radio(
        "📌 ¿Tenías conocimientos previos sobre los temas desarrollados en este curso?",
        ["CONOCÍA BIEN LOS TEMAS", "TENÍA ALGÚN CONOCIMIENTO", "DESCONOCÍA LOS TEMAS"],
        index=None
    )

    valoracion_curso = st.radio(
        "📊 ¿Cómo calificarías esta capacitación en general?",
        ["EXCELENTE", "MUY BUENA", "BUENA", "REGULAR", "MALA"],
        index=None
    )

    conocimientos_aplicables = st.radio(
        "🧠 ¿Creés que vas a aplicar a tus tareas habituales los conocimientos adquiridos en este curso?",
        ["TOTALMENTE DE ACUERDO", "DE ACUERDO", "PARCIALMENTE DE ACUERDO", "EN DESACUERDO"],
        index=None
    )

    valoracion_docente = st.radio(
        "👨‍🏫 ¿Cómo calificarías el desempeño del/la docente?",
        ["EXCELENTE", "MUY BUENO", "BUENO", "REGULAR", "MALO"],
        index=None
    )

    aprendizajes_adquiridos = st.text_area("💡 Contanos qué aprendizajes adquiriste en esta capacitación.", placeholder="Escribí aquí...")
    comentarios = st.text_area("💬 Comentarios o sugerencias que puedan resultar útiles para futuras capacitaciones (opcional)", placeholder="Escribí aquí...")

    if st.button("📤 Enviar encuesta"):
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

# Mostrar mensaje de éxito si ya se envió
else:
    st.success("✅ ¡Gracias! Tu opinión fue enviada correctamente.")
