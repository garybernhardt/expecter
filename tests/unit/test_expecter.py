from __future__ import with_statement
from nose.tools import assert_raises

from tests.util import fail_msg
from expecter import expect


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

    def it_expects_isintance_multi(self):
        expect('str').isinstance((str, bytes))
        def _fails():
            expect('str').isinstance((int, long))
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected an instance of int or long but got an instance of str')

    def it_expects_containment(self):
        expect([1]).contains(1)
        def _fails():
            expect([2]).contains(1)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected [2] to contain 1 but it didn't")

    def it_expects_non_containment(self):
        expect([1]).does_not_contain(0)
        def _fails():
            expect([1]).does_not_contain(1)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected [1] to not contain 1 but it did")
