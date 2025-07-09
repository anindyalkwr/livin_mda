from fastapi import APIRouter, Depends, Query
from typing import Optional
from . import handlers, schemas

router = APIRouter()

@router.get("/", response_model=schemas.OfferList)
def read_all_offers(
    handler: handlers.OfferHandler = Depends(),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    category: Optional[str] = Query(None, description="Filter by category label (e.g., 'Elektronik')")
):
    """
    Retrieve all offers with pagination and optional category filter. Publicly accessible.
    """
    return handler.get_all_offers(page=page, size=size, category=category)
