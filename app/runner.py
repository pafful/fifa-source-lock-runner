# from uuid import uuid4
#
# from app.extractors.fifa_browser import capture_page
# from app.processors.manifest_builder import build_source_manifest
# from app.processors.feature_vector_generator import generate_feature_vector
# from app.processors.hash_generator import write_hash
# from app.processors.leakage_validator import run_leakage_check
# from app.governance.verdict_engine import determine_verdict
# from app.extractors.pdf_parser import parse_pdf
#
#
# def run_fixture_pipeline(request):
#     run_id = f"fifa_{uuid4().hex[:8]}"
#
#     # MVP test URL. Later you replace this with the real FIFA fixture URL.
#     fifa_url = "https://www.fifa.com"
#
#     browser_output = capture_page(
#         url=fifa_url,
#         out_dir=f"data/raw/{run_id}",
#     )
#
#     source_manifest_path = build_source_manifest(
#         run_id=run_id,
#         fixture=request.fixture,
#         sources=[
#             {
#                 "source_name": "FIFA website",
#                 "source_type": "rendered_html_network_capture",
#                 "source_url": fifa_url,
#                 "extraction_method": "playwright_network_capture",
#                 "records_extracted": 1,
#                 "status": "captured",
#                 "artefacts": browser_output,
#             }
#         ],
#     )
#
#     leakage_report_path, leakage_report = run_leakage_check(run_id)
#
#     feature_vector_path, feature_vector = generate_feature_vector(
#         run_id=run_id,
#         fixture=request.fixture,
#     )
#
#     hash_path, feature_hash = write_hash(
#         run_id=run_id,
#         obj=feature_vector,
#     )
#
#     run_state = {
#         "target_match_identified": True,
#         "teams_identified": True,
#         "blocking_missing_data": False,
#         "leakage_passed": leakage_report["passed"],
#         "feature_vector_hash": feature_hash,
#     }
#
#     verdict = determine_verdict(run_state)
#
#     return {
#         "run_id": run_id,
#         "status": "completed",
#         "fixture": request.fixture,
#         "fixture_level_verdict": verdict,
#         "feature_vector_hash": feature_hash,
#         "artefacts": {
#             "source_manifest": source_manifest_path,
#             "feature_vectors": feature_vector_path,
#             "feature_vector_hash": hash_path,
#             "leakage_report": leakage_report_path,
#         },
#     }



from uuid import uuid4

from app.extractors.fifa_browser import capture_page
from app.extractors.pdf_downloader import download_pdf
from app.extractors.pdf_parser import parse_pdf
from app.processors.manifest_builder import build_source_manifest
from app.processors.feature_vector_generator import generate_feature_vector
from app.processors.hash_generator import write_hash
from app.processors.leakage_validator import run_leakage_check
from app.governance.verdict_engine import determine_verdict
from app.storage.feature_store import (
    init_db,
    save_run_manifest,
    save_sources,
    save_artefact,
)


def run_fixture_pipeline(request):
    run_id = f"fifa_{uuid4().hex[:8]}"
    init_db()

    # MVP 1: browser capture
    # Later, replace this with a real FIFA fixture/match-centre URL.
    fifa_url = "https://www.fifa.com"

    browser_output = capture_page(
        url=fifa_url,
        out_dir=f"data/raw/{run_id}",
    )

    # MVP 2: optional PDF download + parse
    pdf_result = None
    parsed_pdf_result = None

    if request.pdf_url:
        pdf_result = download_pdf(
            url=request.pdf_url,
            run_id=run_id,
        )

        parsed_pdf_result = parse_pdf(
            pdf_path=pdf_result["pdf_path"],
            run_id=run_id,
        )

    sources = [
        {
            "source_name": "FIFA website",
            "source_type": "rendered_html_network_capture",
            "source_url": fifa_url,
            "extraction_method": "playwright_network_capture",
            "records_extracted": 1,
            "status": "captured",
            "artefacts": browser_output,
        }
    ]

    save_sources(run_id, sources)

    leakage_report_path, leakage_report = run_leakage_check(
        run_id=run_id,
        fixture=request.fixture,
        sources=sources,
    )

    feature_vector_path, feature_vector = generate_feature_vector(
        run_id=run_id,
        fixture=request.fixture,
        sources=sources,
    )

    hash_path, feature_hash = write_hash(
        run_id=run_id,
        obj=feature_vector,
    )

    run_state = {
        "target_match_identified": True,
        "teams_identified": True,
        "blocking_missing_data": False,
        "reconciliation_passed": True,
        "leakage_passed": leakage_report["passed"],
        "feature_vector_hash": feature_hash,
    }

    verdict = determine_verdict(run_state)

    if pdf_result:
        sources.append(
            {
                "source_name": "PDF report",
                "source_type": "official_pdf",
                "source_url": pdf_result["url"],
                "extraction_method": "httpx_download_pdf_pdfplumber_parse",
                "records_extracted": parsed_pdf_result["table_rows_extracted"],
                "status": pdf_result["status"],
                "sha256": pdf_result["sha256"],
                "size_bytes": pdf_result["size_bytes"],
                "artefacts": {
                    "download": pdf_result,
                    "parsed": parsed_pdf_result,
                },
            }
        )

    source_manifest_path = build_source_manifest(
        run_id=run_id,
        fixture=request.fixture,
        sources=sources,
    )

    save_artefact(run_id, "source_manifest", source_manifest_path)

    leakage_report_path, leakage_report = run_leakage_check(
        run_id=run_id,
        fixture=request.fixture,
        sources=sources,
    )

    feature_vector_path, feature_vector = generate_feature_vector(
        run_id=run_id,
        fixture=request.fixture,
        sources=sources,
    )

    hash_path, feature_hash = write_hash(
        run_id=run_id,
        obj=feature_vector,
    )

    run_state = {
        "target_match_identified": True,
        "teams_identified": True,
        "blocking_missing_data": False,
        "leakage_passed": leakage_report["passed"],
        "feature_vector_hash": feature_hash,
    }

    verdict = determine_verdict(run_state)

    save_run_manifest(
        run_id=run_id,
        fixture=request.fixture,
        prediction_mode=request.prediction_mode,
        status="completed",
        verdict=verdict,
        feature_vector_hash=feature_hash,
    )

    return {
        "run_id": run_id,
        "status": "completed",
        "fixture": request.fixture,
        "fixture_level_verdict": verdict,
        "feature_vector_hash": feature_hash,
        "artefacts": {
            "browser_capture": browser_output,
            "source_manifest": source_manifest_path,
            "pdf_download": pdf_result,
            "parsed_pdf": parsed_pdf_result,
            "feature_vectors": feature_vector_path,
            "feature_vector_hash": hash_path,
            "leakage_report": leakage_report_path,
            "fixture_level_verdict": verdict,
        },
    }