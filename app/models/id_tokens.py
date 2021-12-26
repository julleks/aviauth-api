from sqlmodel import Field, SQLModel


class IDToken(SQLModel, table=True):
    token: str = Field(primary_key=True)
