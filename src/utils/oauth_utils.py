import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from ..exceptions import CREDENTIALS_EXCEPTION
from ..settings import settings
from .datetime_utils import checkValidExpirationToken
from .jwt_utils import JwtUtils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class OauthUtils:
    @classmethod
    async def get_current_user_email(
        cls, token: str = Depends(oauth2_scheme), JwtUtils=Depends(JwtUtils)
    ):
        try:
            payload = JwtUtils.decode_token(token)
            email: str = payload.get("sub")
            if email is None:
                raise CREDENTIALS_EXCEPTION
        except jwt.PyJWTError:
            raise CREDENTIALS_EXCEPTION

        if JwtUtils.valid_email_server(email):
            return email

        raise CREDENTIALS_EXCEPTION

    @classmethod
    async def get_current_user_token(cls, token: str = Depends(oauth2_scheme)):
        _ = await cls.get_current_user_email(token)
        return token

    @classmethod
    async def validate_auth(cls, request: Request, JwtUtils=Depends(JwtUtils)):
        try:
            user_data = request.session.get("user", {})
            token = user_data.get("Authorization")
            if not user_data:
                return False
            payload = JwtUtils.decode_token(token)
            if checkValidExpirationToken(payload.get("exp")):
                email = payload.get("sub")
                if cls.validate_email(email):
                    return email
            request.session.pop("user", None)
            return False
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False

    @classmethod
    def validate_email(cls, email) -> bool:
        return email == settings.authorized_email
