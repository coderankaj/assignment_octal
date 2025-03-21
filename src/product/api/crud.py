from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.product.schemas import ProductCreateSchema, ProductSchema, ProductUpdateSchema
from src.product.services import ProductService
from src.users.dependencies.permissions import get_current_user

product_service = ProductService()
product_crud_router = APIRouter()


@product_crud_router.post("/products/", response_model=ProductSchema, status_code=201)
async def create_product(product_schema: ProductCreateSchema, current_user=Depends(get_current_user)):
    """Create a new product with proper error handling."""
    try:
        created_product = await product_service.create_product(current_user, product_schema)
        return created_product

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )


@product_crud_router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(product_id: str):
    """Get a product by ID."""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_crud_router.get("/products/", response_model=List[ProductSchema])
async def get_all_products():
    """Get all products."""
    return await product_service.get_all_products()


@product_crud_router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: str, update_data: ProductUpdateSchema, current_user=Depends(get_current_user)):
    """Update a product."""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if str(product.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You do not have permission to update this product")

    try:
        updated_product = await product_service.update_product(product_id, update_data)
        if not updated_product:
            return JSONResponse(status_code=404, content={"detail": "Product not found"})
        return updated_product

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )


@product_crud_router.patch("/products/{product_id}", response_model=ProductSchema)
async def partial_update_product(product_id: str, update_data: dict, current_user=Depends(get_current_user)):
    """Partially update a product."""

    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if str(product.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You do not have permission to update this product")

    try:
        updated_product = await product_service.partial_update_product(product_id, update_data)
        if not updated_product:
            return JSONResponse(status_code=404, content={"detail": "Product not found"})
        return updated_product

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )


@product_crud_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user=Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")

    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure the product belongs to the current user
    if str(product.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this product")

    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete product")

    return JSONResponse(content={"message": "Product deleted successfully"})


@product_crud_router.get("/products/search/{name}", response_model=List[ProductSchema])
async def search_products(name: str):
    """Search products by name."""
    return await product_service.get_products_by_name(name)
