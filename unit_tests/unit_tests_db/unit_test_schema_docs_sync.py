# File: unit_tests/unit_tests_db/unit_test_schema_docs_sync.py

from unit_tests.unit_tests_db.abstract_unit_test_db import AbstractUnitTestDB
import config.keys.keys_unit_tests as keys
import unit_tests.utils_db.schema_docs as schema_docs

class UnitTestSchemaDocsSync(AbstractUnitTestDB):
    KEY = keys.UNIT_TEST_SCHEMA_DOCS_SYNC

    def run(self) -> None:
        db_columns = schema_docs.get_all_columns()
        documented_columns = schema_docs.get_documented_columns()

        missing_docs = db_columns - documented_columns
        obsolete_docs = documented_columns - db_columns

        if missing_docs:
            raise AssertionError(f"Missing documentation for: {sorted(missing_docs)}")
        if obsolete_docs:
            raise AssertionError(f"Obsolete documentation for non-existent columns: {sorted(obsolete_docs)}")