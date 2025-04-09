from fastapi import APIRouter

from app.api.endpoints import collections, documents

api_router = APIRouter()

api_router.include_router(collections.router, prefix="/collections", tags=["collections"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
