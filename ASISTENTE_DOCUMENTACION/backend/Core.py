import os
from tabnanny import verbose
from typing import Any, Dict, List
from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
#es la que nos va a servir para poder guardar historial con el LLm
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain

from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from openai import embeddings

from pinecone import Pinecone
#no sirve para poder hacer el enlace con nuestro IA agent
from langchain_community.vectorstores import Pinecone as PineconeLangChain

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#se pide el historial y con cada consulta se va a ir actualizando
def run_llm(query: str, chat_history:List[Dict[str, Any]]) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(
        index_name=os.getenv("INDEX_NAME"),
        embedding=embeddings
    )
    #con temperature le decimos que sea 0 creativo
    chat =ChatOpenAI(verbose=True, temperature=0)

    #es de un modelo ya existente
    retrieval_qa_promt_ = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(
        chat, retrieval_qa_promt_
    )

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    #creamos un objeto que va a servir como retriever
    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )

    #vamos a unirlo todo en una sola chain
    qa = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input":query,"chat_history": chat_history})
    #este resultado va a ser tipo diccionario, con input, answer y context

    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source":result["context"]
    }
    return new_result


if __name__ == "__main__":
    print(run_llm(query="What is a Chain in LangChain?"))



