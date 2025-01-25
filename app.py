import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Académico de Español",
    page_icon="🗨️",
    layout="wide",
)

# Título de la aplicación
st.title("🗨️ Chatbot Académico de Español")

# Instrucciones para el usuario
st.markdown("""
Bienvenido al **Chatbot Académico de Español**. Este asistente utiliza la API de OpenRouter para resolver tus dudas sobre el idioma español. Realiza consultas sobre gramática, sintaxis, variaciones regionales y más.
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
                api_key = st.secrets["openrouter"]["api_key"]

                # Definir el prompt inicial
                system_prompt = """
You are a renowned academic specializing in the Spanish language, with over two decades of experience in linguistics, grammar, and literary analysis. Your expertise is sought to resolve complex queries related to the Spanish language, providing clear and authoritative insights. You have a deep understanding of the nuances of the language, its regional variations, and its historical evolution. Your role involves not only explaining the correct usage but also illustrating common mistakes and their corrections.
"""

                # Crear el payload para la API
                payload = {
                    "model": "deepseek/deepseek-r1",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ]
                }

                # Definir los encabezados de la solicitud
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                # Realizar la solicitud a la API de OpenRouter
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )

                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    response_data = response.json()
                    chatbot_reply = response_data["choices"][0]["message"]["content"]
                    st.success("Respuesta del chatbot:")
                    st.markdown(f"```\n{chatbot_reply}\n```")
                else:
                    st.error(f"Error en la solicitud: {response.status_code}")
                    st.error(f"Detalles: {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# Mensaje adicional
st.markdown("""
---
*Este chatbot utiliza la API de OpenRouter para procesar las consultas. Asegúrate de que tu clave de API esté configurada correctamente en los secretos de Streamlit.*
""")
