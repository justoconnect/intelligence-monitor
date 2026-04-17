"""Basic usage example for the Intelligence Monitor.

Run:
    python3 examples/basic_usage.py

This example shows how to (1) initialize the local SQLite store, (2) insert
a sample intelligence entry with deduplication, (3) query by category, and
(4) export the full dataset as JSON.

It is intentionally self-contained: no external dependencies.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "example_intelligence.db"


def init_db(db_path: Path) -> sqlite3.Connection:
    """Create the minimal intelligence schema if it does not exist."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS intelligence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_hash TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT,
            source TEXT,
            impact INTEGER CHECK (impact BETWEEN 1 AND 10),
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON intelligence(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_impact ON intelligence(impact)")
    conn.commit()
    return conn


def insert_entry(
    conn: sqlite3.Connection,
    *,
    category: str,
    title: str,
    summary: str,
    source: str,
    impact: int,
) -> bool:
    """Insert an entry, returning False if it was a duplicate."""
    payload = f"{category}|{title}|{summary}|{source}".encode("utf-8")
    content_hash = hashlib.sha256(payload).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute(
            "INSERT INTO intelligence (content_hash, category, title, summary, source, impact, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (content_hash, category, title, summary, source, impact, now),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def search_by_category(conn: sqlite3.Connection, category: str) -> list[dict]:
    cur = conn.execute(
        "SELECT id, category, title, summary, source, impact, created_at "
        "FROM intelligence WHERE category = ? ORDER BY impact DESC, created_at DESC",
        (category,),
    )
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def export_json(conn: sqlite3.Connection, out_path: Path) -> int:
    cur = conn.execute("SELECT * FROM intelligence ORDER BY created_at DESC")
    cols = [c[0] for c in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(rows)


def main() -> None:
    conn = init_db(DB_PATH)
    inserted = insert_entry(
        conn,
        category="Transport (Gabon)",
        title="Nouveau chantier ferroviaire annonce sur la ligne Transgabonais",
        summary="Un plan de modernisation de la ligne Transgabonais a ete presente, incluant "
        "la rehabilitation de tronçons critiques et l'acquisition de nouveau materiel roulant.",
        source="https://example.test/gabon/transgabonais",
        impact=8,
    )
    print(f"Inserted new entry: {inserted}")

    # Second call with same payload must be deduplicated.
    duplicate = insert_entry(
        conn,
        category="Transport (Gabon)",
        title="Nouveau chantier ferroviaire annonce sur la ligne Transgabonais",
        summary="Un plan de modernisation de la ligne Transgabonais a ete presente, incluant "
        "la rehabilitation de tronçons critiques et l'acquisition de nouveau materiel roulant.",
        source="https://example.test/gabon/transgabonais",
        impact=8,
    )
    print(f"Duplicate was inserted again? {duplicate}  (expected False)")

    results = search_by_category(conn, "Transport (Gabon)")
    print(f"Entries in 'Transport (Gabon)': {len(results)}")
    for row in results:
        print(f"  - [impact={row['impact']}] {row['title']}")

    out = DB_PATH.with_suffix(".json")
    count = export_json(conn, out)
    print(f"Exported {count} entries to {out}")


if __name__ == "__main__":
    main()
