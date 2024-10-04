import os
from typing import Any
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

#Es practicamente para hacer el asistente. Un retrieval es un chat que se abre con un
# LLM con el que podemos guardar en memoria y manejar un historial con el chat
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

def run_llm(query:str) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(
        index_name=os.getenv('INDEX_NAME'),
        embedding=embeddings
    )
    chat = ChatOpenAI(verbose=True, temperature=0)
    # stuff es tomar el contexto y pegarlos a la pregunta
    qa = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True
    )
    return qa.invoke({"query": query})

if __name__ == "__main__":
    print(run_llm(query="What is LangChain?"))
