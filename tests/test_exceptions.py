from nose.tools import assert_raises

from tests.util import fail_msg
from expecter import expect


class describe_expecter_when_expecting_exceptions():
    def it_swallows_expected_exceptions(self):
        with expect.raises(KeyError):
            raise KeyError

    def it_requires_exceptions_to_be_raised(self):
        def _expects_raise_but_doesnt_get_it():
            with expect.raises(KeyError):
                pass
        assert_raises(AssertionError, _expects_raise_but_doesnt_get_it)
        assert fail_msg(_expects_raise_but_doesnt_get_it) == (
            'Expected an exception of type KeyError but got none')

    def it_does_not_swallow_exceptions_of_the_wrong_type(self):
        def _expects_key_error_but_gets_value_error():
            with expect.raises(KeyError):
                raise ValueError
        assert_raises(ValueError, _expects_key_error_but_gets_value_error)

    def it_can_expect_any_exception(self):
        with expect.raises():
            raise ValueError

    def it_can_expect_failure_messages(self):
        with expect.raises(ValueError, 'my message'):
            raise ValueError('my message')

    def it_can_require_failure_messages(self):
        def _fails():
            with expect.raises(ValueError, 'my message'):
                raise ValueError('wrong message')
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected ValueError('my message') but got ValueError('wrong message')")

