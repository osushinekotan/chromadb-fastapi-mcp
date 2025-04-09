from typing import Any

from pydantic import BaseModel, Field


class AddDocumentsRequest(BaseModel):
    """Request model for adding documents to a collection."""

    collection_name: str = Field(..., description="Name of the collection to add documents to")
    documents: list[str] = Field(..., description="List of text documents to add")
    metadatas: list[dict[str, Any]] | None = Field(
        default=None, description="Optional list of metadata dictionaries for each document"
    )


class QueryDocumentsRequest(BaseModel):
    """Request model for querying documents from a collection."""

    collection_name: str = Field(..., description="Name of the collection to query")
    query_texts: list[str] = Field(..., description="List of query texts to search for")
    n_results: int = Field(default=5, description="Number of results to return per query")
    where: dict[str, Any] | None = Field(
        default=None,
        description="Optional metadata filters using Chroma's query operators. default is empty dict."
        'A Where type dict used to filter results by. E.g. {"color" : "red", "price": 4.20}',
    )
    where_document: dict[str, Any] | None = Field(
        default=None,
        description="Optional document content filters. default is empty dict. "
        'A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}',
    )
    include: list[str] = Field(
        default=["documents", "metadatas", "distances"], description="List of what to include in response"
    )


class GetDocumentsRequest(BaseModel):
    """Request model for getting documents from a collection."""

    collection_name: str = Field(..., description="Name of the collection to get documents from")
    ids: list[str] | None = Field(default=None, description="Optional list of document IDs to retrieve")
    where: dict[str, Any] | None = Field(
        default=None,
        description="Optional metadata filters using Chroma's query operators. default is empty dict."
        'A Where type dict used to filter results by. E.g. {"color" : "red", "price": 4.20}',
    )
    where_document: dict[str, Any] | None = Field(
        default=None,
        description="Optional document content filters. default is empty dict. "
        'A WhereDocument type dict used to filter by the documents. E.g. {$contains: {"text": "hello"}}',
    )
    include: list[str] = Field(default=["documents", "metadatas"], description="List of what to include in response")
    limit: int | None = Field(default=10, description="Optional maximum number of documents to return")
    offset: int | None = Field(default=0, description="Optional number of documents to skip before returning results")


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
