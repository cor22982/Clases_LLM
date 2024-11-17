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

load_dotenv()

def main():
    print("Start...")
    instrucciones = """
            - You are a agent design to write and execute Python code to answer questions
            - You have access to a python REPL, wich you can use to execute python code
            - If you get and error , debug your code and try again
            - You have qr code package installed
            - Only use the output of your code to answer the question.
            - You might know the answer without running the code , but you should still run the code to get the answer.
            - If it does not seem like you can write code to answer the question, just return "Sorry, I don´t know" as the answer
    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instrucciones)
    tools = [PythonREPLTool()]
    python_agent = create_react_agent(prompt=prompt,
                               llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
                               tools=tools)
    python_agent_exexutor = AgentExecutor(agent=python_agent, tools=tools, verbose=True)


    csv_agent_executor: AgentExecutor = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4"),
        path="episode_info.csv",
        verbose=True,
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
            name="CSV Agent",
            func=csv_agent_executor.invoke,
            description="""Useful when you need to answer questions over episode_info.csv file,
            taken and input the entire question and returns the answer after running pandas calculations"""
        )
    ]

    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=  ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools_react
    )
    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=tools_react,
        verbose=True
    )

    print(grand_agent_executor.invoke(
        {
            "input": """Generate and save in current working directory 1 qr code that point to https://www.youtube.com/watch?v=Z3J_MCbwaJ0"""

        }
    ))


if __name__ == "__main__":
    main()