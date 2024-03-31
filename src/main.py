from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .auth.auth0 import auth0_app
from .infra.path_scripts import get_root_dir
from .settings import get_settings

env_settings = get_settings()
root_dir = get_root_dir()


def start_app() -> FastAPI:
    application = FastAPI(
        title="Auth0 Example App",
        description="Study Case",
    )
    application.add_middleware(
        SessionMiddleware, secret_key=env_settings.app_secret_key
    )

    application.include_router(auth0_app)
    print("Appliation initialized")
    return application


app = start_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
