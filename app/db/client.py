import chromadb

from app.core.config import get_settings

settings = get_settings()

# Global client instance
_chroma_client = None


def get_chroma_client() -> chromadb.Client:
    """Get or create the ChromaDB client instance.

    Returns:
        chromadb.Client: The ChromaDB client instance
    """
    global _chroma_client

    if _chroma_client is None:
        if settings.CHROMA_CLIENT_TYPE == "persistent":
            if not settings.CHROMA_DATA_DIR:
                raise ValueError(
                    "Data directory must be provided via CHROMA_DATA_DIR environment variable when using persistent client"
                )
            _chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DATA_DIR)
            print(f"Using persistent Chroma client with data directory: {settings.CHROMA_DATA_DIR}")
        else:  # ephemeral
            _chroma_client = chromadb.EphemeralClient()
            print("Using ephemeral Chroma client")

    return _chroma_client
