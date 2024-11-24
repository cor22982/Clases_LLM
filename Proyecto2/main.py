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


load_dotenv()

def interfaz ():
    st.set_page_config(page_title="Proyecto 2",
                       layout= "wide")
    st.title("Proyecto 2 ")


if __name__=="__main__":
    interfaz()