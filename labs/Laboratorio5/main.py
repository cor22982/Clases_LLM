import os
from dotenv import load_dotenv
#sirve para cargar los pdfs y posteriormente poderlos convertir
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
#ESTO ES una libreria de facebook para que sea este el que indique como se van a guardar
# de estructura vectorial y asi mismo hagamos consulta de esos datos de esta estructura vectorial
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

load_dotenv()


if __name__ == "__main__":
    print("Carga del archivo PDF")
    pdf_path = "2210.03629v3.pdf"
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    print("Dividir el pdf en chunks")

    #dividimos en chunks el text splitter.
    text_splitter = CharacterTextSplitter(
        chunk_size=1000 , chunk_overlap=30, separator="\n"
    )
    docs = text_splitter.split_documents(documents=documents)

    #guardamos los chunks en una base vectorial.
    embeding = OpenAIEmbeddings()
    # pero ahora vamos a crear la variable vectore store y usar el algorimtmo FAISS de Facebook
    vectorStore = FAISS.from_documents(docs , embedding=embeding)

    #vamos a guardar ahora la base de datos dle manera local
    # esto guardandolo en react
    vectorStore.save_local("faiss_index_react")

    #ahora vamos a usar nuestra agente para consultar a nuestro agente de la las cosas sobre la base vectorial
    print("Carga de embedings")
    new_vectorstore = FAISS.load_local(
        "faiss_index_react", embeding,
        allow_dangerous_deserialization=True
    )
    #la ultima variable es una variable de seguridad cuando se hacen cargas de manera local
    #ahorita tenemos que ponerla en true para hacer una correcta caraa de los embedings

    #ahora creamos nuestro llm

    print("Creacion y ejecucion del agente.")
    retrieval_qa_chat_promt = hub.pull("langchain-ai/retrieval-qa-chat")
    combines_docs_chain = create_stuff_documents_chain(
        OpenAI(),
        retrieval_qa_chat_promt
    )
    #ahora creamos la chain donde cargamos la base de datos vectorial y el modelo
    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(),
        combines_docs_chain
    )
    #ahora hacemos la llamada
    #aqui de una vez pasamos el prompt
    print("Consulta")
    res = retrieval_chain.invoke({"input": "Give me the gist of reAct in 3 sentences"})
    print(res["answer"])
    print("End of process")


