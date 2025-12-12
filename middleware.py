from flask import session, redirect
from functools import wraps

def require_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        uid = session.get('user_id')
        if uid is None:
            return redirect('/login')
        return f(uid, *args, **kwargs)
    return wrapper

def require_self(target_id_arg):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            uid = session.get('user_id')
            if uid is None:
                return redirect('/login')
            target = kwargs.get(target_id_arg)
            if target is None:
                return "Bad Request", 400
            if int(uid) != int(target):
                return "Forbidden", 400
            return func(uid, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            return redirect('/admin/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
