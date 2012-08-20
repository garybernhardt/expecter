from subprocess import check_call
from os.path import join, dirname


class describe_docs:
    def they_build_cleanly(self):
        docs_dir = join(dirname(__file__), "..", "..", "docs")
        command = "(cd %s && make html) > /dev/null" % docs_dir
        check_call(command, shell=True)

