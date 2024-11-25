from turtledemo.sorting_animate import instructions1
from typing import Any, Dict

from Scripts.pywin32_postinstall import verbose
from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import streamlit as st
from streamlit_chat import message

load_dotenv()

def interfaz ():
    st.set_page_config(page_title="Proyecto 2",
                       layout= "wide")
    st.title("Proyecto 2 ")
    #agente python

    instrucciones = """
           - You are a agent design to write and execute Python code to answer questions
           - You have access to a python REPL, wich you can use to execute python code
           - If you get and error , debug your code and try again
           - Only use the output of your code to answer the question.
           - You might know the answer without running the code , but you should still run the code to get the answer.
           - If it does not seem like you can write code to answer the question, just return "Sorry, I don´t know" as the answer
       """


    st.subheader("Agente Python")
    st.write(
        "<p style='font-size:17px;'>Esta parte del agente realiza trabajos usando python</span>",
        unsafe_allow_html=True)
    ejemplos = [
        "Crea un juego basico de pong en pygame, dame solo el codigo",
        "Genera una grafica gaussiana en Matplotlib y luego guarda la grafica como jpg en este directorio , tambien dame el codigo que usaste",
        "Del archivo breaking-bad.csv obten las temporadas (Season) y en una grafica contrastalas con sus us-viewers usa Matplotlib y luego guarda la grafica como jpg en este directorio , tambien dame el codigo que usaste"
    ]

    example = st.selectbox("Seleccione un ejemplo", ejemplos)

    # Agentes

    #Agente Python
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instrucciones)
    tools = [PythonREPLTool()]
    python_agent = create_react_agent(prompt=prompt,
                                      llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
                                      tools=tools)
    python_agent_exexutor = AgentExecutor(agent=python_agent, tools=tools, verbose=True)

    #ejecutor para breaking bad
    csv_agent_executor_bb: AgentExecutor = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4"),
        path="breaking-bad.csv",
        verbose=True,
        encoding='utf-8',
        allow_dangerous_code=True
    )
    #ejecutor para mario
    csv_agent_executor_mario: AgentExecutor = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4"),
        path="mario64_speedruns.csv",
        verbose=True,
        encoding='utf-8',
        allow_dangerous_code=True
    )
    # ejecutor para solar
    csv_agent_executor_solar: AgentExecutor = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4"),
        path="solar.csv",
        verbose=True,
        encoding='utf-8',
        allow_dangerous_code=True
    )
    # ejecutor para exoplanets
    csv_agent_executor_exoplanets: AgentExecutor = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4"),
        path="all_exoplanets_2021.csv",
        verbose=True,
        encoding='utf-8',
        allow_dangerous_code=True
    )

    def python_Agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_exexutor.invoke(
            {"input": original_prompt}
        )

    tools_react = [
        Tool(
            name="Python Agent",
            func=python_Agent_executor_wrapper,
            description="""
                   useful when you need to transform natural language
                   to python and execute python code, returning the results of the code execution
                   DOES NOT ACCEPT CODE AS INPUT
               """
        ),
        Tool(
            name="CSV Agent Breaking Bad",
            func=csv_agent_executor_bb.invoke,
            description="""Useful when you need to answer questions over breaking-bad.csv file in breaking bad context,
               taken and input the entire question and returns the answer after running pandas calculations"""
        )
        ,
        Tool(
            name="CSV Agent Spedruns Mario",
            func=csv_agent_executor_mario.invoke,
            description="""Useful when you need to answer questions over mario64_speedruns.csv.csv file,
                   taken and input the entire question and returns the answer after running pandas calculations"""
        ),
        Tool(
            name="CSV Agent Eclipse Solar",
            func=csv_agent_executor_solar.invoke,
            description="""Useful when you need to answer questions over solar.csv file,
                   taken and input the entire question and returns the answer after running pandas calculations"""
        ),
        Tool(
            name="CSV Agent All Exoplanets",
            func=csv_agent_executor_exoplanets.invoke,
            description="""Useful when you need to answer questions over all_exoplanets_2021.csv file,
                   taken and input the entire question and returns the answer after running pandas calculations"""
        )
    ]
    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools_react
    )
    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=tools_react,
        verbose=True
    )
    if st.button("Ejecutar accion"):
        user_input = example
        try:
            respuesta = grand_agent_executor.invoke(
                {
                    "input": user_input

                }
            )
            st.markdown("### Respuesta del agente")
            st.code(respuesta["output"], language="python")
        except ValueError as e:
            st.error(f"Error en el agent: {str(e)}")

    #agente csv



    images = [
        'https://es.web.img3.acsta.net/pictures/18/04/04/22/52/3191575.jpg',
        'https://media.es.wired.com/photos/65c67d27c50373eaab81e70b/4:3/w_2664,h_1998,c_limit/exoplanetas%20habitables.jpg',
        'https://www.enter.co/wp-content/uploads/2013/11/Supermario-64.jpg',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcy31Tofx03h1xKvB7guX06-rZN0hRBXMeQg&s',
    ]

    names = [
        'Breaking Bad',
        'Exoplanetas',
        'Speedrun Mario 64',
        'Elipses Solares',
    ]

    st.subheader("Agente CSV")
    st.write(
        "<p style='font-size:17px;'>Esta parte del agente responde preguntas en base a varios csv que tratan sobre los siguientes temas:</span>",
        unsafe_allow_html=True)

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
    num_columns = 3
    num_rows = (len(images) + num_columns - 1) // num_columns

    for row in range(num_rows):
        # Crear una fila de 3 columnas
        cols = st.columns(num_columns)

        # Recorrer las columnas y asignar imágenes y botones
        for col in range(num_columns):
            index = row * num_columns + col
            if index < len(images):  # Asegura que no haya índice fuera de rango
                with cols[col]:
                    st.markdown(f'<div class="image-cover" style="background-image: url({images[index]});"></div>',
                                unsafe_allow_html=True)
                    st.text(f"{names[index]}")
    prompt = st.text_input("Pregunta", placeholder="Aqui haz tus preguntas de los csv")

    if (
            "chat_anwers_history" not in st.session_state and
            "user_prompt_history" not in st.session_state and
            "chat_history" not in st.session_state
    ):
        st.session_state["chat_anwers_history"] = []
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_history"] = []

    def create_sources_string(source_urls: set[str]) -> str:
        if not source_urls:
            return ""
        source_list = list(source_urls)
        source_list.sort()
        source_string = "sources:\n"

        for i, source in enumerate(source_list):
            source_string += f"{i + 1}.{source}\n"
        return source_string

    if st.button("Preguntar sobre CSV"):
        with st.spinner("Generating responde"):
            generated_responde = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history"]
            )
            # en el fronted vamos a mostrar la respuesta, y otro es los lugares de donde los saco o links
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


if __name__=="__main__":
    interfaz()