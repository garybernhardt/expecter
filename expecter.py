class expect:
    def __init__(self, value):
        self._value = value

    def __eq__(self, other):
        assert self._value == other

    def __ne__(self, other):
        assert self._value != other

    def __lt__(self, other):
        assert self._value < other

    def __gt__(self, other):
        assert self._value > other

    def __le__(self, other):
        assert self._value <= other

    def __ge__(self, other):
        assert self._value >= other

    @staticmethod
    def raises(cls):
        return _RaisesExpectation(cls)

class _RaisesExpectation:
    def __init__(self, exception_class):
        self._exception_class = exception_class

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        no_exception_was_raised = not exc_type
        if exc_type is self._exception_class:
            return True
        elif no_exception_was_raised:
            raise AssertionError(
                'Expected an exception of type %s but got none'
                % self._exception_class.__name__)
        else:
            pass

