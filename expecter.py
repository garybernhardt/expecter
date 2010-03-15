__all__ = ['expect']


class expect:
    def __init__(self, actual):
        self._actual = actual

    def __eq__(self, other):
        assert self._actual == other, (
            'Expected %s but got %s' % (repr(other), repr(self._actual)))
        return self

    def __ne__(self, other):
        assert self._actual != other, (
            'Expected anything except %s but got it' % repr(self._actual))
        return self

    def __lt__(self, other):
        assert self._actual < other, (
            'Expected something less than %s but got %s'
            % (repr(other), repr(self._actual)))
        return self

    def __gt__(self, other):
        assert self._actual > other, (
            'Expected something greater than %s but got %s'
            % (repr(other), repr(self._actual)))
        return self

    def __le__(self, other):
        assert self._actual <= other, (
            'Expected something less than or equal to %s but got %s'
            % (repr(other), repr(self._actual)))
        return self

    def __ge__(self, other):
        assert self._actual >= other, (
            'Expected something greater than or equal to %s but got %s'
            % (repr(other), repr(self._actual)))
        return self

    def __repr__(self):
        return 'expect(%s)' % repr(self._actual)

    def isinstance(self, expected_cls):
        assert isinstance(self._actual, expected_cls), (
            'Expected an instance of %s but got an instance of %s' % (
                expected_cls.__name__, self._actual.__class__.__name__))

    @staticmethod
    def raises(cls=Exception, message=None):
        return _RaisesExpectation(cls, message)


class _RaisesExpectation:
    def __init__(self, exception_class, message):
        self._exception_class = exception_class
        self.message = message

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        success = not exc_type
        if success:
            raise AssertionError(
                'Expected an exception of type %s but got none'
                % self._exception_class.__name__)
        else:
            return self.validate_failure(exc_type, exc_value)

    def validate_failure(self, exc_type, exc_value):
        no_exception_was_raised = not exc_type
        wrong_message_was_raised = (self.message and
                                    self.message != str(exc_value))
        if wrong_message_was_raised:
            raise AssertionError(
                "Expected %s('%s') but got %s('%s')" %
                 (self._exception_class.__name__,
                  str(self.message),
                  exc_type.__name__,
                  str(exc_value)))
        elif issubclass(exc_type, self._exception_class):
            return True
        else:
            pass

