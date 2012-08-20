BASICS
======

Expecter Gadget helps you to write assertions. Never again will you forget
which is expected and which is actual!

Basic expectations are easy:

    >>> from expecter import expect
    >>> expect('some' + 'thing') == 'something'
    expect('something')
    >>> expect(1) > 100
    Traceback (most recent call last):
    ...
    AssertionError: Expected something greater than 100 but got 1

Just read the expectations like a sentence. "expect(2) == 1 + 1" reads as
"Expect 2 to equal 1 + 1". Obviously, the expectation is about 2, and it's
being compared to 1 + 1. No ambiguity!

EXCEPTIONS
==========

Expectations about exceptions use the "with" statement. Everything is good if
the expected exception is raised:

    >>> from __future__ import with_statement
    >>> with expect.raises(KeyError):
    ...     {}[123]

If it's not raised, Expecter Gadget will raise an AssertionError:

    >>> with expect.raises(KeyError):
    ...     pass
    Traceback (most recent call last):
    ...
    AssertionError: Expected an exception of type KeyError but got none

Exceptions that don't match the expected one will not be swallowed, so your
test will error as you expect:

    >>> from __future__ import with_statement
    >>> with expect.raises(NameError):
    ...     {}[123]
    Traceback (most recent call last):
    ...
    KeyError: 123

CUSTOM EXPECTATIONS
===================

You can add a custom expectation with the add\_expectation method. You give it
a predicate that should return true if the expectation succeeds and false if
it fails. All expectation objects will grow a method with the name of your
predicate method (so don't use a lambda). Appropriate exception messages will
be generated when your predicate fails:

    >>> import expecter
    >>> def can_meow(thing):
    ...     return thing == 'kitty'
    >>> expecter.add_expectation(can_meow)
    >>> expect('kitty').can_meow()
    >>> expect('puppy').can_meow()
    Traceback (most recent call last):
    ...
    AssertionError: Expected that 'puppy' can_meow, but it can't

API DOCUMENTATION
=================

See http://expecter-gadget.readthedocs.org/en/latest/

