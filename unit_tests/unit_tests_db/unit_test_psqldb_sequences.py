# File: unit_tests/unit_tests_db/unit_test_psqldb_sequences.py

import config.keys.keys_unit_tests as tests
import unit_tests.utils_db.psqldb_sequences as db_psqldb_sequences
from unit_tests.unit_tests_db.abstract_unit_test_db import AbstractUnitTestDB


class UnitTestPSQLDBSequences(AbstractUnitTestDB):
    """
    Verifies that PostgreSQL sequences are initialized correctly.
    Sequence last_value must be ≥ MAX(id) + 1.
    """

    KEY = tests.UNIT_TEST_PSQLDB_SEQUENCES

    def run(self) -> None:
        mismatches = db_psqldb_sequences.get_sequence_mismatches()

        if mismatches:
            formatted = [f"{m['sequence_name']} (last_value={m['last_value']} < max_id+1={m['expected_min']})"
                         for m in mismatches]
            raise AssertionError("Sequences out of sync:\n  " + "\n  ".join(formatted))