from functools import wraps

from copier.error import NeglectableError


def neglectable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise NeglectableError(e)

    return wrapper
