from typing import Any

from pydantic import BaseModel, Field


class CreateCollectionRequest(BaseModel):
    """Request model for creating a new collection."""

    collection_name: str = Field(..., description="Name of the collection to create")


class ModifyCollectionRequest(BaseModel):
    """Request model for modifying a collection."""

    new_name: str | None = Field(default=None, description="Optional new name for the collection")


class CollectionListResponse(BaseModel):
    """Response model for listing collections."""

    collections: list[str] = Field(..., description="List of collection names")


class CollectionInfoResponse(BaseModel):
    """Response model for collection info."""

    name: str = Field(..., description="Name of the collection")
    count: int = Field(..., description="Number of documents in the collection")
    sample_documents: dict[str, Any] = Field(..., description="Sample documents from the collection")


class SuccessResponse(BaseModel):
    """Generic success response model."""

    message: str = Field(..., description="Success message")
