#Este es el ejercicio 3 de la clase de 9 de Agosto

#Este es un ejemplo con agentes. Este es un programa al que le damos un nombre y un apellido
#y gracias al uso de agentes y tools vamos a poder dejar que el LLM vaya  y busque el perfil
#Y nos regrese el URL

#funciones sistema operativo
import os
#variables de entorno
from dotenv import load_dotenv
load_dotenv()
#ayuda a crear nuestro LLM
from langchain_openai import ChatOpenAI
#crea un template del prompt que se le manda al LLM
from langchain.prompts.prompt import PromptTemplate
from Tools.tools import get_profile_url_tavily
#libreria para las tools y son funciones que communican al LLM con el exterior
from langchain_core.tools import Tool

#importar para los agents
from langchain.agents import (
    # y ese es ya un tipo de agente el react agent.
    create_react_agent,
    AgentExecutor, #este es un framework para correr.
)

# nos rive par aque podamos tomar diferentes prompts que ya estan hechos por la comunidad
from langchain import hub

def lookup (name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name = "gpt-3.5-turbo",
    )
    #pedido a chatgpt que queremos
    template = """
        given the full name {name_of_pearson} I want you to get me a link to their Linkedin 
        profile page. 
            Your answer should contain only a URL."""
    prompt_template = PromptTemplate(
        template=template, #el template
        input_variable=["name_of_pearson"] #la variable de entrada
    )

    #coontenedor con las tools que nuestro agente va a usar

    tools_for_agent = [
        Tool(
            name = "Crawl Google 4 Linkedin profile page",
            func = get_profile_url_tavily,
            description = "useful when you need to get a Linkedin page URL",
        )]
    # otra parte que necesitan es una apllicacion de reazomamiento.
    # para eso ya hay agents precreados
    react_promt = hub.pull("hwchase17/react") #es el perfil de quien creo lanchain
    #este es el agent
    #con ese react prompt le diremos que use el react model
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_promt)

    #runtime para ejecutar el agente
    #verbose es para visualizar el proceso de razonamiento
    agent_executor = AgentExecutor(agent=agent,
                                   tools=tools_for_agent,
                                   verbose=True)
    result = agent_executor.invoke(
        input= {"input": prompt_template.format_prompt(name_of_pearson=name)}
    )
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Mathew Cordero Técnico en electrónica")
    print(linkedin_url)