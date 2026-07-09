from datetime import datetime, timezone
from pathlib import Path
import json


def build_source_manifest(run_id: str, fixture: str, sources: list):
    manifest = {
        "run_id": run_id,
        "fixture": fixture,
        "prediction_mode": "pre_match",
        "retrieval_timestamp": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
    }

    out = Path("data/manifests")
    out.mkdir(parents=True, exist_ok=True)

    manifest_path = out / f"{run_id}_source_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    return str(manifest_path)