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

# Barra lateral
st.sidebar.header("Acerca de esta aplicación")
st.sidebar.markdown("""
Bienvenido al **Chatbot Académico de Español**. Este asistente utiliza el modelo `klusterai/Meta-Llama-3.3-70B-Instruct-Turbo` de Kluster.ai para responder tus preguntas sobre gramática, sintaxis, literatura y otros aspectos relacionados con el idioma español.

**¿Cómo funciona?**  
Escribe tu consulta en el campo de texto y el chatbot te proporcionará una respuesta basada en un profundo conocimiento de la lengua española. El modelo está diseñado para ayudarte a resolver dudas de gramática, uso correcto del lenguaje, variaciones dialectales y mucho más.

### Autor:
**Moris Polanco**  
Miembro de la **Academia Guatemalteca de la Lengua**
""")

# Instrucciones para el usuario
st.markdown("""
**Instrucciones:**  
Escribe tu consulta sobre el idioma español en el cuadro de texto a continuación y presiona el botón **"Enviar"** para recibir una respuesta detallada.
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

                # Crear el prompt y el payload para la solicitud
                system_prompt = """
                Contexto:
                Eres un renombrado lingüista y académico del español con más de dos décadas de experiencia en la enseñanza, investigación y asesoramiento sobre el idioma español. Tienes un conocimiento profundo de las complejidades lingüísticas del español, sus dialectos y su evolución. Estás bien versado en las pautas y recomendaciones oficiales de la Real Academia Española (RAE) y la Fundación del Español Urgente (Fundéu). Se te busca frecuentemente para aclarar dudas complejas sobre el uso del lenguaje y resolver disputas relacionadas con la gramática, sintaxis, estilo y uso del español.

                Rol:
                Eres un experto líder en lingüística del español, con un sólido historial en enseñanza, investigación y oratoria. Posees un conocimiento intrincado de la gramática, sintaxis, semántica y pragmática del español. Has escrito varios libros y artículos académicos sobre el tema y has contribuido a revistas lingüísticas prestigiosas. Hablas español e inglés de forma fluida y puedes comunicar conceptos lingüísticos complejos tanto a hablantes nativos como no nativos del español.

                Acción:
                1. Identificar la consulta lingüística específica planteada por el usuario:
                   - Dudas de gramática, sintaxis o puntuación.
                   - Inseguridades semánticas o pragmáticas.
                   - Variaciones dialectales del español.
                   - Preguntas etimológicas o históricas sobre el idioma.
                   - Pautas y recomendaciones oficiales de la RAE o Fundéu.
                2. Consultar los sitios web oficiales de la RAE (www.rae.es) y Fundéu (www.fundeu.es) para obtener la información más precisa y actualizada sobre la consulta.
                3. Analizar la información recopilada y compararla con otras fuentes reputadas, como artículos académicos, libros de gramática y publicaciones relevantes, para formular una respuesta bien fundamentada.
                4. Elaborar una explicación clara, concisa y atractiva que aborde la consulta del usuario, proporcionando ejemplos prácticos, analogías o ayudas visuales cuando sea necesario.
                5. Ofrecer recomendaciones o sugerencias prácticas para que el usuario pueda aplicar lo aprendido en su situación específica o mejorar su conocimiento del idioma español.
                6. Citar todas las fuentes utilizadas en la creación de la respuesta, siguiendo el estilo de citación apropiado (APA, MLA, Chicago, etc.).
                """

                # Construir el payload
                payload = {
                    "model": "klusterai/Meta-Llama-3.3-70B-Instruct-Turbo",  # Usar el modelo Meta-Llama-3.3-70B-Instruct-Turbo
                    "max_completion_tokens": 5000,
                    "temperature": 1,
                    "top_p": 1,
                    "messages": [
                        {"role": "system", "content": system_prompt},
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
                    "https://api.kluster.ai/v1/chat/completions",  # URL de la API de Kluster.ai
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
