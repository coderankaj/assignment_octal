from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator, constr


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user.")
    username: constr(min_length=3, max_length=50) = Field(..., description="The unique username of the user.")
    full_name: str = Field(..., description="The full name of the user.")
    password: Optional[str] = Field(..., min_length=3, max_length=64, exclude=True,
                                    description="The user's password, which will be hashed and stored.")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        """Ensure the username is alphanumeric and within length constraints."""
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric (letters and numbers only).")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        """Ensure the password meets the minimum length requirement."""
        if value and len(value) < 3:
            raise ValueError("Password must be at least 3 characters long.")
        return value


class AuthSchema(UserBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    is_active: Optional[bool] = Field(True, description="Whether the user is active or not.")

    created_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was last updated.")

    def update_timestamps(self):
        """Update the `updated_at` field with the current timestamp."""
        self.updated_at = datetime.utcnow()

    @property
    def is_account_active(self) -> bool:
        return self.is_active


class CreateUserSchema(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "user123",
                "full_name": "John Doe",
                "password": "securepassword"
            }
        }
