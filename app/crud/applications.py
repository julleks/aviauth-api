from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud.base import CRUDBase, ModelType
from app.models.applications import Application


class CRUDApplication(CRUDBase):
    async def get(self, db: AsyncSession, client_id: str) -> Optional[ModelType]:

        statement = select(self.model).where(self.model.client_id == client_id)
        results = await db.execute(statement)

        return results.scalar_one_or_none()


applications = CRUDApplication(Application)
