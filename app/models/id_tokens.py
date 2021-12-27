from sqlmodel import Field, SQLModel

__all__ = ["IDToken"]


class IDToken(SQLModel, table=True):
    token: str = Field(primary_key=True)
