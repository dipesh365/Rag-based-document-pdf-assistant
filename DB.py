from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

#libraries which we can create documents by ourselves

from langchain_core.documents import Document

docs=[
    Document(page_content="Python is widely used in Artificial Intelligence.", metadata={"source": "AI_book"}),
    Document(page_content="Pandas is used for data analysis in Python.", metadata={"source": "DataScience_book"}),
    Document(page_content="Neural networks are used in deep learning.", metadata={"source": "DL_book"}),
]

#good part- chroma DB itself can create embeddings

embedding_model= MistralAIEmbeddings()

#we will create a vector store and we will tell that take your documents and use  the embedding model and where to save it and we tell these to our vector store

vectorstore = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    persist_directory="chroma-db"#local storage in my pc for now
)

result = vectorstore.similarity_search("what is used for data analysis?",k=2 )#k=2 (give me 2 similar searches)

for r in result:
    print(r.page_content)
    print(r.metadata)
    
retriver=vectorstore.as_retriever()#as default similariity search
    
docs = retriver.invoke("Explain deep learning")

for d in docs:
    print(d.page_content)