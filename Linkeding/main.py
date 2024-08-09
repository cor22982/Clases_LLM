from langchain.chains.llm import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import PipelinePromptTemplate
from third_partys.linting import  scrape_linkeding_profile
#ahora vamos a importar la libreria que nos va a ayudar para crear ese chat con open ia
from langchain_openai import ChatOpenAI
#luego tenemos que importar la libereria que nos va a servir para poder tomar las api key
from dotenv import load_dotenv
import os #manejo de las request, o tener funciones del sistema operativo.

#DESCRIPCION
#TOmarme cierta informaicon que yo le pongo a el codigo, y va a hacer que se le pida a
#CHATPGT y que haga un resumen de esa biografia y que le de datos interesantes de esa biografica

#Esta es la autobiografia


if __name__ == "__main__":
    informacion = "linkeding_data"
    load_dotenv()  # vamos a cargar las variables de ambiente que tengamos.
    summary_template = """
    Given the information of {informacion} about that pearson I want to create: 
        1. A little summary
        2. Two intersting facts about him.
    """

    # crearemos nuestro objeto promt template. Esa nos iba a servir par el esquema del prompt

    summary_template_prompt = PromptTemplate(
        input_variables=[informacion],
        template=summary_template
    )

    # ahora vamos a crear nuestro objeto que es el chatgpt y vamos a agregar nuestro llm

    # la temperatura es una variable que indica que tan creativa es la respuesta.
    # Que tan creativa es la respuesta.
    # La temperatura va de 0 a 1.

    # Los steps lo que hacen es varias consultas a la inteligencia aritficial para iterar sobre una misa respuesta
    # Es otra forma de hacer few shoots prompting.

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # creamos una chain y metemos el promt y el llm
    chain = LLMChain(llm=llm, prompt = summary_template_prompt)
    linkeding_data = scrape_linkeding_profile(
        lining_profile_url="https://gist.githubusercontent.com/rogerdiaz/2d10d662484e892c83106b749b6b8d27/raw/316ff86d46bf2da7b0fa00b8ac149ebe38d894b3/roger-diaz.json",
        mock=False)
    # ahora creamos nuestra consulta
    # le estoy diciento que informacion sea la variable de entrada. a GPT.
    res = chain.invoke(input={"informacion": linkeding_data})
    print(res['text'])

