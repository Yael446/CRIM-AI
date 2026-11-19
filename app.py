print("Bienvenido a CRIM-AI")
print("Sistema de investigación criminológica iniciado")
import streamlit as st
import requests

# Configuración de CRIM-AI
st.set_page_config(
    page_title="CRIM-AI",
    page_icon="🔎"
)

st.title("🔎 CRIM-AI")
st.subheader("Sistema de investigación criminológica")

st.write("Asistente de inteligencia artificial para el análisis de casos.")

# Configuración del modelo
MODELO = "qwen2.5:3b"
URL = "http://localhost:11434/api/chat"

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
                respuesta = requests.post(
                    URL,
                    json={
                        "model": MODELO,
                        "messages": [
                            {
                                "role": "system",
                                "content": INSTRUCCIONES
                            },
                            *st.session_state.mensajes
                        ],
                        "stream": False
                    },
                    timeout=180
                )

                respuesta.raise_for_status()
                texto = respuesta.json()["message"]["content"]
                st.write(texto)

                st.session_state.mensajes.append({
                    "role": "assistant",
                    "content": texto
                })

            except requests.exceptions.RequestException as error:
                st.error(f"No pude conectar con Ollama: {error}")
