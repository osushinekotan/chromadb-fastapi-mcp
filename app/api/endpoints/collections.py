from typing import Any

from chromadb.api.collection_configuration import (
    CreateCollectionConfiguration,
    CreateHNSWConfiguration,
    UpdateCollectionConfiguration,
    UpdateHNSWConfiguration,
)
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.db.client import get_chroma_client
from app.models.collection import (
    CollectionInfoResponse,
    CollectionListResponse,
    CreateCollectionRequest,
    ModifyCollectionRequest,
    SuccessResponse,
)

settings = get_settings()
router = APIRouter()


@router.get("/", response_model=CollectionListResponse)
async def list_collections(limit: int = 10, offset: int = 0) -> CollectionListResponse:
    """List all collection names in the Chroma database with pagination support.

    Args:
        limit: Optional maximum number of collections to return
        offset: Optional number of collections to skip before returning results

    Returns:
        A CollectionListResponse containing collection names
    """
    client = get_chroma_client()
    try:
        colls = client.list_collections(limit=limit, offset=offset)
        return CollectionListResponse(collections=[coll.name for coll in colls])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")


@router.post("/", response_model=SuccessResponse)
async def create_collection(request: CreateCollectionRequest) -> SuccessResponse:
    """Create a new Chroma collection with configurable HNSW parameters.

    Args:
        request: Collection creation parameters

    Returns:
        A SuccessResponse with confirmation message
    """
    client = get_chroma_client()

    try:
        hnsw_config = CreateHNSWConfiguration()
        configuration = CreateCollectionConfiguration(hnsw=hnsw_config)

        client.create_collection(
            name=request.collection_name,
            configuration=configuration,
            embedding_function=OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small",
            ),
        )

        return SuccessResponse(message=f"Successfully created collection {request.collection_name}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create collection '{request.collection_name}': {str(e)}"
        )


@router.get("/{collection_name}/peek", response_model=dict[str, Any])
async def peek_collection(collection_name: str, limit: int = 5) -> dict[str, Any]:
    """Peek at documents in a Chroma collection.

    Args:
        collection_name: Name of the collection to peek into
        limit: Number of documents to peek at

    Returns:
        Sample documents from the collection
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(collection_name)
        results = collection.peek(limit=limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to peek collection '{collection_name}': {str(e)}")


@router.get("/{collection_name}/info", response_model=CollectionInfoResponse)
async def get_collection_info(collection_name: str) -> CollectionInfoResponse:
    """Get information about a Chroma collection.

    Args:
        collection_name: Name of the collection to get info about

    Returns:
        Collection information including name, count, and sample documents
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(collection_name)

        # Get collection count
        count = collection.count()

        # Peek at a few documents
        peek_results = collection.peek(limit=3)

        return CollectionInfoResponse(name=collection_name, count=count, sample_documents=peek_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collection info for '{collection_name}': {str(e)}")


@router.get("/{collection_name}/count", response_model=int)
async def get_collection_count(collection_name: str) -> int:
    """Get the number of documents in a Chroma collection.

    Args:
        collection_name: Name of the collection to count

    Returns:
        Number of documents in the collection
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(collection_name)
        return collection.count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collection count for '{collection_name}': {str(e)}")


@router.put("/{collection_name}", response_model=SuccessResponse)
async def modify_collection(collection_name: str, request: ModifyCollectionRequest) -> SuccessResponse:
    """Modify a Chroma collection's name

    Args:
        collection_name: Name of the collection to modify
        request: Collection modification parameters

    Returns:
        A SuccessResponse with confirmation message
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(collection_name)

        hnsw_config = UpdateHNSWConfiguration()
        configuration = UpdateCollectionConfiguration(hnsw=hnsw_config)
        collection.modify(name=request.new_name, configuration=configuration)

        modified_aspects = []
        if request.new_name:
            modified_aspects.append("name")

        return SuccessResponse(
            message=f"Successfully modified collection {collection_name}: updated {' and '.join(modified_aspects)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to modify collection '{collection_name}': {str(e)}")


@router.delete("/{collection_name}", response_model=SuccessResponse)
async def delete_collection(collection_name: str) -> SuccessResponse:
    """Delete a Chroma collection.

    Args:
        collection_name: Name of the collection to delete

    Returns:
        A SuccessResponse with confirmation message
    """
    client = get_chroma_client()
    try:
        client.delete_collection(collection_name)
        return SuccessResponse(message=f"Successfully deleted collection {collection_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete collection '{collection_name}': {str(e)}")
