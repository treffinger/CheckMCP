import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._reset_singletons()

    def tearDown(self):
        self._reset_singletons()

    def _reset_singletons(self):
        from config.config_loader import ConfigLoader
        from cmk_client.cmk_client import CmkClient

        ConfigLoader.config = None
        CmkClient._instance = None
        CmkClient._initialized = False
