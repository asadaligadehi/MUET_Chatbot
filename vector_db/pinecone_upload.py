import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

# Pinecone connection
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "muet-chatbot"

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Index ready")

# Read scraped data
with open("data/muet_data.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split text into chunks  b/c llm can not handle the huge text at once
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_text(text)

docs = [Document(page_content=c) for c in chunks]     #Wraps text chunks into LangChain format.

# Embeddings
embeddings = OpenAIEmbeddings()

# Upload to Pinecone
vectorstore = PineconeVectorStore.from_documents(
    docs,
    embeddings,
    index_name=index_name
)

print("Documents uploaded to Pinecone successfully")