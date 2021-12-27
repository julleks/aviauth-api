from sqlalchemy.inspection import inspect
from sqlmodel import SQLModel as OriginalSQLModel


class SQLModel(OriginalSQLModel):
    @property
    def pk(self):
        return "-".join([str(value) for value in inspect(self).identity])
