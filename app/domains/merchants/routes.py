from fastapi import APIRouter, Depends, Query
from . import handlers, schemas

router = APIRouter()

@router.get("/", response_model=schemas.MerchantList)
def read_all_merchants(
    handler: handlers.MerchantHandler = Depends(),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    """
    Retrieve all merchants with pagination. Publicly accessible.
    """
    return handler.get_all_merchants(page=page, size=size)
