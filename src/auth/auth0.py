from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.config import Config
from starlette.requests import Request

from ..exceptions import CREDENTIALS_EXCEPTION
from ..infra.path_scripts import get_dir_from_root
from ..settings import settings
from ..utils.jwt_utils import JwtUtils
from ..utils.oauth_utils import OauthUtils

templates_dir = get_dir_from_root("templates")

templates = Jinja2Templates(directory=templates_dir)
auth0_app = APIRouter()

AUTH0_CLIENT_ID = settings.auth0_client_id
AUTH0_CLIENT_SECRET = settings.auth0_client_secret
AUTH0_DOMAIN = settings.auth0_domain
if None in [AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET]:
    raise HTTPException(status_code=500, detail="Missing env variables")

config_data = {
    "AUTH0_CLIENT_ID": AUTH0_CLIENT_ID,
    "AUTH0_CLIENT_SECRET": AUTH0_CLIENT_SECRET,
}
starlette_config = Config(environ=config_data)  # type: ignore
oauth = OAuth(starlette_config)
oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
        "prompt": "select_account",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)  # type: ignore


@auth0_app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth0_app.get("/welcome")
async def welcome(request: Request, email: str = Depends(OauthUtils.validate_auth)):
    return templates.TemplateResponse(
        "welcome.html", {"request": request, "user_email": email}
    )


@auth0_app.get("/login")
async def login(request: Request):
    auth0 = oauth.create_client("auth0")
    redirect_url = request.url_for("auth_via_auth0")
    return await auth0.authorize_redirect(request, redirect_url)  # type: ignore


@auth0_app.get("/callback")
async def auth_via_auth0(
    request: Request, JwtUtils=Depends(JwtUtils), OauthUtils=Depends(OauthUtils)
):
    try:
        auth0 = oauth.create_client("auth0")
        token = await auth0.authorize_access_token(request)  # type: ignore
    except OAuthError:
        request.session.pop("user", None)
        return RedirectResponse(url="/")
    user_data = token["userinfo"]
    if OauthUtils.validate_email(user_data["email"]):
        token = JwtUtils.create_token(user_data["email"])
        user_data.update({"Authorization": token})
        request.session["user"] = dict(user_data)
        return RedirectResponse(url="/welcome")
    request.session.pop("user", None)
    raise CREDENTIALS_EXCEPTION


@auth0_app.route("/token")
async def auth(
    request: Request, JwtUtils=Depends(JwtUtils), OauthUtils=Depends(OauthUtils)
):
    try:
        auth0 = oauth.create_client("auth0")
        token = await auth0.authorize_access_token(request)  # type: ignore
    except OAuthError:
        return RedirectResponse(url="/")
    user_data = token["userinfo"]
    if OauthUtils.validate_email(user_data["email"]):
        token = JwtUtils.create_token(user_data["email"])
        return JSONResponse(
            {
                "result": True,
                "token": token,
                "token_type": "bearer",
            }
        )
