import os
import sys

os.environ.setdefault("CONFIG_PATH", "/tmp/test_config.yml")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
