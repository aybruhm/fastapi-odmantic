# Uvicorn Imports
import uvicorn

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Starlette Imports
from starlette.middleware.sessions import SessionMiddleware

# Own Imports
from config.secrets import get_settings
from apps.commoners.api import router as commoners_router
from apps.accounts.routers.auth import router as auth_router


# Initialize get_settings
secrets = get_settings()


def create_application() -> FastAPI:
    # initialize application
    application = FastAPI(
        title=secrets.API_TITLE,
        description=secrets.API_DESCRIPTION,
        version=secrets.API_VERSION,
        contact=secrets.API_CONTACT,
        openapi_url="/api-docs.json",
    )

    # mount middlewares
    application.add_middleware(
        CORSMiddleware,
        allow_origins=secrets.ALLOWED_ORIGINS.split(","),
        allow_credentials=secrets.ALLOWED_CREDENTIALS,
        allow_methods=secrets.ALLOWED_METHODS.split(","),
        allow_headers=secrets.ALLOWED_HEADERS,
    )
    application.add_middleware(SessionMiddleware, secret_key=secrets.JWT_SECRET_KEY)

    @application.get(
        "/",
        responses={
            200: {
                "description": "Service is healthy",
                "content": {
                    "application/json": {
                        "schema": {
                            "example": {
                                "heartbeat": True,
                                "message": "Backend is healthy and running.",
                            }
                        }
                    }
                },
            }
        },
    )
    async def read_root() -> dict:
        return {
            "heartbeat": True,
            "message": "Backend is healthy and running.",
        }

    # include routers
    application.include_router(auth_router)
    application.include_router(commoners_router)

    return application
