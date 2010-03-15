from __future__ import with_statement
import doctest
from nose.tools import assert_raises

from expecter import expect


def fail_msg(callable_):
    try:
        callable_()
    except Exception,e :
        return str(e)


def describe_expecter():
    def expects_equals():
        expect(2) == 1 + 1
        def _fails(): expect(1) == 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected 2 but got 1'

    def expects_not_equals():
        expect(1) != 2
        def _fails(): expect(1) != 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected anything except 1 but got it'

    def expects_less_than():
        expect(1) < 2
        def _fails(): expect(1) < 0
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected something less than 0 but got 1'

    def expects_greater_than():
        expect(2) > 1
        def _fails(): expect(0) > 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than 1 but got 0')

    def expects_less_than_or_equal():
        expect(1) <= 1
        expect(1) <= 2
        def _fails(): expect(2) <= 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something less than or equal to 1 but got 2')

    def expects_greater_than_or_equal():
        expect(1) >= 1
        expect(2) >= 1
        def _fails(): expect(1) >= 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than or equal to 2 but got 1')

    def can_chain_comparison_expectations():
        # In each of these chains, the first expectation passes and the second
        # fails. This forces the first expectation to return self.
        failing_chains = [lambda: 1 == expect(1) != 1,
                          lambda: 1 != expect(2) != 2,
                          lambda: 1 < expect(2) != 2,
                          lambda: 1 > expect(0) != 0,
                          lambda: 1 <= expect(1) != 1,
                          lambda: 1 >= expect(1) != 1]
        for chain in failing_chains:
            assert_raises(AssertionError, chain)

        # Mote bug: if we leave the lambda in a local variable, it will try to
        # run it as a spec.
        del chain

    def expects_isinstance():
        expect(1).isinstance(int)
        def _fails(): expect(1).isinstance(str)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected an instance of str but got an instance of int')

    def describe_when_expecting_exceptions():
        def swallows_expected_exceptions():
            with expect.raises(KeyError):
                raise KeyError

        def requires_exceptions_to_be_raised():
            def _expects_raise_but_doesnt_get_it():
                with expect.raises(KeyError):
                    pass
            assert_raises(AssertionError, _expects_raise_but_doesnt_get_it)
            assert fail_msg(_expects_raise_but_doesnt_get_it) == (
                'Expected an exception of type KeyError but got none')

        def does_not_swallow_exceptions_of_the_wrong_type():
            def _expects_key_error_but_gets_value_error():
                with expect.raises(KeyError):
                    raise ValueError
            assert_raises(ValueError, _expects_key_error_but_gets_value_error)

        def can_expect_any_exception():
            with expect.raises():
                raise ValueError

        def can_expect_failure_messages():
            with expect.raises(ValueError, 'my message'):
                raise ValueError('my message')

        def can_require_failure_messages():
            def _fails():
                with expect.raises(ValueError, 'my message'):
                    raise ValueError('wrong message')
            assert_raises(AssertionError, _fails)
            assert fail_msg(_fails) == (
                "Expected ValueError('my message') but got ValueError('wrong message')")

def describe_readme():
    def passes_as_a_doctest():
        doctest.testfile('README', module_relative=False)

