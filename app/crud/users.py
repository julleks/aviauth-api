from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud.base import CRUDBase, ModelType
from app.models.users import User

__all__ = ["users"]


class CRUDUser(CRUDBase):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[ModelType]:

        statement = select(self.model).where(self.model.email == email)
        results = await db.execute(statement)

        return results.scalar_one_or_none()

    async def verify_email(self, db: AsyncSession, user: User) -> Optional[ModelType]:
        user.verify_email()

        db.add(user)
        await db.flush()

        return user


users = CRUDUser(User)
