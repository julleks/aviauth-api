from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


__all__ = ["CRUDBase"]


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Returns object by id."""

        statement = select(self.model).where(self.model.id == id)
        results = await db.execute(statement)

        return results.scalar_one_or_none()

    #
    # async def all(
    #     self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    # ) -> List[ModelType]:
    #     """Returns all objects with skip and limit."""
    #
    #     statement = select(self.model).offset(skip).limit(limit)
    #     results = await db.execute(statement)
    #
    #     return results.scalars().all()

    async def create(self, db: AsyncSession, obj: ModelType) -> ModelType:
        """Create a new object in the database."""
        if not type(obj) == self.model:
            obj = self.model(**obj.dict())

        db.add(obj)
        await db.flush()

        return obj

    # async def update(self, db: AsyncSession, *, obj: ModelType) -> ModelType:
    #     """Update object in the database"""
    #
    #     db.add(obj)
    #     await db.commit()
    #     await db.refresh(obj)
    #
    #     return obj

    # async def delete(self, db: AsyncSession, pk: Any) -> None:
    #     """Delete object from the database by id."""
    #
    #     statement = select(self.model).where(self.model.id == pk)
    #     results = await db.execute(statement)
    #     obj = results.scalar()
    #
    #     await db.delete(obj)
    #     await db.commit()
    #
    #     return obj
