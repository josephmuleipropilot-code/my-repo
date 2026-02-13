def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

add(3, 4)