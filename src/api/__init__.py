"""Contains the entry point for API."""
import fastapi
from typing import Dict, Any, Callable

from . import main
import config
from logger import logger

# Initialize FastAPI
app = fastapi.FastAPI(
    title=config.TITLE,
    description=config.DESCRIPTION,
    debug=config.DEBUG,
)


app.include_router(main.router)


# TODO: compute city geocodes on start to process requests faster
@app.on_event("startup")
async def startup() -> None:
    """Code to run at the startup of the app like loading env variables."""
    logger.info("Ready to accept applications.")


@app.on_event("shutdown")
async def shutdown() -> None:
    """Code to run at the shutdown of the app like clearing cache."""
    pass


@app.middleware("http")
async def authorize(request: fastapi.Request, call_next: Callable) -> Dict[str, Any]:
    """Authorizes all incoming request."""
    # Whitelist some route. K8s need to access / to know the service is alive.
    whitelisted_routes = ["/", "/healthz"]
    if request["path"] in whitelisted_routes:
        return await call_next(request)

    # Authenticate the request
    request_key = request.headers.get("x-api-key", "")
    if not request_key:
        return fastapi.responses.JSONResponse(
            status_code=401,
            content={"_error": "Use header 'x-api-key' to authenticate"},
        )

    # authorize the request
    if request_key != config.api_key():
        return fastapi.responses.JSONResponse(
            status_code=403,
            content={"_error": "Contact #data-products for a valid API KEY"},
        )
    return await call_next(request)


@app.get("/", name="redirect", include_in_schema=False)
async def redirect_root() -> fastapi.responses.Response:
    """Redirect when the root path is contacted."""
    return fastapi.responses.Response("Hello, world!", media_type="text/plain")


@app.get("/keytest", name="test key", include_in_schema=False)
async def test_key() -> fastapi.responses.Response:
    """Route for checkin if API Key works."""
    return fastapi.responses.Response("Valid Key")


@app.get("/error", name="sentry error", include_in_schema=False)
async def _error() -> fastapi.responses.Response:
    """Raise exception for debugging purposes."""
    raise Exception("Exception to test Sentry.")
