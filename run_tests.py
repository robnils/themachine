import itertools

import os
from nose.loader import TestLoader
from nose import run
from nose.suite import LazySuite

dir_path = os.path.dirname(os.path.realpath(__file__))
folders = ("tests",)
paths = [os.path.join(dir_path, f) for f in folders]

FAST_TESTS = True

def run_tests():
    all_tests = ()
    for path in paths:
        all_tests = itertools.chain(all_tests, TestLoader().loadTestsFromDir(path))
    suite = LazySuite(all_tests)
    run(suite=suite)

if __name__ == '__main__':
    run_tests()


