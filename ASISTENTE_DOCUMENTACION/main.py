from backend.Core import run_llm
import streamlit as st

from streamlit_chat import message
image_url = 'https://steamuserimages-a.akamaihd.net/ugc/1834670776883523989/E0C3A59F049D1958C15A9E475A5CF2941F02BEC4/?imw=637&imh=358&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true'

# Aplicar estilo personalizado para ajustar la imagen como cover
st.markdown(f"""
    <style>
    .full-width-image {{
        background-image: url('{image_url}');
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 200px; /* Ajusta la altura según lo que prefieras */
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    </style>
    <div class="full-width-image"></div>
""", unsafe_allow_html=True)
st.title("ALL TOMORROWS BESTIARY")
st.subheader('What is All Tomorrows')
st.write("<p style='font-size:17px;'>All Tomorrows: A Billion Year Chronicle of the Myriad Species and Mixed Fortunes of Man is a 2006 work of science fiction and speculative evolution written and illustrated by the Turkish artist C. M. Kosemen under the pen name Nemo Ramjet. It explores a hypothetical future path of human evolution set from the near future to a billion years from the present. Several future human species evolve through natural means and through genetic engineering, conducted by both humans themselves and by a mysterious and superior alien species called the Qu.</span>", unsafe_allow_html=True)

st.subheader('Select a post human or specie in this universe')

images = [
    'https://static.miraheze.org/intercriaturaswiki/thumb/c/cc/Marcianos_americanos_por_Nemo_Ramjet.jpg/424px-Marcianos_americanos_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/d/d3/Pre-Humano_Estelar_por_Nemo_Ramjet.jpg/424px-Pre-Humano_Estelar_por_Nemo_Ramjet.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8Kio7zUNn8u2yM3qLEWWu8iiSyF-NbFKj9A&s',
    'https://static.miraheze.org/intercriaturaswiki/thumb/2/28/Gusanos_por_Nemo_Ramjet.jpg/450px-Gusanos_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/f/fe/Titanes_por_Nemo_Ramjet.jpg/300px-Titanes_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/e/e3/Nadadores_por_Nemo_Ramjet.jpg/300px-Nadadores_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/3/3f/Tentados_por_Nemo_Ramjet.jpg/300px-Tentados_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/1/11/Coloniales_por_Nemo_Ramjet.jpg/300px-Coloniales_por_Nemo_Ramjet.jpg',
    'https://static.miraheze.org/intercriaturaswiki/thumb/a/aa/Ladeados_por_Nemo_Ramjet.jpg/300px-Ladeados_por_Nemo_Ramjet.jpg'
]

names = [
    'The Martians',
    'The Star People',
    'The Qus',
    'The Worms',
    'The Titans',
    'The Swimers',
    'The Temptors',
    'Colonial',
    'The Lopsider'
]

responses = [
    'What are The Martians in all tomorrows'
]

# Estilos para las imágenes
st.markdown("""
    <style>
        .image-cover {
            width: 100%;
            height: 200px;
            background-size: cover;
            background-position: center;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Calcular cuántas filas necesitamos para mostrar todas las imágenes (3 columnas por fila)
num_columns = 3
num_rows = (len(images) + num_columns - 1) // num_columns  # Esto asegura que se agregue una fila adicional si es necesario
prompt = st.text_input("Prompt", placeholder = "Enter your prompt here")

# Recorrer las filas
for row in range(num_rows):
    # Crear una fila de 3 columnas
    cols = st.columns(num_columns)
    
    # Recorrer las columnas y asignar imágenes y botones
    for col in range(num_columns):
        index = row * num_columns + col
        if index < len(images):  # Asegura que no haya índice fuera de rango
            with cols[col]:
                st.markdown(f'<div class="image-cover" style="background-image: url({images[index]});"></div>', unsafe_allow_html=True)
                if st.button(f"{names[index]}"):
                    prompt = 'What are The Martians in all tomorrows'



if (
    "chat_anwers_history" not in st.session_state and
    "user_prompt_history" not in st.session_state and
    "chat_history" not in st.session_state
):
    st.session_state["chat_anwers_history"]= []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

def create_sources_string(source_urls: set[str])->str:
    if not source_urls:
        return ""
    source_list = list(source_urls)
    source_list.sort()
    source_string="sources:\n"

    for i , source in enumerate(source_list):
        source_string += f"{i+1}.{source}\n"
    return source_string

if prompt:
    with st.spinner("Generating responde"):
        generated_responde = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"]
        )
        #en el fronted vamos a mostrar la respuesta, y otro es los lugares de donde los saco o links
        sources = set([doc.metadata["source"] for doc in generated_responde["source"]])
        formated_responde = f"{generated_responde['result']}\n\n{create_sources_string(sources)}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_anwers_history"].append(formated_responde)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_responde["result"]))

    if st.session_state["chat_anwers_history"]:
        for i, (generated_responde, user_query) in enumerate(
                zip(st.session_state["chat_anwers_history"], st.session_state["user_prompt_history"])):
            message(user_query, is_user=True, key=f"user_{i}")
            message(generated_responde, key=f"bot_{i}")










