from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_service import CSVService
from app.schema.csv_schema import CSVResponse

csv_controller = APIRouter(prefix="/csv", tags=["CSV Reader"])

@csv_controller.post("/read", response_model=CSVResponse)
async def read_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    data = await CSVService.read_csv(file)

    return CSVResponse(
        filename=file.filename,
        rows=len(data),
        data=data
    )
