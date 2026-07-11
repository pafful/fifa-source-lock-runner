# API Reference

## Base URL

By default, the service runs on:

- http://127.0.0.1:8000

## Endpoints

### GET /

Health check endpoint.

**Response**

```json
{"status": "ok"}
```

### POST /runs/fifa/team-at-play

Starts a fixture evidence run.

**Request body**

```json
{
  "fixture": "Argentina vs France",
  "prediction_mode": "pre_match",
  "cutoff_policy": "before_kickoff",
  "source_policy": "official_fifa_only",
  "pdf_url": "https://example.com/report.pdf"
}
```

**Fields**

- fixture: required string identifying the fixture.
- prediction_mode: optional string, defaults to pre_match.
- cutoff_policy: optional string, defaults to before_kickoff.
- source_policy: optional string, defaults to official_fifa_only.
- pdf_url: optional PDF URL to download and parse.

**Response**

```json
{
  "run_id": "fifa_1234abcd",
  "status": "completed",
  "fixture": "Argentina vs France",
  "fixture_level_verdict": "PASS_TEAM_AT_PLAY_OFFICIAL_RECONSTRUCTED",
  "feature_vector_hash": "sha256-hash",
  "artefacts": {
    "browser_capture": {...},
    "source_manifest": "data/manifests/....json",
    "pdf_download": {...},
    "parsed_pdf": {...},
    "feature_vectors": "data/feature_vectors/....json",
    "feature_vector_hash": "data/hashes/....txt",
    "leakage_report": "data/ledgers/....json",
    "fixture_level_verdict": "PASS_TEAM_AT_PLAY_OFFICIAL_RECONSTRUCTED"
  }
}
```

## Error Handling

The current API relies on FastAPI default validation and exception behavior. Invalid input bodies will return a 422 response.

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/runs/fifa/team-at-play \
  -H "Content-Type: application/json" \
  -d '{"fixture":"Argentina vs France","pdf_url":"https://example.com/report.pdf"}'
```
