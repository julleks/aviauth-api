from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models.access_tokens import AccessToken


class CRUDAccessToken(CRUDBase):
    async def get_active(
        self, db: AsyncSession, access_token: Any
    ) -> Optional[ModelType]:
        """Returns object by id."""

        statement = select(self.model).where(
            self.model.access_token == access_token,
            AccessToken.expires_at > datetime.now(),
            AccessToken.is_active,
        )
        results = await db.execute(statement)

        return results.scalar_one_or_none()


access_tokens = CRUDAccessToken(AccessToken)
