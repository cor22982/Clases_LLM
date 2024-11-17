from turtledemo.sorting_animate import instructions2

from Scripts.pywin32_postinstall import verbose
from dotenv import load_dotenv
from langchain import hub
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor

# Esto lo que hace es generar un agente python para generar codigo automaticamente
from langchain_experimental.tools import PythonREPLTool

load_dotenv()
def main():
    print("Start ....")

    instrucciones = """
        - You are a agent design to write and execute Python code to answer questions
        - You have access to a python REPL, wich you can use to execute python code
        - If you get and error , debug your code and try again
        - Only use the output of your code to answer the question.
        - You might know the answer without running the code , but you should still run the code to get the answer.
        - If it does not seem like you can write code to answer the question, just return "Sorry, I don´t know" as the answer
    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instrucciones)
    tools = [PythonREPLTool()]

    agent = create_react_agent(prompt=prompt,
                               llm=ChatOpenAI(temperature=0,model="gpt-4-turbo"),
                               tools=tools)

    # necesitamos el running time para ejecutar el agente
    agent_exexutor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_exexutor.invoke(
        input={
            "input":""""generate and save in current working directory 2 qr codes that point to https://www.youtube.com/watch?v=dQw4w9WgXcQ you have qrcode package intalled already"""
        }
    )



if __name__== "__main__":
    main()


