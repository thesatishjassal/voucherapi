import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db_connection
from app.controllers.quotation import (
    create_quotation_revision,
    clone_quotation,
    get_all_quotation_item_histories,
    get_history_by_quotation_item_id,
    bulk_update_quotation_items,
    get_items_by_quotation_id,
    create_quotation_item,
    create_quotation,
    get_quotation_by_id,
    get_all_quotations,
    update_quotation,
    delete_quotation,
    delete_quotation_item,
    add_or_update_item_image,
    update_single_quotation_item,
)
from app.schema.quotation import Quotation, QuotationCreate
from app.schema.quotation_items import QuotationItemBase, QuotationItemCreate, QuotationItemResponse
from app.schema.QuotationItemHistory import QuotationItemHistoryResponse
from app.models.quotationitems import QuotationItem

# ------------------------------------------------------
# FastAPI App & Router
# ------------------------------------------------------
app = FastAPI(title="Quotation Management API")
router = APIRouter(tags=["Quotations API"])

# ------------------------------------------------------
# Upload Directory Setup
# ------------------------------------------------------
UPLOAD_DIR = "uploads/quotations"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------------------------------------
# Clone Quotation
# ------------------------------------------------------
@router.post("/quotation/{quotation_id}/clone", response_model=Quotation)
def clone_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    """
    Clone a quotation and all its items into a new quotation.
    New quotation_no will include timestamp (e.g., PLQOT-022-CLONE-20250918123456).
    """
    return clone_quotation(db, quotation_id)

# ------------------------------------------------------
# Create Revision
# ------------------------------------------------------
@router.post("/quotation/{quotation_id}/revise", response_model=Quotation)
def revise_quotation_api(
    quotation_id: int,
    update_data: Optional[dict] = None,
    db: Session = Depends(get_db_connection)
):
    """
    Create a new revision of an existing quotation (e.g. PLQOT-022 -> PLQOT-022-A).
    `update_data` may include remarks or status updates.
    """
    return create_quotation_revision(db, quotation_id, update_data)

# ------------------------------------------------------
# Update Single Item
# ------------------------------------------------------
@router.put("/quotation/{quotation_id}/items/{item_id}", response_model=QuotationItemResponse)
def update_item_api(
    quotation_id: int,
    item_id: int,
    item: QuotationItemCreate,
    db: Session = Depends(get_db_connection)
):
    return update_single_quotation_item(db, quotation_id, item_id, item)

# ------------------------------------------------------
# Upload Item Image
# ------------------------------------------------------
@router.put("/quotation/{quotation_id}/items/{quotation_item_id}/image", response_model=QuotationItemResponse)
def upload_item_image_api(
    quotation_id: int,
    quotation_item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_connection),
):
    """
    Upload or update an image for a specific quotation item.
    Saves file in `uploads/quotations` folder.
    """
    item = db.query(QuotationItem).filter(
        QuotationItem.id == quotation_item_id,
        QuotationItem.quotation_id == quotation_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Quotation item not found for given quotation")

    file_location = os.path.join(UPLOAD_DIR, f"{quotation_item_id}_{file.filename}")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_path = f"/{file_location}"  # relative path for serving
    updated_item = add_or_update_item_image(db, quotation_item_id, image_path)
    return QuotationItemResponse.from_orm(updated_item)

# ------------------------------------------------------
# Create New Quotation
# ------------------------------------------------------
@router.post("/quotation/", response_model=Quotation)
def create_quotation_api(quotation: QuotationCreate, db: Session = Depends(get_db_connection)):
    return create_quotation(db, quotation)

# ------------------------------------------------------
# Add Item to Quotation
# ------------------------------------------------------
@router.post("/quotation/{quotation_id}/items/", response_model=QuotationItemResponse)
def create_quotation_item_api(quotation_id: int, item: QuotationItemCreate, db: Session = Depends(get_db_connection)):
    return create_quotation_item(db, quotation_id, item)

# ------------------------------------------------------
# Bulk Update Quotation Items
# ------------------------------------------------------
@router.put("/quotation/{quotation_id}/items/", response_model=List[QuotationItemResponse])
def bulk_update_quotation_items_api(
    quotation_id: int,
    items: List[QuotationItemCreate],
    db: Session = Depends(get_db_connection)
):
    return bulk_update_quotation_items(db, quotation_id, items)

# ------------------------------------------------------
# Get All Items for Quotation
# ------------------------------------------------------
@router.get("/quotation/{quotation_id}/items/", response_model=List[QuotationItemResponse])
def read_quotation_items_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    items = get_items_by_quotation_id(db, quotation_id)
    return [QuotationItemResponse.from_orm(item) for item in items]

# ------------------------------------------------------
# Get Quotation by ID
# ------------------------------------------------------
@router.get("/quotation/{quotation_id}", response_model=Quotation)
def read_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

# ------------------------------------------------------
# Get All Quotations (Paginated)
# ------------------------------------------------------
@router.get("/quotation/", response_model=List[Quotation])
def read_all_quotations_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)):
    return get_all_quotations(db, skip, limit)

# ------------------------------------------------------
# Update Quotation
# ------------------------------------------------------
@router.put("/quotation/{quotation_id}", response_model=Quotation)
def update_quotation_api(quotation_id: int, update_data: dict, db: Session = Depends(get_db_connection)):
    updated_quotation = update_quotation(db, quotation_id, update_data)
    if not updated_quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return updated_quotation

# ------------------------------------------------------
# Delete Quotation
# ------------------------------------------------------
@router.delete("/quotation/{quotation_id}")
def delete_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    success = delete_quotation(db, quotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"message": "Quotation deleted successfully"}

# ------------------------------------------------------
# Get All Item Histories
# ------------------------------------------------------
@router.get("/quotation-history/", response_model=List[QuotationItemHistoryResponse])
def fetch_all_histories_api(db: Session = Depends(get_db_connection)):
    return get_all_quotation_item_histories(db)

# ------------------------------------------------------
# Get History by Quotation Item ID
# ------------------------------------------------------
@router.get("/quotation-history/{quotation_item_id}", response_model=List[QuotationItemHistoryResponse])
def fetch_history_by_item_id_api(quotation_item_id: int, db: Session = Depends(get_db_connection)):
    return get_history_by_quotation_item_id(db, quotation_item_id)

# ------------------------------------------------------
# Delete Specific Quotation Item
# ------------------------------------------------------
@router.delete("/quotation/{quotation_id}/items/{item_id}")
def delete_quotation_item_api(quotation_id: int, item_id: int, db: Session = Depends(get_db_connection)):
    try:
        with db.begin():
            item = db.query(QuotationItem).filter(
                QuotationItem.quotation_id == quotation_id,
                QuotationItem.id == item_id
            ).first()

            if not item:
                raise HTTPException(status_code=404, detail="Quotation item not found")

            delete_quotation_item(db, item)

        db.commit()
        return {"message": "Quotation item deleted successfully"}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ------------------------------------------------------
# Register Router
# ------------------------------------------------------
app.include_router(router)
