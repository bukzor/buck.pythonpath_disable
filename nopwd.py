from __future__ import print_function
# TODO:
# - [ ] enable PYTHONPATH_DISABLE=x:y environment var
# find out if this is called more than once per path entry
# wrie tests
from os import stat
from os.path import samestat, abspath
import sys

print('BEFORE:')
for p in sys.path:
    print('   ', p)

if False:
    sys.path[:] = [
        '/usr/lib/python3.4',
        '/home/buck/venv/py34/lib/python3.4/site-packages',
        '/home/buck/venv/py34/lib/python3.4/lib-dynload',
    ]
    print('AFTER:')
    for p in sys.path:
        print('   ', p)
    print('END.')

print('metapath:')
for p in sys.meta_path:
    print('   ', p)


def disable(path):
    path = stat(path)

    class NoisyFinder(object):
        def __init__(self, syspath):
            print('SYSPATH:', syspath)
            for syspath in sys.path[:]:
                try:
                    pstat = stat(abspath(syspath))
                except OSError:
                    continue
                if samestat(pstat, path):
                    print('Removing:', repr(syspath))
                    sys.path.remove(syspath)
            raise ImportError
    return NoisyFinder


def register(hook):
    import sys
    sys.path_hooks.insert(0, hook)
    sys.path_importer_cache.clear()


def disable_pwd_syspath():
    register(disable('.'))
