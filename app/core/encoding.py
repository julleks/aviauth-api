__all__ = ["force_bytes"]


def force_bytes(string: str) -> bytes:
    return string.encode("utf-8")
