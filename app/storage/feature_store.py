from pathlib import Path
import duckdb


DB_PATH = "data/fifa_runner.duckdb"


def get_connection():
    Path("data").mkdir(parents=True, exist_ok=True)
    return duckdb.connect(DB_PATH)


def init_db():
    con = get_connection()

    con.execute("""
        CREATE TABLE IF NOT EXISTS run_manifest (
            run_id VARCHAR,
            fixture VARCHAR,
            prediction_mode VARCHAR,
            status VARCHAR,
            verdict VARCHAR,
            feature_vector_hash VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS source_manifest (
            run_id VARCHAR,
            source_name VARCHAR,
            source_type VARCHAR,
            source_url VARCHAR,
            extraction_method VARCHAR,
            records_extracted INTEGER,
            status VARCHAR,
            sha256 VARCHAR,
            size_bytes BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS artefacts (
            run_id VARCHAR,
            artefact_name VARCHAR,
            artefact_path VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.close()


def save_run_manifest(run_id, fixture, prediction_mode, status, verdict, feature_vector_hash):
    con = get_connection()
    con.execute(
        """
        INSERT INTO run_manifest
        (run_id, fixture, prediction_mode, status, verdict, feature_vector_hash)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [run_id, fixture, prediction_mode, status, verdict, feature_vector_hash],
    )
    con.close()


def save_sources(run_id, sources):
    con = get_connection()

    for source in sources:
        con.execute(
            """
            INSERT INTO source_manifest
            (run_id, source_name, source_type, source_url, extraction_method,
             records_extracted, status, sha256, size_bytes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                run_id,
                source.get("source_name"),
                source.get("source_type"),
                source.get("source_url"),
                source.get("extraction_method"),
                source.get("records_extracted", 0),
                source.get("status"),
                source.get("sha256"),
                source.get("size_bytes"),
            ],
        )

    con.close()


def save_artefact(run_id, artefact_name, artefact_path):
    con = get_connection()
    con.execute(
        """
        INSERT INTO artefacts
        (run_id, artefact_name, artefact_path)
        VALUES (?, ?, ?)
        """,
        [run_id, artefact_name, artefact_path],
    )
    con.close()