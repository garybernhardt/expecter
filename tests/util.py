def fail_msg(callable_):
    try:
        callable_()
    except Exception,e :
        return str(e)

