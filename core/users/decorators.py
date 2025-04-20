"""Define the decorators to manage the roles of the users."""

from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(f):
    """Define the decorator to check if a user has admin privileges."""

    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, "is_admin", False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)

    return decorated_function
