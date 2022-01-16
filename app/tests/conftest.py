from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sendgrid.base_interface import BaseInterface

from app.core.config import settings
from app.core.helpers import override_settings
from app.main import app


@pytest.fixture
async def client():
    with override_settings(POSTGRES_DB=f"{settings.POSTGRES_DB}_test"):
        async with AsyncClient(app=app, base_url="http://test/latest") as client:
            yield client


@pytest.fixture(scope="session", autouse=True)
def patch_sendgrid():
    with patch.object(BaseInterface, "send") as _fixture:
        yield _fixture
