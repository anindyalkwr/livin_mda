from fastapi import FastAPI

from app.domains.users import routes as user_routes
from app.domains.transactions import routes as transaction_routes
from app.domains.products import routes as product_routes
from app.domains.categories import routes as category_routes
from app.domains.merchants import routes as merchant_routes
from app.domains.offers import routes as offer_routes

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(user_routes.router, prefix=settings.API_V1_STR, tags=["Users"])
app.include_router(transaction_routes.router, prefix=settings.API_V1_STR, tags=["Transactions"])
app.include_router(product_routes.router, prefix=f"{settings.API_V1_STR}/products", tags=["Products"])
app.include_router(category_routes.router, prefix=f"{settings.API_V1_STR}/categories", tags=["Categories"])
app.include_router(merchant_routes.router, prefix=f"{settings.API_V1_STR}/merchants", tags=["Merchants"])
app.include_router(offer_routes.router, prefix=f"{settings.API_V1_STR}/offers", tags=["Offers"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI E-commerce API"}
