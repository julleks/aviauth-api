from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud.base import CRUDBase, ModelType
from app.models.users import User


class CRUDUser(CRUDBase):
    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[ModelType]:

        statement = select(self.model).where(self.model.username == username)
        results = await db.execute(statement)

        return results.scalar_one_or_none()


users = CRUDUser(User)
