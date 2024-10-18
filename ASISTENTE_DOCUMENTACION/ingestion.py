from dotenv import  load_dotenv
import requests
load_dotenv()
import os

from firecrawl import FirecrawlApp
from langchain.schema import Document
import time
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



def ingest_url() -> None:
    urls_to_load = [
        'https://tuscriaturas.miraheze.org/wiki/Bestiateca:Todos_los_mañanas',
        'https://en.wikipedia.org/wiki/All_Tomorrows',
        'https://speculativeevolution.fandom.com/wiki/All_Tomorrows',
        'https://nofm-radio.com/tecnologia/internet/all-tomorrows-biologia-especulativa-y-antifascismo/',
        'https://aliens.fandom.com/wiki/Qu',
        'https://aliens.fandom.com/wiki/Subject_(All_Tomorrows)',
        'https://aliens.fandom.com/wiki/Spacer_(All_Tomorrows)',
        'https://aliens.fandom.com/wiki/Colonial_(All_Tomorrows)'
    ]
    
    for url in urls_to_load:
        app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        
        try:
            # Intentamos scraper la URL con un timeout personalizado (si es soportado)
            print(f"Scraping {url}...")
            page_content = app.scrape_url(
                url=url,
                params={
                    "onlyMainContent": True
                }
            )
            print("Contenido obtenido exitosamente.")
            
            # Procesar y dividir el contenido
            doc = Document(page_content=str(page_content), metadata={"source": url})
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
            docs = text_splitter.split_documents([doc])

            # Subir documentos a Pinecone
            PineconeVectorStore.from_documents(
                docs, embedings, index_name=os.getenv('INDEX_NAME')
            )
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP al intentar scrape URL: {url} - {str(e)}")
        except requests.exceptions.Timeout:
            print(f"Timeout alcanzado para la URL: {url}")
        except Exception as e:
            print(f"Error general al procesar la URL {url}: {str(e)}")
        
        # Espera unos segundos entre solicitudes para evitar sobrecargar el servidor
        time.sleep(2)


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
    ingest_url()

