from nose.tools import assert_raises

from tests.util import fail_msg
from expecter import expect, add_expectation, clear_expectations


class describe_custom_matchers:
    def is_a_potato(self, thing):
        return thing == 'potato'

    def teardown(self):
        clear_expectations()

    def they_can_succeed(self):
        add_expectation(self.is_a_potato)
        expect('potato').is_a_potato()

    def they_can_fail(self):
        add_expectation(self.is_a_potato)
        def _fails():
            expect('not a potato').is_a_potato()
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected that 'not a potato' is_a_potato, but it isn't")

    def they_adjust_failure_message_for_expectation_name(self):
        def can_do_something(thing): return False
        def will_do_something(thing): return False

        for predicate in [can_do_something, will_do_something]:
            add_expectation(predicate)

        assert fail_msg(expect('walrus').can_do_something) == (
            "Expected that 'walrus' can_do_something, but it can't")
        assert fail_msg(expect('walrus').will_do_something) == (
            "Expected that 'walrus' will_do_something, but it won't")

    def they_have_default_failure_message(self):
        def predicate_with_bad_name(thing): return False
        add_expectation(predicate_with_bad_name)
        assert fail_msg(expect('walrus').predicate_with_bad_name) == (
            "Expected that 'walrus' predicate_with_bad_name, but got False")

    def they_can_be_cleared(self):
        clear_expectations()
        assert_raises(AttributeError, lambda: expect('potato').is_a_potato)

