import os
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Initialize Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index_name = "muet-chatbot"

# Connect to index
index = pc.Index(index_name)

# Embeddings
embeddings = OpenAIEmbeddings()

# Vector store
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# Retriever
retriever = vectorstore.as_retriever()

# LLM
llm = ChatOpenAI(model="gpt-4o-mini")

def ask_question(query):
    # Use similarity_search on vectorstore instead of retriever
    docs = vectorstore.similarity_search(query, k=5)  # k = number of relevant docs

    # Join the content
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI assistant for Mehran University.

Answer using the context below.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    return response.content