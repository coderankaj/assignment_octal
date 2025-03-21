from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from bson import ObjectId, errors
from fastapi import HTTPException
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from src.app.database import MongoDBMotorClient
from src.product.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema


class ProductService:
    def __init__(self):
        """Initialize ProductService with a MongoDBMotorClient instance."""
        self.db = MongoDBMotorClient().db
        self.collection = self.db.get_collection("products")

    @staticmethod
    async def is_object_id(id: str):
        # Check if product_id is valid before querying the database
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")
        return id

    async def create_product(self, current_user,  product_data: ProductCreateSchema) -> ProductSchema:
        """Create a new product in the database."""
        try:
            product_dict = product_data.model_dump(
                exclude_unset=True, by_alias=True, exclude_defaults=True
            )

            # Convert Decimal fields to float
            if "price" in product_dict and isinstance(product_dict["price"], Decimal):
                product_dict["price"] = float(product_dict["price"])

            # Assign timestamps
            product_dict["created_at"] = product_dict["updated_at"] = datetime.utcnow()
            product_dict["owner_id"] = str(current_user.id)

            result = await self.collection.insert_one(product_dict)
            product_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string

            return ProductSchema(**product_dict)
        except Exception as e:
            raise Exception(f"Database error while creating product: {e}")

    async def get_product_by_id(self, product_id: str) -> Optional[ProductSchema]:
        """Get a product by its ID."""
        try:
            product = await self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product["_id"] = str(product["_id"])
                return ProductSchema(**product)
            return None
        except (PyMongoError, ValueError) as e:
            raise Exception(f"Error fetching product by ID: {e}")

    async def get_all_products(self) -> List[ProductSchema]:
        """Retrieve all products from the database."""
        try:
            return [
                ProductSchema(**{**product, "_id": str(product["_id"])})
                async for product in self.collection.find()
            ]
        except PyMongoError as e:
            raise Exception(f"Database error while fetching products: {e}")

    async def update_product(self, product_id: str, update_data: ProductUpdateSchema) -> Optional[ProductSchema]:
        """Update a product's details."""
        try:
            if not ObjectId.is_valid(product_id):
                raise ValueError("Invalid product ID format")

            update_dict = update_data.model_dump(exclude_unset=True, exclude_defaults=True)

            if "price" in update_dict and isinstance(update_dict["price"], Decimal):
                update_dict["price"] = float(update_dict["price"])

            update_dict["updated_at"] = datetime.utcnow()

            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(product_id)},
                {"$set": update_dict},
                return_document=ReturnDocument.AFTER
            )

            if result:
                result["_id"] = str(result["_id"])
                return ProductSchema(**result)

            return None  # Product not found

        except (errors.InvalidId, PyMongoError, ValueError) as e:
            raise Exception(f"Error updating product: {e}")

    async def partial_update_product(self, product_id: str, update_data: dict) -> Optional[ProductSchema]:
        """Partially update a product's details."""
        try:
            if not ObjectId.is_valid(product_id):
                raise ValueError("Invalid product ID format")

            if not update_data:
                raise HTTPException(status_code=400, detail="No fields to update")

            # Convert Decimal to float
            if "price" in update_data and isinstance(update_data["price"], Decimal):
                update_data["price"] = float(update_data["price"])

            update_data["updated_at"] = datetime.utcnow()

            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(product_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )

            if result:
                result["_id"] = str(result["_id"])
                return ProductSchema(**result)

            return None

        except (errors.InvalidId, PyMongoError, ValueError) as e:
            raise Exception(f"Error updating product: {e}")

    async def delete_product(self, product_id: str) -> bool:
        """Delete a product by its ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count > 0
        except (PyMongoError, ValueError) as e:
            raise Exception(f"Error deleting product: {e}")

    async def get_products_by_name(self, name: str) -> List[ProductSchema]:
        """Search for products by name (case-insensitive)."""
        try:
            return [
                ProductSchema(**{**product, "_id": str(product["_id"])})
                async for product in self.collection.find({"name": {"$regex": name, "$options": "i"}})
            ]
        except PyMongoError as e:
            raise Exception(f"Error searching products by name: {e}")
