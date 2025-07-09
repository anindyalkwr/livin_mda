from fastapi import APIRouter, Depends, Query
from . import handlers, schemas

router = APIRouter()

@router.get("/", response_model=schemas.CategoryList)
def read_all_categories(
    handler: handlers.CategoryHandler = Depends(),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    """
    Retrieve all product categories with pagination. Publicly accessible.
    """
    return handler.get_all_categories(page=page, size=size)