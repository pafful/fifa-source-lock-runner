# from pathlib import Path
# import pdfplumber
# import pandas as pd
#
#
# def parse_pdf(pdf_path: str, out_dir: str):
#     pdf_path = Path(pdf_path)
#     out = Path(out_dir)
#     out.mkdir(parents=True, exist_ok=True)
#
#     text_pages = []
#     tables = []
#
#     with pdfplumber.open(pdf_path) as pdf:
#         for page_number, page in enumerate(pdf.pages, start=1):
#             text_pages.append({
#                 "page": page_number,
#                 "text": page.extract_text() or "",
#             })
#
#             extracted_tables = page.extract_tables()
#             for table in extracted_tables:
#                 for row in table:
#                     tables.append({
#                         "page": page_number,
#                         "row": row,
#                     })
#
#     text_file = out / f"{pdf_path.stem}_text.json"
#     table_file = out / f"{pdf_path.stem}_tables.csv"
#
#     pd.DataFrame(text_pages).to_json(text_file, orient="records", indent=2)
#     pd.DataFrame(tables).to_csv(table_file, index=False)
#
#     return {
#         "text_file": str(text_file),
#         "table_file": str(table_file),
#     }




from pathlib import Path
import json
import pandas as pd
import pdfplumber


def parse_pdf(pdf_path: str, run_id: str) -> dict:
    pdf_path = Path(pdf_path)

    out_dir = Path("data/parsed") / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    text_pages = []
    table_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text_pages.append({
                "pdf": pdf_path.name,
                "page": page_number,
                "text": page.extract_text() or "",
            })

            tables = page.extract_tables()
            for table_index, table in enumerate(tables, start=1):
                for row_index, row in enumerate(table, start=1):
                    table_rows.append({
                        "pdf": pdf_path.name,
                        "page": page_number,
                        "table_index": table_index,
                        "row_index": row_index,
                        "row": row,
                    })

    text_file = out_dir / f"{pdf_path.stem}_text_pages.json"
    table_file = out_dir / f"{pdf_path.stem}_tables_raw.csv"

    text_file.write_text(json.dumps(text_pages, indent=2), encoding="utf-8")
    pd.DataFrame(table_rows).to_csv(table_file, index=False)

    return {
        "pdf_path": str(pdf_path),
        "text_file": str(text_file),
        "table_file": str(table_file),
        "pages_parsed": len(text_pages),
        "table_rows_extracted": len(table_rows),
    }