from typing import Callable
import functools
import json

from .redis_client import redis


def cacher(ttl: int = 3600):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"cache:{func.__name__}"

            cached = await redis.get(key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            await redis.set(key, json.dumps(result), ex=ttl)

            return result
        return wrapper
    return decorator