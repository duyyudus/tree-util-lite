import sys
import unittest
from pathlib2 import Path

# Append parent directory of `binary_vcs_lite` package
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from tree_util_lite.common.util import *

from tree_util_lite.core import tree

TEST_ROOT = Path(__file__).resolve().parent.parent


def start_log_test(testcase_path):
    message = '[START TEST] :: {}'.format(testcase_path)
    exe = 'Python interpreter: {}'.format(sys.executable)
    print('')
    print('#' * len(message))
    print('#' * len(message))
    print(message)
    print(exe)
    print('')


def end_log_test(testcase_path):
    message = '[END TEST] :: {}'.format(testcase_path)
    exe = 'Python interpreter: {}'.format(sys.executable)
    print('')
    print(exe)
    print(message)
    print('#' * len(message))
    print('#' * len(message))
    print('')


def log_test(testcase_path):
    def _log_test(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            switch_log(0)
            start_log_test(testcase_path)
            func(*args, **kwargs)
            end_log_test(testcase_path)
        return wrapper
    return _log_test


if __name__ == '__main__':
    pass
