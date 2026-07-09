from pathlib import Path
import hashlib
import json


def canonical_hash(obj: dict) -> str:
    canonical = json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def write_hash(run_id: str, obj: dict):
    digest = canonical_hash(obj)

    out_dir = Path("data/hashes")
    out_dir.mkdir(parents=True, exist_ok=True)

    hash_path = out_dir / f"{run_id}_feature_vector_hash.txt"
    hash_path.write_text(digest, encoding="utf-8")

    return str(hash_path), digest