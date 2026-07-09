from pathlib import Path
import json
from playwright.sync_api import sync_playwright


def capture_page(url: str, out_dir: str):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    requests_log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0 Chrome/120 Safari/537.36",
            viewport={"width": 1366, "height": 900},
            locale="en-US",
        )

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()

        def on_response(response):
            try:
                req = response.request
                content_type = response.headers.get("content-type", "")

                body = None
                if "json" in content_type or "text" in content_type:
                    body = response.text()

                requests_log.append({
                    "url": response.url,
                    "method": req.method,
                    "status": response.status,
                    "content_type": content_type,
                    "post_data": req.post_data,
                    "response_body_preview": body[:5000] if body else None,
                })

            except Exception as e:
                requests_log.append({
                    "url": response.url,
                    "error": str(e),
                })

        page.on("response", on_response)

        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)

        (out / "dom_snapshot.html").write_text(page.content(), encoding="utf-8")
        (out / "page_text.txt").write_text(
            page.locator("body").inner_text(),
            encoding="utf-8",
        )
        (out / "network_request_inventory.json").write_text(
            json.dumps(requests_log, indent=2),
            encoding="utf-8",
        )

        context.tracing.stop(path=str(out / "trace.zip"))

        browser.close()

    return {
        "dom": str(out / "dom_snapshot.html"),
        "text": str(out / "page_text.txt"),
        "network": str(out / "network_request_inventory.json"),
        "trace": str(out / "trace.zip"),
    }