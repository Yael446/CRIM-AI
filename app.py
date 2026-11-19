
import streamlit as st
from google import genai

# Configuración de CRIM-AI
st.set_page_config(
    page_title="CRIM-AI",
    page_icon="🔎"
)

st.title("🔎 CRIM-AI")
st.subheader("Sistema de investigación criminológica")

st.write("Asistente de inteligencia artificial para el análisis de casos.")

# Configuración de Gemini
MODELO = "gemini-3.8-flash"

# Instrucciones de la IA
INSTRUCCIONES = """
Eres CRIM-AI, un asistente especializado en criminología.

Ayudas a organizar expedientes, analizar casos documentados
y estudiar investigaciones criminológicas.

Distingue siempre entre:
- Hechos documentados.
- Testimonios.
- Hipótesis.
- Información desconocida.

No inventes pruebas, confesiones ni información.
No presentes simulaciones como testimonios reales.
No atribuyas pensamientos privados como si fueran hechos.
No emitas diagnósticos clínicos ni afirmes culpabilidad.
Explica las limitaciones de la información disponible.
"""

# Historial de conversación
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar conversación
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.write(mensaje["content"])

# Cuadro para escribir
pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:
    st.session_state.mensajes.append({
        "role": "user",
        "content": pregunta
    })

    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("CRIM-AI está pensando..."):
            try:
                api_key = st.secrets["gemini"]["api_key"]
                cliente = genai.Client(api_key=api_key)

                historial = []

                for mensaje in st.session_state.mensajes:
                    rol = "user" if mensaje["role"] == "user" else "model"

                    historial.append({
                        "role": rol,
                        "parts": [{"text": mensaje["content"]}]
                    })

                respuesta = cliente.models.generate_content(
                    model=MODELO,
                    contents=historial,
                    config={
                        "system_instruction": INSTRUCCIONES
                    }
                )

                texto = respuesta.text

                if not texto:
                    texto = "No recibí una respuesta de Gemini."

                st.write(texto)

                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": texto
                })

            except KeyError:
                st.error("No encuentro la API key. Revisa la configuración de Secrets.")

            except Exception as error:
                st.error(f"Error al conectar con Gemini: {error}")
