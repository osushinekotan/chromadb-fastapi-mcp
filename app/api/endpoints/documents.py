import uuid

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.db.client import get_chroma_client
from app.models.document import (
    AddDocumentsRequest,
    DeleteDocumentsRequest,
    GetDocumentsRequest,
    GetDocumentsResponse,
    QueryDocumentsRequest,
    QueryResponse,
    SuccessResponse,
)

settings = get_settings()
router = APIRouter()


@router.post("/add", response_model=SuccessResponse)
async def add_documents(request: AddDocumentsRequest) -> SuccessResponse:
    """Add documents to a Chroma collection.

    Args:
        request: Document addition parameters

    Returns:
        A SuccessResponse with confirmation message
    """
    if not request.documents:
        raise HTTPException(status_code=400, detail="The 'documents' list cannot be empty.")

    client = get_chroma_client()
    print("Number of documents that can be inserted at once: ", client.max_batch_size)
    try:
        collection = client.get_or_create_collection(
            request.collection_name,
            embedding_function=OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small",
            ),
        )

        # Generate sequential IDs
        ids = [str(uuid.uuid4()) for _ in range(len(request.documents))]
        for metadata, _id in zip(request.metadatas, ids, strict=True):
            if not metadata:
                metadata["id"] = _id

        collection.add(documents=request.documents, metadatas=request.metadatas, ids=ids)

        return SuccessResponse(
            message=f"Successfully added {len(request.documents)} documents to collection {request.collection_name}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add documents to collection '{request.collection_name}': {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryDocumentsRequest) -> QueryResponse:
    """Query documents from a Chroma collection with advanced filtering.

    Args:
        request: Document query parameters

    Returns:
        Query results
    """
    if not request.query_texts:
        raise HTTPException(status_code=400, detail="The 'query_texts' list cannot be empty.")

    client = get_chroma_client()
    try:
        collection = client.get_collection(request.collection_name)
        results = collection.query(
            query_texts=request.query_texts,
            n_results=request.n_results,
            where=request.where or None,
            where_document=request.where_document or None,
            include=request.include,
        )
        return QueryResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to query documents from collection '{request.collection_name}': {str(e)}"
        )


@router.post("/get", response_model=GetDocumentsResponse)
async def get_documents(request: GetDocumentsRequest) -> GetDocumentsResponse:
    """Get documents from a Chroma collection with optional filtering.

    Args:
        request: Document retrieval parameters

    Returns:
        Retrieved documents
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(request.collection_name)
        results = collection.get(
            ids=request.ids,
            where=request.where or None,
            where_document=request.where_document or None,
            include=request.include,
            limit=request.limit,
            offset=request.offset,
        )
        return GetDocumentsResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get documents from collection '{request.collection_name}': {str(e)}"
        )


@router.delete("/delete", response_model=SuccessResponse)
async def delete_documents(request: DeleteDocumentsRequest) -> SuccessResponse:
    """Delete documents from a Chroma collection.

    Args:
        request: Document deletion parameters

    Returns:
        A SuccessResponse with confirmation message
    """
    if not request.ids:
        raise HTTPException(status_code=400, detail="The 'ids' list cannot be empty.")

    client = get_chroma_client()
    try:
        collection = client.get_collection(request.collection_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collection '{request.collection_name}': {str(e)}")

    try:
        collection.delete(ids=request.ids)
        return SuccessResponse(
            message=f"Successfully deleted {len(request.ids)} documents from "
            f"collection '{request.collection_name}'. Note: Non-existent IDs are ignored by ChromaDB."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete documents from collection '{request.collection_name}': {str(e)}"
        )
