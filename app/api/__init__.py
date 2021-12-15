from fastapi import APIRouter

from app.api import auth, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])


# Endpoints:
# /users/register
# /users/profile
# /users/profile/tokens/<id>/revoke
# /users/profile/access-history
# /auth/token
# /auth/refresh
# /auth/applications or /auth/applications/register
# /auth/applications -> list of user's applications
# /auth/applications/<id> -> application details
