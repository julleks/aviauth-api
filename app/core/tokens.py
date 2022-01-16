from app.core.config import settings
from app.core.crypto import salted_hmac

__all__ = ["email_confirmation_token_generator"]


class EmailConfirmationTokenGenerator:
    def __init__(self, algorithm="sha256", secret=settings.SECRET_KEY):
        self.algorithm = algorithm
        self.secret = secret

    def create_token(self, user: "User") -> str:
        hash_value = f"{user.id}:{user.email}"

        return salted_hmac(
            key_salt="email-confirmation-token",
            value=hash_value,
            secret=self.secret,
            algorithm=self.algorithm,
        ).hexdigest()[::2]

        # return "ha30exd3h"

    def check_token(self, user: "User", token: str):
        if not (user and token):
            return False

        if not user.is_active:
            return False

        if user.is_verified:
            return False

        # if token == "ha30exd3h":
        #     return True

        if self.create_token(user) == token:
            return True

        return False


email_confirmation_token_generator = EmailConfirmationTokenGenerator()
