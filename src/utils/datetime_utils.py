from datetime import datetime, timezone


def checkValidExpirationToken(exp: float) -> bool:
    return datetime.fromtimestamp(exp, timezone.utc) >= datetime.now(timezone.utc)
