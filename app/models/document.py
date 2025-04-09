from typing import Any

from pydantic import BaseModel, Field


class AddDocumentsRequest(BaseModel):
    """Request model for adding documents to a collection."""

    collection_name: str = Field(..., description="Name of the collection to add documents to")
    documents: list[str] = Field(..., description="List of text documents to add")
    metadatas: list[dict[str, Any]] | None = Field(
        default=None, description="Optional list of metadata dictionaries for each document"
    )
    ids: list[str] | None = Field(default=None, description="Optional list of IDs for the documents")


class QueryDocumentsRequest(BaseModel):
    """Request model for querying documents from a collection."""

    collection_name: str = Field(..., description="Name of the collection to query")
    query_texts: list[str] = Field(..., description="List of query texts to search for")
    n_results: int = Field(default=5, description="Number of results to return per query")
    where: dict[str, Any] | None = Field(
        default=None, description="Optional metadata filters using Chroma's query operators"
    )
    where_document: dict[str, Any] | None = Field(default=None, description="Optional document content filters")
    include: list[str] = Field(
        default=["documents", "metadatas", "distances"], description="List of what to include in response"
    )


class GetDocumentsRequest(BaseModel):
    """Request model for getting documents from a collection."""

    collection_name: str = Field(..., description="Name of the collection to get documents from")
    ids: list[str] | None = Field(default=None, description="Optional list of document IDs to retrieve")
    where: dict[str, Any] | None = Field(
        default=None, description="Optional metadata filters using Chroma's query operators"
    )
    where_document: dict[str, Any] | None = Field(default=None, description="Optional document content filters")
    include: list[str] = Field(default=["documents", "metadatas"], description="List of what to include in response")
    limit: int | None = Field(default=None, description="Optional maximum number of documents to return")
    offset: int | None = Field(
        default=None, description="Optional number of documents to skip before returning results"
    )


class UpdateDocumentsRequest(BaseModel):
    """Request model for updating documents in a collection."""

    collection_name: str = Field(..., description="Name of the collection to update documents in")
    ids: list[str] = Field(..., description="List of document IDs to update")
    embeddings: list[list[float]] | None = Field(
        default=None, description="Optional list of new embeddings for the documents"
    )
    metadatas: list[dict[str, Any]] | None = Field(
        default=None, description="Optional list of new metadata dictionaries for the documents"
    )
    documents: list[str] | None = Field(default=None, description="Optional list of new text documents")


class DeleteDocumentsRequest(BaseModel):
    """Request model for deleting documents from a collection."""

    collection_name: str = Field(..., description="Name of the collection to delete documents from")
    ids: list[str] = Field(..., description="List of document IDs to delete")


class QueryResponse(BaseModel):
    """Response model for query results."""

    data: dict[str, Any] = Field(..., description="Query results")


class GetDocumentsResponse(BaseModel):
    """Response model for get documents results."""

    data: dict[str, Any] = Field(..., description="Get documents results")


class SuccessResponse(BaseModel):
    """Generic success response model."""

    message: str = Field(..., description="Success message")
