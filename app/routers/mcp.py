from fastapi import APIRouter
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
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)