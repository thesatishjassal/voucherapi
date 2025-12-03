from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_service import CSVService
from app.schema.csv_schema import CSVResponse

csv_controller = APIRouter(prefix="/csv", tags=["CSV Reader"])

# ------- READ CSV FROM UPLOADED FILE -------
@csv_controller.post("/read", response_model=CSVResponse)
async def read_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    data = await CSVService.read_uploaded_csv(file)

    return CSVResponse(
        filename=file.filename,
        rows=len(data),
        data=data
    )

# ------- READ CSV FROM DATA FOLDER -------
@csv_controller.get("/read-file/{filename}", response_model=CSVResponse)
async def read_csv_from_folder(filename: str):

    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        data = await CSVService.read_csv_from_disk(filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return CSVResponse(
        filename=filename,
        rows=len(data),
        data=data
    )
