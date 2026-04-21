import time
import logging
import uuid
from fastapi import Request, Response
from jose import jwt, JWTError
from app.core.config import settings

# Configure the logger — writes to stdout by default
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("ywt")

# Endpoints that don't carry a user token — logged without username
PUBLIC_ENDPOINTS = {"/token", "/users"}


def _extract_username(request: Request) -> str:
    """Try to extract the username from the Authorization header JWT.
    Returns 'anonymous' if no token or token is invalid.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "anonymous"
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub", "anonymous")
    except JWTError:
        return "anonymous"


async def logging_middleware(request: Request, call_next) -> Response:
    """AOP middleware — logs every request without touching any router or service.

    Captures:
    - Request ID (unique per request for tracing)
    - Caller username (extracted from JWT)
    - HTTP method + URL
    - Response status code
    - Execution time in ms
    - Error details on 4xx/5xx
    """

    # Generate a unique ID to correlate request and response logs
    request_id = str(uuid.uuid4())[:8]
    username = _extract_username(request)
    method = request.method
    url = request.url.path
    query = f"?{request.url.query}" if request.url.query else ""

    # Log the incoming request
    logger.info(f"[{request_id}] → {method} {url}{query} | user={username}")

    # Record start time — used to compute execution duration
    start = time.perf_counter()

    try:
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        # Choose log level based on status code
        level = logging.INFO if response.status_code < 400 else logging.WARNING
        if response.status_code >= 500:
            level = logging.ERROR

        logger.log(
            level,
            f"[{request_id}] ← {response.status_code} | "
            f"{method} {url} | user={username} | {duration_ms:.1f}ms",
        )

        # Attach request ID to response headers for frontend tracing
        response.headers["X-Request-ID"] = request_id
        return response

    except Exception as exc:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.error(
            f"[{request_id}] ✕ UNHANDLED EXCEPTION | "
            f"{method} {url} | user={username} | "
            f"{duration_ms:.1f}ms | error={exc!r}"
        )
        raise
