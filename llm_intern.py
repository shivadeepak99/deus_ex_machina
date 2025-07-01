from langchain_chroma import Chroma # <-- Updated import
from langchain_ollama import OllamaEmbeddings # <-- Updated import
# Load environment variables from .env file
from langchain_groq import ChatGroq

from dotenv  import load_dotenv
load_dotenv()
import os

# --- CONFIGURE THE NEW GROQ CHAT MODEL ---
try:
    # We can choose a model like "llama3-8b-8192" or "llama3-70b-8192"
    # Llama 3 8B is a great starting point - super fast and smart.
    chat_model = ChatGroq(
        temperature=0.7,
        # --- THE FIX: Using a current, powerful model ---
        model_name="llama3-8b-8192",
        api_key=os.environ.get("GROQ_API_KEY")
    )
except Exception as e:
    print(f"Error configuring Groq API: {e}")
    print("Please ensure your GROQ_API_KEY is set correctly in the .env file.")
    chat_model = None


def load_persona():
    """Loads the agent's persona from the markdown file."""
    try:
        with open('persona.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "No persona file found."


# Load the persona once when the module is imported
PERSONA = load_persona()


def delegate_task(prompt: str) -> str:
    """
    Delegates a task to the LLM (now using Groq via LangChain).
    """
    if not chat_model:
        return "ERROR: Groq chat model not initialized."

    final_prompt = f"{PERSONA}\n\n--- TASK ---\n\n{prompt}"

    try:
        response = chat_model.invoke(final_prompt)
        return response.content
    except Exception as e:
        return f"ERROR: An unexpected LLM error occurred with Groq - {e}"
