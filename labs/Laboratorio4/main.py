import os
from dotenv import  load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
# es para ver el tema de retrival chains
from langchain.chains.retrieval import  create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == '__main__':
    print("Retrieving")
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    #vamos a hacer una variable query y este query es la pregunta que le vamos a hacer a nuestro agente
    query = "what is Pinecone in machine learning"

    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    print(result.content)

    #pinecone object
    vectorStore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"],
        embedding=embeddings
    )

    #prompt model de la comunidad para poder hacer el Q&A
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    #chain que toma el contenido de los docuementos y los une

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    #obtener los documentos y vamos a unir todo el contenido

    retrieval_chain = create_retrieval_chain(
        retriever=vectorStore.as_retriever(),
        combine_docs_chain=combine_docs_chain
    )

    result = retrieval_chain.invoke({"input": query})

    #print(result)

    template = """ Use the following pieces of context to answer the question at the end
    If you dont know the answer, just say you don't know, don't try to answer.
    Use three sentences maximum and keep the answer as concise as posibble. 
    Always say "tanks for asking" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer: """

    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": vectorStore.as_retriever()|format_docs, "question":
         RunnablePassthrough()} | custom_rag_prompt | llm
    )
    res = rag_chain.invoke(query)
    print(res.content)


