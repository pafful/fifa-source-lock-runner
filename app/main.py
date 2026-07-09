from fastapi import FastAPI
from app.runner import run_fixture_pipeline
from app.schemas import FixtureRunRequest

app= FastAPI(title="FIFA Source-Lock Evidence Runner")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/runs/fifa/team-at-play")
def create_run(request: FixtureRunRequest):
    result = run_fixture_pipeline(request)
    return result

