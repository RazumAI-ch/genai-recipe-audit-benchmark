# File: utils/prompt_helpers.py

import psycopg2.extras
from db.core.connection import get_db_connection


def get_deviation_section_from_db() -> str:
    """
    Dynamically constructs the deviation classification section using all available fields.
    Automatically adapts to added fields like 'explanation', 'gxp_principle', etc.
    """

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM deviation_types ORDER BY severity, id")
            rows = cur.fetchall()
    finally:
        conn.close()

    # Determine which fields to include (exclude system columns)
    excluded = {"id", "created_at"}
    included_fields = [key for key in rows[0].keys() if key not in excluded]

    # Group by severity
    grouped = {"critical": [], "major": [], "minor": []}
    for row in rows:
        severity = row.get("severity", "unspecified").lower()
        if severity not in grouped:
            grouped[severity] = []

        # Build multi-line description per deviation
        parts = [f"**{row.get('type', 'UNKNOWN')}**"]
        for field in included_fields:
            if field != "type" and field in row and row[field]:
                label = field.replace("_", " ").capitalize()
                parts.append(f"  - {label}: {row[field]}")

        grouped[severity].append("\n".join(parts))

    # Build output
    lines = []
    for severity in ["critical", "major", "minor"]:
        if grouped[severity]:
            lines.append(f"- **{severity.capitalize()}**")
            lines.extend(grouped[severity])
            lines.append("")

    return "\n".join(lines)