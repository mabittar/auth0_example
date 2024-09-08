from datetime import datetime, timedelta

import jwt

from ..settings import settings


class JwtUtils:
    @classmethod
    def create_access_token(
        cls, *, data: dict, expires_delta: timedelta = timedelta(minutes=0)
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.app_secret_key, algorithm=settings.api_algorithm
        )
        return encoded_jwt

    @classmethod
    def refresh_token(cls, request):
        user_data = request.session.get("user", None)
        if user_data:
            expires = timedelta(minutes=settings.api_access_token_expire_minutos)
            token = cls.create_access_token(
                data={"sub": user_data["email"]}, expires_delta=expires
            )
            user_data.update({"Authorization": token})
            request.session["user"] = dict(user_data)
            return request
        else:
            return False

    @classmethod
    def create_token(cls, email):
        access_token_expires = timedelta(
            minutes=settings.api_access_token_expire_minutos
        )
        access_token = cls.create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return access_token

    @classmethod
    def decode_token(cls, token):
        return jwt.decode(
            token, settings.app_secret_key, algorithms=[settings.api_algorithm]
        )
