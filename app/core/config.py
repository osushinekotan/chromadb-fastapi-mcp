from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings configuration."""

    APP_NAME: str = "ChromaDB FastAPI Server"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "FastAPI server for ChromaDB"
    APP_HOST: str = Field(description="Host for the FastAPI server")
    APP_PORT: int = Field(description="Port for the FastAPI server")

    # ChromaDB settings
    CHROMA_CLIENT_TYPE: str = Field(
        description="Type of Chroma client to use (persistent or ephemeral)",
    )
    CHROMA_DATA_DIR: str | None = Field(
        description="Directory for persistent client data (only used with persistent client)",
    )
    CHROMA_DOTENV_PATH: str = Field(description="Path to .env file")

    # OpenAI API key for embedding
    OPENAI_API_KEY: str | None = Field(description="OpenAI API key for embedding function")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Get application settings from cache."""
    return Settings()
