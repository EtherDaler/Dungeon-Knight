from functools import wraps


def threadpool_decorator(func):
     @wraps(func)
     def wrapper(*args_, **kwargs_):
         import threading
         func_thread = threading.Thread(target=func,
                                        args=tuple(args_),
                                        kwargs=kwargs_)
         func_thread.start()
         return func_thread
     return wrapper