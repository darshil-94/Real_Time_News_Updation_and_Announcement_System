import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings 
from dotenv import load_dotenv
from Connect import get_database

users, news_collection, processed_news_collection, annouced_news, annoucement_tracker = get_database()

current_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(current_dir, "db", "chroma_db")

# Embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load or create vector store
if os.path.exists(persist_dir):
    print("Loading existing vector store...")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
else:
    print("Creating new vector store...")
    db = Chroma.from_documents([], embeddings, persist_directory=persist_dir)

# Fetch only unvectorized documents
new_documents = list(news_collection.find({"vectorized": {"$ne": True}}))

if not new_documents:
    print("No new documents to add.")
else:
    print(f"Found {len(new_documents)} new documents.")

    langchain_docs = []
    for doc in new_documents:
        content = f"{doc.get('headline', '')}\n{doc.get('description', '')}"
        langchain_docs.append(Document(page_content=content))

    # Split documents
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    docs = text_splitter.split_documents(langchain_docs)

    # Add to vector DB
    db.add_documents(docs)
    db.persist()
    print("New documents added and persisted to vector DB.")

    # Mark documents as vectorized
    ids = [doc["_id"] for doc in new_documents]
    news_collection.update_many({"_id": {"$in": ids}}, {"$set": {"vectorized": True}})
