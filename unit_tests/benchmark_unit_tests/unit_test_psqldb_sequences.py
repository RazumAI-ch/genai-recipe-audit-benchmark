# File: unit_tests/benchmark_unit_tests/unit_test_psqldb_sequences.py

from unit_tests.abstract_unit_test import AbstractUnitTest
import config.keys_unit_tests as tests
import unit_tests.db.psqldb_sequences as db_psqldb_sequences

class UnitTestPSQLDBSequences(AbstractUnitTest):
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