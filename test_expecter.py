from __future__ import with_statement
import doctest
from nose.tools import assert_raises

from expecter import expect, add_expectation, clear_expectations


def fail_msg(callable_):
    try:
        callable_()
    except Exception,e :
        return str(e)


class describe_expecter:
    def it_expects_equals(self):
        expect(2) == 1 + 1
        def _fails(): expect(1) == 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected 2 but got 1'

    def it_expects_not_equals(self):
        expect(1) != 2
        def _fails(): expect(1) != 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected anything except 1 but got it'

    def it_expects_less_than(self):
        expect(1) < 2
        def _fails(): expect(1) < 0
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected something less than 0 but got 1'

    def it_expects_greater_than(self):
        expect(2) > 1
        def _fails(): expect(0) > 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than 1 but got 0')

    def it_expects_less_than_or_equal(self):
        expect(1) <= 1
        expect(1) <= 2
        def _fails(): expect(2) <= 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something less than or equal to 1 but got 2')

    def it_expects_greater_than_or_equal(self):
        expect(1) >= 1
        expect(2) >= 1
        def _fails(): expect(1) >= 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than or equal to 2 but got 1')

    def it_can_chain_comparison_expectations(self):
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

    def it_expects_isinstance(self):
        expect(1).isinstance(int)
        def _fails():
            expect(1).isinstance(str)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected an instance of str but got an instance of int')


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


class describe_custom_matchers:
    def is_a_potato(self, object):
        return object == 'potato'

    def setup(self):
        add_expectation(self.is_a_potato)

    def teardown(self):
        clear_expectations()

    def they_can_succeed(self):
        expect('potato').is_a_potato()

    def they_can_fail(self):
        def _fails():
            expect('not a potato').is_a_potato()
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected that 'not a potato' is_a_potato, but it wasn't")

    def they_can_be_cleared(self):
        clear_expectations()
        assert_raises(AttributeError, lambda: expect('potato').is_a_potato)


class describe_readme:
    def it_passes_as_a_doctest(self):
        doctest.testfile('README', module_relative=False)

