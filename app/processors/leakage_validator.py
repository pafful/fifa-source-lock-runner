from pathlib import Path
import json


def run_leakage_check(run_id: str, fixture: str, sources: list):
    checks = []
    passed = True

    for source in sources:
        source_url = source.get("source_url", "")

        if "post-match" in source_url.lower() or "full-time" in source_url.lower():
            passed = False
            checks.append({
                "rule": "target_match_or_post_match_exclusion",
                "status": "fail",
                "source_url": source_url,
                "details": "Possible post-match or full-time source detected."
            })
        else:
            checks.append({
                "rule": "source_pre_match_safety",
                "status": "pass",
                "source_url": source_url,
                "details": "No obvious post-match leakage detected in MVP."
            })

    report = {
        "run_id": run_id,
        "fixture": fixture,
        "passed": passed,
        "checks": checks,
    }

    out_dir = Path("data/ledgers")
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / f"{run_id}_leakage_check_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return str(path), report