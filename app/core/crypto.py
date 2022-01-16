import hashlib
import hmac

from app.core.config import settings
from app.core.encoding import force_bytes

__all__ = ["salted_hmac"]


def salted_hmac(key_salt, value, secret=settings.SECRET_KEY, *, algorithm="sha1"):

    key_salt = force_bytes(key_salt)
    secret = force_bytes(secret)

    hasher = getattr(hashlib, algorithm)

    key = hasher(key_salt + secret).digest()

    return hmac.new(key, msg=force_bytes(value), digestmod=hasher)
