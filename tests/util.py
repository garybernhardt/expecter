def fail_msg(callable_):
    try:
        callable_()
    except Exception as e:
        return unicode(e)

