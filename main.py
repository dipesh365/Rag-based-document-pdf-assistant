from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma#fro retrieval of information(selected query from the chroma db)
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

#embedding model for the query
embedding_model=MistralAIEmbeddings()
#vector store load
vectorstore=Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)
#retrievers
retriever= vectorstore.as_retriever(
search_type="mmr",
search_kwargs={
    "k":4,#after the similar search
    "fetch_k":10,
    "lambda_mult":0.5}#0,1 = 0 for more diverse reults and 1 for less diverse results
)
#search keywords in a dictionary


#LLM
llm=ChatMistralAI(model="mistral-small-2506")


#prompt template
prompt = ChatPromptTemplate.from_messages([
       (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),        (
            "human",
            """Context:
{context}

Question:
{question}
"""
        )#human will give context on the basis of retriever context and the retriever retrieves the context from vector store
    ])
    
print("Rag system created ")

print("press 0 to exit ")
    
while True:
    query = input("You : ")
    if query == '0':
        break
    
    docs=retriever.invoke(query)# koi bhi query ke samay retrieval ko call karna parega
    
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    
    final_prompt=prompt.invoke({
        "context":context,
        "question":query
    })
    
    response=llm.invoke(final_prompt)
    
    print(f"\n AI: {response.content}")
    



#WE ARE MAKING AN RAG APPLICATION AND WE ARE ANSWERING THE QUERY ON THE BASIS OF THE PDF AND I DONT WANT THE ANSWER IF THE QUERY INFORMATION IS NOT PRESENT IN THE PDF