# vim: set fileencoding=utf-8 :
from __future__ import unicode_literals
from nose.tools import assert_raises

from tests.util import fail_msg
from expecter import expect

try:
    import builtins as __builtins__
except ImportError:
    import __builtin__ as __builtins__

unicode = getattr(__builtins__, 'unicode', str)

class describe_expecter:
    def it_shows_diff_when_unicode_strings_differ(self):
        value = 'ueber\ngeek'
        fixture = 'über\ngeek'
        assert isinstance(value, unicode), "value is a " + repr(type(value))
        assert isinstance(fixture, unicode), "fixture is a " + repr(type(fixture))
        def _fails(): expect(value) == fixture
        assert_raises(AssertionError, _fails)
        msg = ("Expected 'über\\ngeek' but got 'ueber\\ngeek'\n"
               "Diff:\n"
               "@@ -1,2 +1,2 @@\n"
               "-über\n"
               "+ueber\n"
               " geek"
               )
        #normalize real msg for differences in py2 and py3
        real = fail_msg(_fails).replace("u'", "'").replace(
                '\\xfc', '\xfc')
        assert  real == msg, '\n' + repr(real) + '\n' + repr(msg)

