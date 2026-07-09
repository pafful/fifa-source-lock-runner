

from pathlib import Path
from datetime import datetime, timezone
import json


def generate_feature_vector(run_id: str, fixture: str, sources: list):
    feature_vector = {
        "run_id": run_id,
        "fixture": fixture,
        "prediction_mode": "pre_match",
        "prediction_cutoff_datetime": datetime.now(timezone.utc).isoformat(),
        "feature_schema_version": "1.0",
        "features": [
            {
                "feature_name": "pdf_sources_count",
                "value": len([s for s in sources if s.get("source_type") == "official_pdf"]),
                "source_urls": [
                    s.get("source_url") for s in sources
                    if s.get("source_type") == "official_pdf"
                ],
                "aggregation_method": "count",
                "leakage_check_status": "pending"
            },
            {
                "feature_name": "total_records_extracted",
                "value": sum(s.get("records_extracted", 0) for s in sources),
                "source_urls": [s.get("source_url") for s in sources],
                "aggregation_method": "sum",
                "leakage_check_status": "pending"
            }
        ],
        "missing_data": [],
        "limitations": ["MVP feature vector only counts sources and extracted rows"]
    }

    out_dir = Path("data/feature_vectors")
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / f"{run_id}_feature_vectors.canonical.json"
    path.write_text(json.dumps(feature_vector, indent=2), encoding="utf-8")

    return str(path), feature_vector