# File: unit_tests/unit_tests_db/abstract_unit_test_db.py

"""
AbstractUnitTestDB exists as an intermediate base class between AbstractUnitTest
and any unit test classes that are specific to the database layer.

Its primary purpose is to configure a dedicated log output path for all DB-related
tests. By appending 'db' to the standard unit test logging root folder, it ensures
that logs from database-specific unit tests are clearly separated from other test domains
(e.g., benchmark, training, core logic).

This keeps the log structure clean, and avoids the need to duplicate log path setup
in every DB-related test class.
"""

import os
from unit_tests.abstract_unit_test import AbstractUnitTest

class AbstractUnitTestDB(AbstractUnitTest):
    def __init__(self):
        super().__init__()
        self.LOG_FOLDER_PATH = os.path.join(self.LOG_FOLDER_PATH, "db")

