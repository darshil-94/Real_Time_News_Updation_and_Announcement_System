from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import OllamaLLM , OllamaEmbeddings 
from dotenv import load_dotenv
import os
from pymongo import DESCENDING
from langchain_chroma import Chroma
from Connect import get_database

load_dotenv()

API_KEY = os.getenv("API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Database setup ---
users, news_collection, processed_news_collection, announced_news, announcement_tracker = get_database()

# --- LLM & Embeddings setup ---
llm = OllamaLLM(
    model="llama3"
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# --- Vector DB setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "db", "chroma_db")
db = Chroma(persist_directory=persistent_dir, embedding_function=embeddings)

# --- Retriever for relevant news context ---
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'k': 3, 'score_threshold': 0.5}
)

# --- Chat history with initial system prompt ---
chat_history: list = [
    SystemMessage(
        content=(
            "You are a news expert AI Assistant with vast knowledge of current events. "
            "Your name is Pravakta. "
            "Your role is to provide concise (under 100 words), accurate, and up-to-date news information "
            "using credible sources and clear, user-friendly language. "
            "Answer news-related queries uniquely and thoroughly. "
            "If asked your name, respond: 'I am Pravakta, your news assistant.' "
            "If a query is not about news, kindly respond: "
            "'I only answer news related queries. This is not my section.' "
            "If there is no relevant information available, gently inform the user that there are no updates "
            "at this time. For greetings or goodbyes, reply with a unique, one-line quote. "
            "Always act as a best friend, offering warm, friendly, and supportive responses."
        )
    )
]

def get_bot_response(query: str) -> str:
    """
    Appends the user query to chat history, fetches relevant news context,
    invokes the LLM with the full history, and returns the AI's reply.
    """
    global chat_history

    # 1️⃣ Add the user query
    chat_history.append(HumanMessage(content=query))

    # 2️⃣ Fetch relevant docs and optionally include in the prompt
    relevant_docs = retriever.get_relevant_documents(query)
    if relevant_docs:
        context = "\n\n".join(doc.page_content for doc in relevant_docs)
        # We prepend a hidden context note so the LLM sees it inline
        chat_history.insert(
            -1,
            SystemMessage(content=f"Relevant news context:\n{context}")
        )

    # 3️⃣ Invoke the model with the full message list
    raw_response = llm.invoke(chat_history)

    # 4️⃣ Normalize to AIMessage
    if isinstance(raw_response, AIMessage):
        ai_msg = raw_response
    elif isinstance(raw_response, dict) and "content" in raw_response:
        ai_msg = AIMessage(content=raw_response["content"])
    else:
        ai_msg = AIMessage(content=str(raw_response))

    # 5️⃣ Append the AI reply to history and return the text
    chat_history.append(ai_msg)
    return ai_msg.content
