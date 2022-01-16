# https://testdriven.io/blog/fastapi-crud/

import pytest

pytestmark = pytest.mark.asyncio


class TestUserAPI:
    # @patch("sendgrid.base_interface.BaseInterface.send")
    async def test_create_user(self, client):
        # Given
        data = {
            "grant_type": "password",
            "email": "rozumalex@example.com",
            "password": "test",
            "client_id": "c",
            "client_secret": "s",
        }

        # response = client.post("/users/register", data=data)

        response = await client.post("/users/register", data=data)

        from app.core.config import get_settings

        print(get_settings().POSTGRES_DB)

        # Then
        # assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
