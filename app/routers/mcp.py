from fastapi import APIRouter
import csv

# Create router for MCP endpoints
router = APIRouter(
    prefix="/mcp",
    tags=["mcp books"],
    responses={404: {"description": "Not found"}}
)

@router.get("/books", operation_id="get_csv_data")
async def read_books():
    with open("books.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)