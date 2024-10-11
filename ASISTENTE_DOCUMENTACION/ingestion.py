from dotenv import  load_dotenv
load_dotenv()
import os

#repartir los parrafos en diferentes chumks que tengan tama;os similares
from langchain.text_splitter import RecursiveCharacterTextSplitter

# esto sirve para consumir htmls , y sirve para poder leer mas que solo pdfs
from langchain_community.document_loaders import ReadTheDocsLoader

# Es para embedings, son pedazos de informacion que estan guardados en formato de base vectorial
from langchain_openai import OpenAIEmbeddings

#Sirve para consumir los pedazos de la base vectorial
from langchain_pinecone import PineconeVectorStore

#creamos los embedings

embedings = OpenAIEmbeddings(model="text-embedding-3-small")

#definir una funcion para hacer el consumo y mandarlo a nuestra base vectorial

def ingest_docs():
    #cargar la informacion que se desea consumir
    loader = ReadTheDocsLoader(r"langchain-docs/api.python.langchain.com/en/latest", encoding='utf-8', errors='ignore')
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} raw documents")

    #crear objeto para cortar en chumks todos los documentos que fueron cargados
    #chumk overlap para que se puedan ir armando en orden los chumks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    print(f"Load {len(documents)} documents")

    for doc in documents:
        #moldear esa data, la idea es crear una url para los chumks
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})
    print(f"Going to add {len(documents)} to Pinecone")
    name = os.getenv('INDEX_NAME')
    PineconeVectorStore.from_documents(
        documents, embedings, index_name=name
    )

if __name__ == "__main__":
    ingest_docs()

