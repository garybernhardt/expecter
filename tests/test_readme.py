import doctest


class describe_readme:
    def it_passes_as_a_doctest(self):
        test_results = doctest.testfile('README.markdown', module_relative=False)
        assert not test_results.failed

