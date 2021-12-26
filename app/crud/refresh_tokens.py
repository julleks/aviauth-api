from app.crud.base import CRUDBase
from app.models.refresh_tokens import RefreshToken


class CRUDUser(CRUDBase):
    pass


refresh_tokens = CRUDUser(RefreshToken)
