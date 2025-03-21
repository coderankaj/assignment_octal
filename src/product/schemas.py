from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal, constr, field_validator


class ProductBaseSchema(BaseModel):
    """Base schema for product validation."""
    name: constr(min_length=3, max_length=50) = Field(..., description="The name of the product.")
    description: Optional[str] = Field(None, description="A detailed description of the product.")
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(..., description="The price of the product.")
    stock: Optional[int] = Field(0, ge=0, description="The number of items available in stock.")

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > 500:
            raise ValueError("Product description must not exceed 500 characters.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        """Ensure price is a positive value."""
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        return value

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value


class ProductCreateSchema(ProductBaseSchema):
    """Schema for creating a new product."""
    pass  # Inherits everything from ProductBaseSchema


class ProductUpdateSchema(ProductBaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None
    stock: Optional[int] = None


class ProductSchema(ProductBaseSchema):
    """Schema for full product representation."""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId as a string")
    owner_id: str = Field(..., description="The ID of the owner of the product.")
    is_active: bool = Field(True, description="Whether the product is active or not.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the product was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the product was last updated.")

    def update_timestamps(self):
        """Update the `updated_at` field with the current timestamp."""
        self.updated_at = datetime.utcnow()

    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0
