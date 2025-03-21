from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.users.schemas.auth import AuthSchema
from src.users.services import UserService
from src.users.utils.password import decode_token

user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthSchema:
    """Extract and validate the current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id: str = decode_token(token)
        if not user_id or not ObjectId.is_valid(user_id):
            raise credentials_exception

        # Fetch user from database
        user_data = await user_service.get_user_by_id(user_id)
        if not user_data:
            raise credentials_exception

        return user_data

    except Exception:
        raise credentials_exception
