from typing import List, Optional

from sqlmodel import SQLModel


class Application(SQLModel):
    pass


class Grant(SQLModel):
    pass


class TokenData(SQLModel):
    username: Optional[str] = None
    scopes: List[str] = []


class RefreshToken(SQLModel):
    pass


class IDToken(SQLModel):
    pass
