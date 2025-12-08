import unittest
import os
import sys

def run_tests():
    # Add current directory to path so we can import modules
    sys.path.append(os.getcwd())
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    if not os.path.exists(start_dir) and os.path.exists(os.path.join('QR', 'tests')):
        start_dir = os.path.join('QR', 'tests')
        
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed.")
        exit(1)

if __name__ == "__main__":
    run_tests()
