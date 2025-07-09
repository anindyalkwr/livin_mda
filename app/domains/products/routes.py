from fastapi import APIRouter, Depends, Query
from typing import Optional
from . import handlers, schemas

router = APIRouter()

@router.get("/", response_model=schemas.ProductList)
def read_all_products(
    handler: handlers.ProductHandler = Depends(),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    category: Optional[str] = Query(None, description="Filter by category label (e.g., 'Elektronik')")
):
    """
    Retrieve all products with pagination and optional category filter. Publicly accessible.
    """
    return handler.get_all_products(page=page, size=size, category=category)