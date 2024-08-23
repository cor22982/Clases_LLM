import os

from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader

#vamos a hacer varios parrafos y los que vamos a guardar en la base vectorial

from langchain.text_splitter import  CharacterTextSplitter

# Los embedings son los chuns de cadenas
from langchain_openai import OpenAIEmbeddings

from langchain_pinecone import  PineconeVectorStore

load_dotenv()

if __name__ == '__main__':
    print("Intesting......")

    # Un documento qu eeesea patiendol;;;;;;;;;;;;;;;;;;;;;;;;;
    # Textloader pide la direccion del archivo que vamos a crear
    loader = TextLoader("C:\\Users\\Owner\\PycharmProjects\\Clases_LLM\\labs\\Laboratorio4\\mediumblog1.txt", encoding="utf-8")
    document = loader.load()
    print("Splitting")
    # tama;o de los chunks por pedato
    # Chunk o tama;o y en overlap En las orillas de cada pedazo de testo se h
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"{len(texts)} tama;o de chunks")

    #ahora los embedings
    try:
        embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))
        PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ.get("INDEX_NAME"))
    except Exception as e:
        print(f"Error: {e}")
    #Ahora que ya tenemos nuetra base vectorial  pasemos al main