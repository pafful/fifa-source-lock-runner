# Contributing

## Getting Started

1. Fork the repository.
2. Create a branch for your change.
3. Create a virtual environment and install dependencies.
4. Make your change and add or update tests where relevant.
5. Run the relevant verification steps.
6. Submit a pull request with a clear summary.

## Development Workflow

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Code Style

- Prefer small, focused modules.
- Keep pipeline steps explicit and observable.
- Preserve the existing evidence-first design.
- Avoid introducing silent failures in the extraction pipeline.

## Testing

The repository currently contains a minimal structure for tests. Add new tests for:

- request validation
- run manifest creation
- leakage check behavior
- feature vector generation

## Documentation

When you change behaviour, update the relevant docs under docs/ and the top-level README.

## Pull Request Checklist

- Documentation updated.
- Relevant tests added or updated.
- No secrets committed.
- Evidence artefacts remain reproducible.
