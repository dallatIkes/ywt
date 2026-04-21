import logging
import time
import functools
from typing import Callable

logger = logging.getLogger("ywt.service")


def log_service_call(operation: str | None = None):
    """AOP decorator — logs service method calls with timing and outcome.

    Usage:
        @log_service_call()
        def send_reco(self, data, sender): ...

        @log_service_call("custom operation name")
        def create_user(self, data): ...

    Logs:
        - Operation name (method name or custom label)
        - Key arguments (first non-self argument)
        - Execution time
        - Success or exception raised
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Resolve operation name — use provided label or method name
            op_name = operation or func.__name__

            # Extract a meaningful context from args
            # args[0] = self, args[1] = first meaningful arg
            context = _extract_context(args, kwargs)

            start = time.perf_counter()

            logger.info(f"[SERVICE] {op_name} started | {context}")

            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                logger.info(
                    f"[SERVICE] {op_name} completed | "
                    f"{context} | {duration_ms:.1f}ms"
                )
                return result

            except Exception as exc:
                duration_ms = (time.perf_counter() - start) * 1000
                logger.warning(
                    f"[SERVICE] {op_name} failed | "
                    f"{context} | {duration_ms:.1f}ms | "
                    f"reason={type(exc).__name__}: {exc}"
                )
                # Re-raise — decorator never swallows exceptions
                raise

        return wrapper

    return decorator


def _extract_context(args: tuple, kwargs: dict) -> str:
    """Build a readable context string from method arguments.
    Skips 'self' (args[0]) and extracts meaningful identifiers.
    """
    parts = []

    # args[1] is the first real argument after self
    if len(args) > 1:
        first_arg = args[1]
        context = _describe(first_arg)
        if context:
            parts.append(context)

    # Named kwargs — skip db sessions and repos
    for key, val in kwargs.items():
        if key in ("db", "session", "repo"):
            continue
        parts.append(f"{key}={_describe(val)}")

    return " | ".join(parts) if parts else "no context"


def _describe(obj) -> str:
    """Extract a readable identifier from an object."""
    # Pydantic schema — show its fields
    if hasattr(obj, "model_dump"):
        data = obj.model_dump()
        # Never log passwords
        data.pop("password", None)
        data.pop("hashed_password", None)
        return str(data)

    # SQLAlchemy User model — show username
    if hasattr(obj, "username"):
        return f"user={obj.username}"

    # String or int — show directly
    if isinstance(obj, (str, int)):
        return str(obj)

    return type(obj).__name__
