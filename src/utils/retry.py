import asyncio
from functools import wraps
from typing import Any, Callable, TypeVar
from ..config.settings import RETRY_ATTEMPTS, RETRY_DELAY

T = TypeVar('T')

def with_retry(max_attempts: int = RETRY_ATTEMPTS, delay: int = RETRY_DELAY):
    """Decorator for retrying async functions with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        await asyncio.sleep(wait_time)
            
            raise last_exception
        
        return wrapper
    return decorator 