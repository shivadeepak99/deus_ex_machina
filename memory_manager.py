from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings  # We'll use a local model for embeddings
from cli_formatter import print_memory, print_error

# This is where Evaiya's memories will be stored on your disk
DB_DIRECTORY = "memory/chroma_db"

# Set up the embedding model. This converts text memories into numerical vectors.
# Make sure you have Ollama running with the 'nomic-embed-text' model pulled.
# In your terminal: `ollama run nomic-embed-text`
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
except Exception as e:
    print("Error with Ollama, make sure it's running with 'nomic-embed-text' model pulled.")
    print(f"Error: {e}")
    embeddings = None

# Initialize the vector store. This is our "diary".
vectorstore = Chroma(
    persist_directory=DB_DIRECTORY,
    embedding_function=embeddings
)


def save_memory(text_to_save: str):
    """Saves a string of text to the vector database."""
    if not embeddings:
        print_error("Memory Manager: Cannot save memory, embeddings not initialized.")
        return
    vectorstore.add_texts([text_to_save])
    print_memory(f"SAVED: '{text_to_save[:60]}...'")


def retrieve_memories(query: str, num_memories=3) -> list[str]:
    """Retrieves the most relevant memories based on a query."""
    if not embeddings:
        print_error("Memory Manager: Cannot retrieve memories, embeddings not initialized.")
        return []

    results = vectorstore.similarity_search(query, k=num_memories)
    return [doc.page_content for doc in results]
