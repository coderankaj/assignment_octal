from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from fastapi import HTTPException
from pydantic import EmailStr
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from src.app.database import MongoDBMotorClient
from src.users.schemas.auth import CreateUserSchema, AuthSchema
from src.users.utils.password import get_password_hash, verify_password


class UserService:
    def __init__(self):
        """Initialize UserService with a MongoDBMotorClient instance."""
        self.db = MongoDBMotorClient().db
        self.collection = self.db.get_collection("users")

    @staticmethod
    async def is_valid_object_id(id: str):
        """Validate if the given ID is a valid ObjectId."""
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        return ObjectId(id)

    async def check_if_user_exists(self, username: str, email: EmailStr, is_raise=True):
        """Check if a user already exists by username or email using MongoDB $or query."""
        query = {
            "$or": [
                {"username": username},
                {"email": email}
            ]
        }

        # Perform the query
        existing_user = await self.collection.find_one(query)

        if existing_user:
            if existing_user.get('username') == username:
                raise HTTPException(status_code=400, detail="Username already exists.") if is_raise else True
            if existing_user.get('email') == email:
                raise HTTPException(status_code=400, detail="Email already exists.") if is_raise else True

        return False

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user_by_username(username)
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def create_user(self, user_data: CreateUserSchema) -> AuthSchema:
        """Create a new user in the database."""
        try:

            user_dict = user_data.model_dump(by_alias=True)

            # Assign timestamps
            user_dict["created_at"] = user_dict["updated_at"] = datetime.utcnow()
            user_dict["password"] = get_password_hash(user_data.password)

            # Insert user into the database
            result = await self.collection.insert_one(user_dict)
            user_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string

            return AuthSchema(**user_dict)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error while creating user: {e}")

    async def get_user_by_id(self, user_id: str) -> Optional[AuthSchema]:
        """Retrieve a user by their ID."""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
                return AuthSchema(**user)
            return None
        except (PyMongoError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user by ID: {e}")

    async def get_all_users(self) -> List[AuthSchema]:
        """Retrieve all users from the database."""
        try:
            return [
                AuthSchema(**{**user, "_id": str(user["_id"])})
                async for user in self.collection.find()
            ]
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error while fetching users: {e}")

    async def update_user(self, user_id: str, update_data: dict) -> Optional[AuthSchema]:
        """Update a user's details."""
        try:
            if not ObjectId.is_valid(user_id):
                raise HTTPException(status_code=400, detail="Invalid user ID format")

            update_data["updated_at"] = datetime.utcnow()

            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )

            if result:
                result["_id"] = str(result["_id"])
                return AuthSchema(**result)

            return None  # User not found

        except (PyMongoError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Error updating user: {e}")

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user by their ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except (PyMongoError, ValueError) as e:
            raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")

    async def get_user_by_email(self, email: str) -> Optional[AuthSchema]:
        """Retrieve a user by their email."""
        try:
            user = await self.collection.find_one({"email": email})
            if user:
                user["_id"] = str(user["_id"])
                return AuthSchema(**user)
            return None
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user by email: {e}")

    async def get_user_by_username(self, username: str) -> Optional[AuthSchema]:
        """Retrieve a user by their username."""
        try:
            user = await self.collection.find_one({"username": username})
            if user:
                user["_id"] = str(user["_id"])
                return AuthSchema(**user)
            return None
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user by email: {e}")
