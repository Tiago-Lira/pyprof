import os
import pickle
import functools
from collections import defaultdict

from line_profiler import LineProfiler, show_text

from pyprof.utils import (
    get_paths,
    join_path,
)


def clear_stats(path=None):
    for file_path in get_paths(path=path):
        os.remove(file_path)


def print_stats(path=None):
    for file_path in get_paths(path=path):
        stats = pickle.load(open(file_path, 'rb'))
        show_text(stats.timings, stats.unit)


class Profile:

    def __init__(self):
        self._registry = defaultdict(list)
        self._globals = []

    def __call__(self, *args, **kwargs):
        return self.prof(*args, **kwargs)

    def prof(self, name_or_fn=None, save=False):
        if hasattr(name_or_fn, '__call__'):
            return self._prof(name_or_fn)

        def _inner(fn):
            return self._prof(fn, name=name_or_fn, save=save)
        return _inner

    def _prof(self, fn, name=None, save=False):
        name = name or '{}.{}'.format(fn.__module__, fn.__name__)

        @functools.wraps(fn)
        def _inner(*args, **kwargs):
            prof = LineProfiler()
            [prof(include) for include in self._globals]
            [prof(include) for include in self._registry[name]]
            ret = prof(fn)(*args, **kwargs)
            if save:
                prof.dump_stats(join_path(name))
            else:
                prof.print_stats()
            return ret

        return _inner

    def include(self, name_or_fn=None):
        if hasattr(name_or_fn, '__call__'):
            return self._include(name_or_fn)

        def _inner(fn):
            return self._include(fn, name=name_or_fn)
        return _inner

    def _include(self, fn, name=None):
        if name is None:
            self._globals.append(fn)
        else:
            self._registry[name].append(fn)
        return fn

    def timing(self, fn=None, *args, **kwargs):
        if hasattr(fn, '__call__'):
            return self._timing(fn)

        def _inner(fn):
            return self._timing(fn, *args, **kwargs)
        return _inner

    def _timing(self, fn, num=10, verbose=0, unit='ms'):

        @functools.wraps(fn)
        def _inner(*args, **kwargs):
            from timerit import Timerit
            timer = Timerit(num=num, verbose=verbose, unit=unit)
            for t1 in timer:
                with t1:
                    result = fn(*args, **kwargs)
            print(t1.report())
            return result

        return _inner


profile = Profile()
