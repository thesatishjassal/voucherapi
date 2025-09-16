import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection
from app.controllers.quotation import (
    create_quotation_revision,
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
)
from app.schema.quotation import Quotation, QuotationCreate
from app.schema.quotation_items import QuotationItemBase, QuotationItemCreate, QuotationItemResponse
from app.schema.QuotationItemHistory import QuotationItemHistoryResponse
from app.models.quotationitems import QuotationItem  # Import the model for querying
from app.controllers.quotation import add_or_update_item_image
from app.controllers.quotation import update_single_quotation_item

app = FastAPI()
router = APIRouter(tags=["Quotations API"])  # Tag added for better Swagger UI grouping

from fastapi import UploadFile, File

# ✅ Directory for uploads
UPLOAD_DIR = "uploads/quotations"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- New Revision Endpoint ----------
@router.post("/quotation/{quotation_id}/revise", response_model=Quotation)
def revise_quotation_api(
    quotation_id: int,
    update_data: Optional[dict] = None,
    db: Session = Depends(get_db_connection)
):
    """
    Duplicate a quotation and all its items into a new revision.
    Example: PLQOT-022 -> PLQOT-022-A -> PLQOT-022-B ...
    `update_data` can override fields like remarks or status.
    """
    return create_quotation_revision(db, quotation_id, update_data)

@router.put("/quotation/{quotation_id}/items/{item_id}", response_model=QuotationItemResponse)
def update_item(
    quotation_id: int,
    item_id: int,
    item: QuotationItemCreate,
    db: Session = Depends(get_db_connection)
):
    return update_single_quotation_item(db, quotation_id, item_id, item)

@router.put("/quotation/{quotation_id}/items/{quotation_item_id}/image", response_model=QuotationItemResponse)
def upload_item_image(
    quotation_id: int,
    quotation_item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_connection),
):
    # Ensure item belongs to the correct quotation
    item = db.query(QuotationItem).filter(
        QuotationItem.id == quotation_item_id,
        QuotationItem.quotation_id == quotation_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Quotation item not found for given quotation")

    # Save file to uploads/quotations/
    file_location = os.path.join(UPLOAD_DIR, f"{quotation_item_id}_{file.filename}")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store relative path for static serving
    image_path = f"/{file_location}"

    # Update DB
    updated_item = add_or_update_item_image(db, quotation_item_id, image_path)

    return QuotationItemResponse.from_orm(updated_item)


# Create a new quotation
@router.post("/quotation/", response_model=Quotation)
def create_quotation_api(quotation: QuotationCreate, db: Session = Depends(get_db_connection)):
    return create_quotation(db, quotation)

# Add an item to a quotation
@router.post("/quotation/{quotation_id}/items/", response_model=QuotationItemResponse)
def create_quotation_item_api(quotation_id: int, item: QuotationItemCreate, db: Session = Depends(get_db_connection)):
    return create_quotation_item(db, quotation_id, item)

# Bulk update quotation items
@router.put("/quotation/{quotation_id}/items/", response_model=List[QuotationItemResponse])
def bulk_update_quotation_items_api(quotation_id: int, items: List[QuotationItemCreate], db: Session = Depends(get_db_connection)):
    return bulk_update_quotation_items(db, quotation_id, items)

# Get items by quotation ID
@router.get("/quotation/{quotation_id}/items/", response_model=List[QuotationItemResponse])
def read_quotation_items_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    items = get_items_by_quotation_id(db, quotation_id)
    return [
        QuotationItemResponse(
            id=item.id,
            quotation_id=item.quotation_id,
            product_id=item.product_id,
            customercode=item.customercode,
            customerdescription=item.customerdescription,
            image=item.image,
            itemcode=item.itemcode,
            brand=item.brand,
            mrp=item.mrp,
            price=item.price,
            netPrice=item.netPrice,
            quantity=item.quantity,
            discount=item.discount,
            item_name=item.item_name,
            unit=item.unit,
            amount_including_gst=item.amount_including_gst,
            without_gst=item.without_gst,
            gst_amount=item.gst_amount,
            amount_with_gst=item.amount_with_gst,
            remarks=item.remarks,
            cct=item.cct,
            beamangle=item.beamangle,
            cri=item.cri,
            cutoutdia=item.cutoutdia,
            lumens=item.lumens,
            amount=item.amount,  # Ensure amount is included
        ) for item in items
    ]

# Get quotation by ID
@router.get("/quotation/{quotation_id}", response_model=Quotation)
def read_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

# Get all quotations with pagination
@router.get("/quotation/", response_model=List[Quotation])
def read_all_quotations_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)):
    return get_all_quotations(db, skip, limit)

# Update quotation by ID
@router.put("/quotation/{quotation_id}", response_model=Quotation)
def update_quotation_api(quotation_id: int, update_data: dict, db: Session = Depends(get_db_connection)):
    updated_quotation = update_quotation(db, quotation_id, update_data)
    if not updated_quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return updated_quotation

# Delete quotation by ID
@router.delete("/quotation/{quotation_id}")
def delete_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    success = delete_quotation(db, quotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"message": "Quotation deleted successfully"}

# Get all quotation item histories
@router.get("/quotation-history/", response_model=List[QuotationItemHistoryResponse])
def fetch_all_histories_api(db: Session = Depends(get_db_connection)):
    return get_all_quotation_item_histories(db)

# Get history by quotation item ID
@router.get("/quotation-history/{quotation_item_id}", response_model=List[QuotationItemHistoryResponse])
def fetch_history_by_item_id_api(quotation_item_id: int, db: Session = Depends(get_db_connection)):
    return get_history_by_quotation_item_id(db, quotation_item_id)

# Delete a specific quotation item by ID
@router.delete("/quotation/{quotation_id}/items/{item_id}")
def delete_quotation_item_api(quotation_id: int, item_id: int, db: Session = Depends(get_db_connection)):
    try:
        with db.begin():  # Start transaction
            # Fetch the item to delete
            item = db.query(QuotationItem).filter(
                QuotationItem.quotation_id == quotation_id,
                QuotationItem.id == item_id
            ).first()

            if not item:
                raise HTTPException(status_code=404, detail="Quotation item not found")

            # Delete the item and log it in history
            delete_quotation_item(db, item)

        db.commit()  # Commit transaction
        return {"message": "Quotation item deleted successfully"}

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Include router in FastAPI app
app.include_router(router)