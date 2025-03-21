from fastapi import APIRouter

from src.product.api.crud import product_crud_router
from src.users.routes import auth_router

v1_router = APIRouter()

v1_router.include_router(auth_router, tags=["Auth"])
v1_router.include_router(product_crud_router, tags=["Products CRUD"])
#
