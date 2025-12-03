from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_service import CSVService
from app.schemas.csv_schema import CSVResponse

router = APIRouter(prefix="/csv", tags=["CSV Reader"])

@router.post("/read", response_model=CSVResponse)
async def read_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    data = CSVService.read_csv(file)
    return CSVResponse(
        filename=file.filename,
        rows=len(data),
        data=data
    )
