import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Académico de Español",
    page_icon="🗨️",
)

# Título de la aplicación
st.title("🗨️ Chatbot Académico de Español")

# Instrucciones para el usuario
st.markdown("""
Bienvenido al **Chatbot Académico de Español**. Este asistente utiliza el modelo `Meta-Llama-3.1-405B-Instruct-Turbo` de Kluster.ai para responder tus preguntas sobre gramática, sintaxis, literatura y más.
""")

# Entrada del usuario
user_query = st.text_area("Escribe tu consulta sobre el idioma español:", height=150)

# Botón para enviar la consulta
if st.button("Enviar"):
    if not user_query.strip():
        st.warning("Por favor, introduce una consulta para continuar.")
    else:
        with st.spinner("Procesando tu consulta..."):
            try:
                # Recuperar la clave de API desde los secretos
                api_key = st.secrets["klusterai"]["api_key"]  # Asegúrate de tener la clave API en secrets

                # Crear el payload para la solicitud
                payload = {
                    "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
                    "max_completion_tokens": 5000,
                    "temperature": 1,
                    "top_p": 1,
                    "messages": [
                        {"role": "system", "content": "Eres un experto en lingüística del español y estás listo para ayudar."},
                        {"role": "user", "content": user_query}
                    ]
                }

                # Definir los encabezados de la solicitud
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Realizar la solicitud a la API de Kluster.ai
                response = requests.post(
                    "https://api.kluster.ai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                # Manejar la respuesta de la API
                if response.status_code == 200:
                    response_data = response.json()
                    message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if message:
                        st.success("**Respuesta del chatbot:**")
                        st.markdown(message)
                    else:
                        st.error("La respuesta del chatbot no contiene contenido.")
                else:
                    st.error(f"Error en la solicitud: {response.status_code}")
                    st.error(f"Detalles: {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
