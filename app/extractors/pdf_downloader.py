from pathlib import Path
import hashlib
import httpx


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_pdf(url: str, run_id: str) -> dict:
    out_dir = Path("data/pdfs") / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1] or "report.pdf"
    if not filename.endswith(".pdf"):
        filename = f"{filename}.pdf"

    pdf_path = out_dir / filename

    response = httpx.get(url, timeout=60, follow_redirects=True)
    response.raise_for_status()

    pdf_path.write_bytes(response.content)

    return {
        "url": url,
        "pdf_path": str(pdf_path),
        "status": "downloaded",
        "sha256": sha256_file(pdf_path),
        "size_bytes": pdf_path.stat().st_size,
    }