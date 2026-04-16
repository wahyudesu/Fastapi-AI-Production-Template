from fastapi import APIRouter
import anyio
import csv
from pathlib import Path

router = APIRouter(
    prefix="/mcp",
    tags=["mcp books"],
    responses={404: {"description": "Not found"}}
)

@router.get("/books", operation_id="get_csv_data")
async def read_books():
    csv_path = Path(__file__).parent.parent.parent / "data" / "books.csv"

    def _read_csv():
        with open(csv_path, newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))

    return await anyio.to_thread.run_sync(_read_csv)