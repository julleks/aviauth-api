from typing import Any, List, Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.datetime import datetime
from app.crud.applications import applications
from app.crud.base import CRUDBase, ModelType
from app.crud.refresh_tokens import refresh_tokens
from app.exceptions.applications import InvalidClientCredentials
from app.models.access_tokens import AccessToken, AccessTokenRead
from app.models.refresh_tokens import RefreshToken
from app.models.users import User

__all__ = ["access_tokens"]


class CRUDAccessToken(CRUDBase):
    async def get_access_token_and_user(
        self, db: AsyncSession, access_token: Any
    ) -> Optional[List[Union[ModelType, User]]]:
        """Returns object by id."""

        statement = (
            select(self.model, User)
            .where(
                self.model.access_token == access_token,
                AccessToken.expires_at > datetime.now(),
                AccessToken.deactivated_at == None,
            )
            .join(User, isouter=True)
        )
        results = await db.execute(statement)

        return results.fetchone()

    async def create_access_token(
        self,
        session: AsyncSession,
        client_id: str,
        client_secret: str,
        user_id: UUID,
        scope: str,
    ) -> AccessTokenRead:
        application = await applications.get(session, client_id)

        if not (application and application.verify_secret(client_secret)):
            await session.rollback()
            raise InvalidClientCredentials

        refresh_token = await refresh_tokens.create(
            session,
            RefreshToken(
                user_id=user_id, scope=scope, application_id=application.client_id
            ),
        )

        access_token = await self.create(
            session,
            AccessToken(
                user_id=user_id,
                scope=scope,
                refresh_token=refresh_token.token,
                application_id=application.client_id,
            ),
        )

        return AccessTokenRead(**access_token.dict())


access_tokens = CRUDAccessToken(AccessToken)
