from __future__ import print_function
from os import stat
from os.path import samestat


def disable(path):
    path = stat(path)

    class Disable(object):
        def __init__(self, syspath):
            print('SYSPATH:', syspath)
            syspath = stat(syspath)
            if samestat(syspath, path):
                print('HIT1')
                return
            else:
                raise ImportError

        @staticmethod
        def find_module(dummy_module):
            print('MODULE:', dummy_module)
            if dummy_module.startswith('asottile'):
                print('HIT2')
            # This finder never finds anything.
            return None
    return Disable


def register(hook):
    import sys
    sys.path_hooks.insert(0, hook)
    sys.path_importer_cache.clear()


def disable_pwd_syspath():
    register(disable('.'))
