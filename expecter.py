__all__ = ['expect']


class expect(object):
    def __init__(self, actual):
        self._actual = actual

    def __getattr__(self, name):
        is_custom_expectation = name in _custom_expectations
        if is_custom_expectation:
            predicate = _custom_expectations[name]
            return CustomExpectation(predicate, self._actual)
        else:
            return getattr(super(expect, self), name)

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

    def contains(self, other):
        assert other in self._actual, (
            "Expected %s to contain %s but it didn't" % (
                repr(self._actual), repr(other)))

    def does_not_contain(self, other):
        assert other not in self._actual, (
            "Expected %s to not contain %s but it did" % (
                repr(self._actual), repr(other)))

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


class CustomExpectation:
    negative_verbs = {"can": "it can't",
                      "is": "it isn't",
                      "will": "it won't",
                     }

    def __init__(self, predicate, actual):
        self._predicate = predicate
        self._actual = actual

    def __call__(self):
        self.enforce()

    def enforce(self):
        if not self._predicate(self._actual):
            predicate_name = self._predicate.__name__
            raise AssertionError('Expected that %s %s, but %s' %
                                 (repr(self._actual),
                                  predicate_name,
                                  self._negative_verb()))

    def _negative_verb(self):
        # XXX: getting name in multiple places
        first_word_in_predicate = self._predicate.__name__.split('_')[0]
        try:
            return self.negative_verbs[first_word_in_predicate]
        except KeyError:
            return "got False"


_custom_expectations = {}


def add_expectation(predicate):
    _custom_expectations[predicate.__name__] = predicate


def clear_expectations():
    _custom_expectations.clear()

