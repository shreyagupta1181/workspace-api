import time

from fastapi import HTTPException, Request, status

from app.core.redis import redis_client


def check_rate_limit(
    request: Request,
    action: str,
    limit: int,
    window: int = 60,
):
    client_ip = request.client.host if request.client else "unknown"

    key = f"rate_limit:{action}:{client_ip}"

    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.set(key, 1, ex=window)
        return

    if int(current_count) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many {action} attempts. Try again later.",
            headers={"Retry-After": str(window)},
        )

    redis_client.incr(key)