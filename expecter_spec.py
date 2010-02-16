from __future__ import with_statement
import doctest

from expecter import expect


def describe_expecter():
    def expects_equals():
        expect(2) == 1 + 1
        assert raises(AssertionError, lambda: expect(1) == 2)

    def expects_not_equals():
        expect(1) != 2
        assert raises(AssertionError, lambda: expect(1) != 1)

    def expects_less_than():
        expect(1) < 2
        assert raises(AssertionError, lambda: expect(1) < 1)

    def expects_greater_than():
        expect(2) > 1
        assert raises(AssertionError, lambda: expect(1) > 1)

    def expects_less_than_or_equal():
        expect(1) <= 1
        expect(1) <= 2
        assert raises(AssertionError, lambda: expect(2) <= 1)

    def expects_greater_than_or_equal():
        expect(1) >= 1
        expect(2) >= 1
        assert raises(AssertionError, lambda: expect(1) >= 2)

    def describe_when_expecting_exceptions():
        def swallows_expected_exceptions_to_be_raised():
            with expect.raises(KeyError):
                raise KeyError

        def requires_exceptions_to_be_raised():
            def _expects_raise_but_doesnt_get_it():
                with expect.raises(KeyError):
                    pass
            assert raises(AssertionError, _expects_raise_but_doesnt_get_it)

        def does_not_swallow_exceptions_of_the_wrong_type():
            def _expects_key_error_but_gets_value_error():
                with expect.raises(KeyError):
                    raise ValueError
            assert raises(ValueError, _expects_key_error_but_gets_value_error)

def describe_readme():
    def passes_tests():
        doctest.testfile('README', module_relative=False)

