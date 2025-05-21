#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test runner for the ru_accent_poet package.
Run this script to execute all tests.
"""

import os
import sys
import unittest
import pytest

# Suppress TensorFlow warnings during tests
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def run_tests():
    """Run all tests using unittest or pytest."""
    print("Running ru_accent_poet test suite...")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        # Use unittest
        print("Using unittest framework")
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(test_suite)
        return 0 if result.wasSuccessful() else 1
    else:
        # Use pytest by default
        print("Using pytest framework")
        return pytest.main(["-v"])

if __name__ == "__main__":
    sys.exit(run_tests())