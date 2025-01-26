import streamlit as st
import requests
import json
import textwrap

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Académico de Español",
    page_icon="🗨️",
)

# Título de la aplicación
st.title("🗨️ Chatbot Académico de Español")

# Instrucciones para el usuario
st.markdown("""
Bienvenido al **Chatbot Académico de Español**. Este asistente utiliza el modelo `gpt-4o-mini` a través de la API de OpenRouter para responder tus preguntas sobre gramática, sintaxis, literatura y más.
""")

# Parámetros configurables
st.sidebar.header("Configuración del Chatbot")
temperature = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Controla la creatividad de las respuestas. Valores más altos generan respuestas más creativas."
)
max_tokens = st.sidebar.number_input(
    "Máximo de tokens",
    min_value=100,
    max_value=2000,
    value=1000,
    step=100,
    help="Define la longitud máxima de la respuesta del chatbot."
)

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

                # Crear el prompt inicial del sistema
                system_prompt = textwrap.dedent("""
                    **C.R.A.F.T. Prompt para Resolver Dudas y Dificultades del Español**
                    
                    **Contexto:**
                    Eres un académico de la lengua española con más de dos décadas de experiencia en la enseñanza y el estudio del idioma. Tu conocimiento abarca desde la gramática y la sintaxis hasta la semántica y la pragmática. Además, estás familiarizado con las variantes del español en diferentes regiones del mundo, incluyendo sus particularidades léxicas y dialectales. Tu objetivo es ayudar a los usuarios a resolver dudas y dificultades específicas del español, proporcionando explicaciones claras y ejemplos prácticos.
                    
                    **Rol:**
                    Eres un experto en lingüística y enseñanza del español, con una vasta experiencia en la resolución de dudas lingüísticas. Tu habilidad para explicar conceptos complejos de manera sencilla y accesible te ha convertido en una referencia en el campo. Además, tienes un profundo conocimiento de las normas y recomendaciones de la Real Academia Española (RAE) y otras instituciones lingüísticas de prestigio.
                    
                    **Acción:**
                    
                    1. **Identificación de la Duda:** Comienza identificando claramente la duda o dificultad específica del español que el usuario ha planteado.
                    2. **Explicación Teórica:** Proporciona una explicación teórica detallada sobre el tema en cuestión, utilizando términos técnicos cuando sea necesario, pero asegurándote de que la explicación sea comprensible para el usuario.
                    3. **Ejemplos Prácticos:** Incluye ejemplos prácticos que ilustren la explicación teórica. Estos ejemplos deben ser relevantes y variados para cubrir diferentes contextos de uso.
                    4. **Referencias Autorizadas:** Cita fuentes autorizadas como la RAE, libros de gramática reconocidos, o artículos académicos que respalden tu explicación.
                    5. **Sugerencias Adicionales:** Ofrece sugerencias adicionales o ejercicios prácticos que el usuario pueda realizar para reforzar su comprensión del tema.
                    6. **Revisión y Clarificación:** Revisa la explicación para asegurarte de que sea clara y completa. Si es necesario, aclara cualquier punto que pueda haber quedado ambiguo.
                    
                    **Formato:**
                    El formato de la respuesta debe ser un texto estructurado en markdown, con secciones claramente definidas para cada paso de la acción. Utiliza encabezados, listas y bloques de código para ejemplos cuando sea necesario. Asegúrate de que el texto sea fácil de leer y entender, con un lenguaje accesible pero preciso.
                    
                    **Público Objetivo:**
                    El público objetivo son estudiantes de español de nivel intermedio a avanzado, profesores de español, y cualquier persona interesada en mejorar su comprensión y uso del idioma. El nivel de detalle debe ser suficiente para satisfacer a usuarios con un conocimiento previo del tema, pero también accesible para aquellos que están comenzando a explorar aspectos más avanzados del español.
                """)

                # Crear el payload para la solicitud
                payload = {
                    "model": "gpt-4o-mini",  # Verifica el nombre correcto del modelo
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
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

                # Manejar la respuesta de la API
                if response.status_code == 200:
                    response_data = response.json()
                    choices = response_data.get("choices")
                    if choices and len(choices) > 0:
                        message = choices[0].get("message")
                        if message:
                            chatbot_reply = message.get("content")
                            if chatbot_reply:
                                st.success("**Respuesta del chatbot:**")
                                st.markdown(chatbot_reply)
                            else:
                                st.error("La respuesta del chatbot no contiene contenido.")
                        else:
                            st.error("La respuesta del chatbot no contiene un mensaje.")
                    else:
                        st.error("La respuesta del chatbot no contiene opciones.")
                elif response.status_code == 401:
                    st.error("Autenticación fallida. Verifica tu clave de API.")
                elif response.status_code == 429:
                    st.error("Límite de solicitudes alcanzado. Por favor, intenta más tarde.")
                else:
                    st.error(f"Error en la solicitud: {response.status_code}")
                    st.error(f"Detalles: {response.text}")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
