from typing import Any

from pydantic import BaseModel, Field


class CreateCollectionRequest(BaseModel):
    """Request model for creating a new collection."""

    collection_name: str = Field(..., description="Name of the collection to create")
    embedding_function_name: str | None = Field(
        default="openai", description="Name of the embedding function to use. Options: 'default', 'openai'"
    )
    metadata: dict[str, Any] | None = Field(default=None, description="Optional metadata dict to add to the collection")
    space: str | None = Field(
        default=None, description="Distance function used in HNSW index. Options: 'l2', 'ip', 'cosine'"
    )
    ef_construction: int | None = Field(
        default=None, description="Size of the dynamic candidate list for constructing the HNSW graph"
    )
    ef_search: int | None = Field(
        default=None, description="Size of the dynamic candidate list for searching the HNSW graph"
    )
    max_neighbors: int | None = Field(
        default=None, description="Maximum number of neighbors to consider during HNSW graph construction"
    )
    num_threads: int | None = Field(default=None, description="Number of threads to use during HNSW construction")
    batch_size: int | None = Field(
        default=None, description="Number of elements to batch together during index construction"
    )
    sync_threshold: int | None = Field(
        default=None, description="Number of elements to process before syncing index to disk"
    )
    resize_factor: float | None = Field(default=None, description="Factor to resize the index by when it's full")


class ModifyCollectionRequest(BaseModel):
    """Request model for modifying a collection."""

    new_name: str | None = Field(default=None, description="Optional new name for the collection")
    new_metadata: dict[str, Any] | None = Field(default=None, description="Optional new metadata for the collection")
    ef_search: int | None = Field(
        default=None, description="Size of the dynamic candidate list for searching the HNSW graph"
    )
    num_threads: int | None = Field(default=None, description="Number of threads to use during HNSW construction")
    batch_size: int | None = Field(
        default=None, description="Number of elements to batch together during index construction"
    )
    sync_threshold: int | None = Field(
        default=None, description="Number of elements to process before syncing index to disk"
    )
    resize_factor: float | None = Field(default=None, description="Factor to resize the index by when it's full")


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
