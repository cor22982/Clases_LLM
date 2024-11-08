import os
import streamlit as st
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
import datetime


load_dotenv()

def save_history(question, answer):
    with open("history.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {question}->{answer}\n")


def load_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            return f.readlines()
    return []

def main():
    st.set_page_config(page_title="Agente de Python interactivo",
                       layout= "wide")
    st.title("Agente de python interactivo")

    st.markdown("""
    <style>
    .stApp{background-color:black;}
    .title{color=#ff4b4b;}
    .button{backgorund-color:#ff4b4b; border-radius: 5px;}
    .input{border:1px solid #ff4b4b; border-radius: 5px;}
    </style>
    """)

    instrucciones = """
    - Siempre usa la herramienta , inculso si sabes la respuesta
    - Debes usar codigo de python para responder
    - Eres un agneete puede escribir codigo
    - Solo responde la pregunta escribiendo codigo, inclusi si sabes la respuesta
    - Si no sabes la respuesta escribe No se la respusta
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instrucciones=instrucciones)
    st.write("Prompt cargando...")

    tool = [PythonREPLTool()]
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agente= create_react_agent(
        llm=llm,
        tools=tool,
        prompt=prompt
    )

    agente_executor = AgentExecutor(
        agent=agente,
        tools=tool,
        verbose=True,
        handle_parsing_erros=True
    )
    st.markdown("### Ejemplos:")
    ejemplos = [
        "Clacula la suma de 2 y 3",
        "Genera una lista de 1 al 10",
        "Crea una funcion que calcule el factorial de un numero",
        "Crea un juego basico de snake con pygame",
        "Encuentra los primeros 10 numeros primos"
    ]

    example = st.selectbox("Seleccione un ejemplo",ejemplos)

    if st.button("Ejecutar ejemplo"):
        user_input = example
        try:
            respuesta = agente_executor.invoke(input={"input":user_input, "agent_scratchpad": ""})
            st.markdown("### Respuesta del agente")
            st.code(respuesta["output"],  language="python")
            save_history(user_input, respuesta["output"])
        except ValueError as e:
            st.error(f"Error en el agent: {str(e)}")



if __name__=="__main__":
    main()
