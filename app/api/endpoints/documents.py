from fastapi import APIRouter, HTTPException

from app.db.client import get_chroma_client
from app.models.document import (
    AddDocumentsRequest,
    DeleteDocumentsRequest,
    GetDocumentsRequest,
    GetDocumentsResponse,
    QueryDocumentsRequest,
    QueryResponse,
    SuccessResponse,
    UpdateDocumentsRequest,
)

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
    try:
        collection = client.get_or_create_collection(request.collection_name)

        # Generate sequential IDs if none provided
        if request.ids is None:
            request.ids = [str(i) for i in range(len(request.documents))]

        collection.add(documents=request.documents, metadatas=request.metadatas, ids=request.ids)

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
            where=request.where,
            where_document=request.where_document,
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
            where=request.where,
            where_document=request.where_document,
            include=request.include,
            limit=request.limit,
            offset=request.offset,
        )
        return GetDocumentsResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get documents from collection '{request.collection_name}': {str(e)}"
        )


@router.put("/update", response_model=SuccessResponse)
async def update_documents(request: UpdateDocumentsRequest) -> SuccessResponse:
    """Update documents in a Chroma collection.

    Args:
        request: Document update parameters

    Returns:
        A SuccessResponse with confirmation message
    """
    if not request.ids:
        raise HTTPException(status_code=400, detail="The 'ids' list cannot be empty.")

    if request.embeddings is None and request.metadatas is None and request.documents is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'embeddings', 'metadatas', or 'documents' must be provided for update.",
        )

    # Ensure provided lists match the length of ids if they are not None
    if request.embeddings is not None and len(request.embeddings) != len(request.ids):
        raise HTTPException(status_code=400, detail="Length of 'embeddings' list must match length of 'ids' list.")
    if request.metadatas is not None and len(request.metadatas) != len(request.ids):
        raise HTTPException(status_code=400, detail="Length of 'metadatas' list must match length of 'ids' list.")
    if request.documents is not None and len(request.documents) != len(request.ids):
        raise HTTPException(status_code=400, detail="Length of 'documents' list must match length of 'ids' list.")

    client = get_chroma_client()
    try:
        collection = client.get_collection(request.collection_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collection '{request.collection_name}': {str(e)}")

    # Prepare arguments for update, excluding None values at the top level
    update_args = {
        "ids": request.ids,
        "embeddings": request.embeddings,
        "metadatas": request.metadatas,
        "documents": request.documents,
    }
    kwargs = {k: v for k, v in update_args.items() if v is not None}

    try:
        collection.update(**kwargs)
        return SuccessResponse(
            message=f"Successfully processed update request for {len(request.ids)} documents in "
            f"collection '{request.collection_name}'. Note: Non-existent IDs are ignored by ChromaDB."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update documents in collection '{request.collection_name}': {str(e)}"
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
