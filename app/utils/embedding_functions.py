from chromadb.api import EmbeddingFunction
from chromadb.utils.embedding_functions import (
    DefaultEmbeddingFunction,
    OpenAIEmbeddingFunction,
)
from app.core.config import get_settings
from typing import Dict, Type

settings = get_settings()


# Configure embedding functions
def get_openai_embedding_function() -> OpenAIEmbeddingFunction:
    """Create and return an OpenAI embedding function.

    Returns:
        OpenAIEmbeddingFunction: An instance of the OpenAI embedding function

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment variables
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is required for OpenAI embedding function")

    return OpenAIEmbeddingFunction(api_key=settings.OPENAI_API_KEY, model_name="text-embedding-ada-002")


# Dictionary of available embedding functions
available_embedding_functions: Dict[str, Type[EmbeddingFunction]] = {
    "default": DefaultEmbeddingFunction,
    "openai": OpenAIEmbeddingFunction,
}


def get_embedding_function(name: str = "openai") -> EmbeddingFunction:
    """Get the specified embedding function.

    Args:
        name: Name of the embedding function to get ("default" or "openai")

    Returns:
        EmbeddingFunction: The requested embedding function instance

    Raises:
        ValueError: If the requested embedding function is not available
    """
    if name not in available_embedding_functions:
        raise ValueError(
            f"Embedding function '{name}' is not available. Choose from: {', '.join(available_embedding_functions.keys())}"
        )

    if name == "openai":
        return get_openai_embedding_function()
    else:
        return available_embedding_functions[name]()
