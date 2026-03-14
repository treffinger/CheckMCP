import os
import sys
import unittest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
os.environ.setdefault("CONFIG_PATH", "/tmp/test_config.yml")

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
