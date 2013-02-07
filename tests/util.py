try:
    import builtins as __builtins__
except ImportError:
    import __builtin__ as __builtins__

str = getattr(__builtins__, 'unicode', str)

def fail_msg(callable_):
    try:
        callable_()
    except Exception as e:
        return str(e)

