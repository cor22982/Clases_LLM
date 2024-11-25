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
import datetime
import os

load_dotenv()
def save_history(question, answer):
    with open("history.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}|{question}|{answer}\n")


def load_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            return f.readlines()
    return []

def interfaz ():
    st.set_page_config(page_title="Proyecto 2",
                       layout= "wide")
    st.title("Proyecto 2 ")
    #agente python

    instrucciones = """
           - You are a agent design to write and execute Python code to answer questions
           - You have access to a python REPL, wich you can use to execute python code
           - If you get and error , debug your code and try again
           - You have qr code package installed
           - You have matplotlib package installed
           - You have pandas package installed
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
            description="""Useful when you need to answer questions over solar.csv file and eclipse solars,
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
        with st.spinner("Generating responde"):
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

    try:
        with open("history.txt", "r", encoding="latin-1") as file:
            lines = file.readlines()
    except FileNotFoundError:
        st.error("El archivo 'historial.txt' no se encuentra.")
        lines = []
    st.subheader("Historial de conversaciones")
    # Procesa y muestra cada línea
    if lines:
        for line in lines:
            # Divide la línea en fecha, pregunta y respuesta
            try:
                datetime, question, answer = line.strip().split("|", 2)
                st.markdown("---")
                st.markdown(f"**Fecha y hora:** {datetime}")
                st.markdown(f"**Pregunta:** {question}")
                st.markdown(f"**Respuesta:** {answer}")

            except ValueError:
                st.warning(f"Formato incorrecto en la línea: {line}")
    else:
        st.info("No hay datos disponibles para mostrar.")
    st.subheader("Preguntale al LLM")
    prompt = st.text_input("Pregunta", placeholder="Aqui haz tus preguntas de los csv")

    if st.button("Preguntar sobre CSV"):
        with st.spinner("Generating responde"):
            try:
                respuesta = grand_agent_executor.invoke(
                    {
                        "input": prompt

                    }
                )
                st.markdown("### Respuesta del agente")
                st.success(respuesta["output"])
                save_history(prompt, respuesta["output"])
            except ValueError as e:
                st.error(f"Error en el agent: {str(e)}")


if __name__=="__main__":
    interfaz()