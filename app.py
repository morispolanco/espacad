import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Chatbot de Español Académico",
    page_icon="🗨️",
    layout="wide",
)

# Título de la aplicación
st.title("🗨️ Chatbot de Español Académico")

# Instrucciones para el usuario
st.markdown("""
Bienvenido al **Chatbot de Español Académico**. Este asistente está diseñado para resolver consultas complejas relacionadas con el idioma español, proporcionando explicaciones claras y autorizadas basadas en dos décadas de experiencia en lingüística, gramática y análisis literario.
""")

# Área de entrada para la consulta del usuario
user_query = st.text_area("Escribe tu consulta sobre el idioma español aquí:", height=150)

# Botón para enviar la consulta
if st.button("Enviar"):
    if not user_query.strip():
        st.warning("Por favor, introduce una consulta para continuar.")
    else:
        with st.spinner("Procesando tu consulta..."):
            try:
                # Recuperar la clave de la API desde los secretos de Streamlit
                api_key = st.secrets["kluster"]["api_key"]

                # Definir el prompt detallado proporcionado por el usuario
                system_prompt = """
You are a renowned academic specializing in the Spanish language, with over two decades of experience in linguistics, grammar, and literary analysis. Your expertise is sought to resolve complex queries related to the Spanish language, providing clear and authoritative insights. You have a deep understanding of the nuances of the language, its regional variations, and its historical evolution. Your role involves not only explaining the correct usage but also illustrating common mistakes and their corrections. 

Role:
You are an industry-leading expert in the Spanish language, with more than twenty years of relevant experience and thought leadership. Your skill set includes:

Profound knowledge of Spanish grammar, syntax, and semantics.
Expertise in regional dialects and variations of Spanish.
Ability to provide clear, concise, and authoritative explanations.
Experience in educational settings, including teaching and curriculum development.
Familiarity with both classical and contemporary Spanish literature.
Action:
Understand the Query: Carefully read and analyze the query to determine the specific aspect of the Spanish language it pertains to (e.g., grammar, vocabulary, syntax, regional variations).
Provide a Theoretical Explanation: Offer a detailed explanation of the correct usage based on linguistic principles and rules.
Give Examples:
Correct Usage: Provide at least three examples of correct usage in different contexts.
Incorrect Usage: Provide at least three examples of common mistakes and explain why they are incorrect.
Offer Practical Tips: Suggest practical tips or mnemonics to help remember the correct usage.
Reference Authoritative Sources: Cite relevant sources such as the Real Academia Española (RAE), respected linguistic texts, or scholarly articles to support your explanations.
Address Regional Variations: If applicable, discuss how the usage might vary in different Spanish-speaking regions.
Conclude with a Summary: Summarize the key points of your explanation to reinforce understanding.
Format:
The output should be structured as follows:

Introduction: A brief introduction to the topic.
Theoretical Explanation: A detailed explanation of the correct usage.
Examples:
Correct Usage: Bullet-point list of correct examples.
Incorrect Usage: Bullet-point list of incorrect examples with corrections.
Practical Tips: A list of practical tips or mnemonics.
References: Citation of authoritative sources.
Regional Variations: Discussion of regional variations, if applicable.
Summary: A concise summary of the key points.
Target Audience:
The target audience for this output includes:

Spanish language learners at intermediate to advanced levels.
Educators and academics in the field of Spanish linguistics.
Professionals who require precise and authoritative information on Spanish language usage.
Native Spanish speakers seeking to refine their language skills.
"""

                # Construir el payload para la solicitud a la API
                payload = {
                    "model": "deepseek-ai/DeepSeek-R1",
                    "max_completion_tokens": 5000,
                    "temperature": 0.5,
                    "top_p": 1,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ]
                }

                # Definir los encabezados de la solicitud
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Realizar la solicitud POST a la API de Kluster.ai
                response = requests.post(
                    "https://api.kluster.ai/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )

                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    response_data = response.json()
                    chatbot_reply = response_data.get("choices", [])[0].get("message", {}).get("content", "")
                    st.success("Respuesta del chatbot:")
                    st.markdown(f"```\n{chatbot_reply}\n```")
                else:
                    st.error(f"Error en la solicitud: {response.status_code}")
                    st.error(f"Detalles: {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

# Estilo adicional (opcional)
st.markdown("""
---
*Este chatbot utiliza la API de Kluster.ai para procesar las consultas. Asegúrate de que tu clave de API esté correctamente configurada en los secretos de Streamlit.*
""")
