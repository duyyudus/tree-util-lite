import sys
import os
import functools
import time
import json
import re
import random
import shutil

if sys.version_info[0] == 3:
    from pathlib import Path, PurePath
else:
    from pathlib2 import Path, PurePath
from pprint import pformat

from . import config

CFG_DICT = config.CFG_DICT

LOG_PREFIX = CFG_DICT['LOG_PREFIX']
LOG_ERROR_PREFIX = CFG_DICT['LOG_ERROR_PREFIX']
_log_on = 1


class TreeUtilError(Exception):
    """Base error for tree-related operations."""

    def __init__(self, message):
        super(TreeUtilError, self).__init__()
        self._message = message
        log_error('{}'.format(message))

    def __str__(self):
        return self._message


class InvalidType(TreeUtilError):
    """Invalid type."""


def _time_measure(func):
    """Measure running time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        log_info('Running time of {}() : {} seconds'.format(func.__name__, str(time.time() - st)))
        return ret
    return wrapper


def _log_message(args):
    def fstr(s):
        if type(s) is str:
            return s
        else:
            return '\n' + pformat(s)

    _log_indent = 0
    message = ''.join([fstr(a) for a in args])
    return (''.join([' ' for i in range(_log_indent * 4)]), message)


def log_info(*args):
    if not _log_on:
        return 0
    indent_str, message = _log_message(args)
    if not message:
        print('')
        return 0
    print('{} :: {}'.format(
        LOG_PREFIX,
        indent_str + message
    ))


def log_error(*args):
    if not _log_on:
        return 0
    indent_str, message = _log_message(args)
    if not message:
        print('')
        return 0
    print('{} {} :: {}'.format(
        LOG_PREFIX,
        LOG_ERROR_PREFIX,
        indent_str + message
    ))


def switch_log(is_on):
    global _log_on
    _log_on = is_on


def match_regex_pattern(input_str, patterns):
    for p in patterns:
        if re.findall(p, input_str):
            return 1


def load_json(json_path, verbose=0):
    """
    Args:
        json_path (str or Path):

    """

    json_path = Path(json_path)
    if not json_path.exists():
        if verbose:
            log_info('JSON not found: {}'.format(json_path))
        return {}

    with open(str(json_path), 'r') as f:
        if verbose:
            log_info('Loaded JSON: {}'.format(json_path))
        return json.loads(f.read())


def save_json(data, json_path, verbose=0):
    """
    Args:
        json_path (str or Path):

    """

    if not json_path.parent.exists():
        json_path.parent.mkdir(parents=1)
    with open(str(json_path), 'w') as f:
        f.write(json.dumps(data))
        if verbose:
            log_info('Saved JSON: {}'.format(json_path))


def check_type(obj, types, raise_exception=1):
    """Assert type of `obj`

    Args:
        obj:
        types (list): list of types/classes
    Raises:
        InvalidType:
    """

    if isinstance(obj, tuple(types)):
        return 1
    elif raise_exception:
        msg = '"{}" must be an instance of ({})'.format(str(obj), ', '.join([str(t) for t in types]))
        raise InvalidType(msg)
    else:
        return 0


def generate_id(size=8):
    alphabet = [c for c in 'abcdefghijklmnopqrstuvwxyz0123456789']
    return ''.join(random.sample(alphabet, size))
