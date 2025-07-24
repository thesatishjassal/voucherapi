from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.quotation import (
    bulk_update_quotation_items,
    get_items_by_quotation_id,
    create_quotation_item,
)
from app.schema.cus_quotation_items import CusQuotationItemCreate, CusQuotationItemResponse
from app.models.cus_quotationitems import CusQuotationItem  # Import the model for querying

app = FastAPI()
router = APIRouter(tags=["Quotations API"])  # Tag added for better Swagger UI grouping

# Add an item to a quotation
@router.post("/cus_quotation/{quotation_id}/items/", response_model=CusQuotationItemResponse)
def create_quotation_item_api(quotation_id: int, item: CusQuotationItemCreate, db: Session = Depends(get_db_connection)):
    return create_quotation_item(db, quotation_id, item)

# Bulk update quotation items
@router.put("/cus_quotation/{quotation_id}/items/", response_model=List[CusQuotationItemResponse])
def bulk_update_quotation_items_api(quotation_id: int, items: List[CusQuotationItemCreate], db: Session = Depends(get_db_connection)):
    return bulk_update_quotation_items(db, quotation_id, items)

# Get items by quotation ID
@router.get("/cus_quotation/{quotation_id}/items/", response_model=List[CusQuotationItemResponse])
def read_quotation_items_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    items = get_items_by_quotation_id(db, str(quotation_id))  # Convert to str to match controller signature
    return [
        CusQuotationItemResponse(
            id=item.id,  # Maps to item_id in response due to schema alias
            quotation_id=item.quotation_id,
            product_id=item.product_id,
            customercode=item.customercode,
            customerdescription=item.customerdescription,
            image=item.image,
            itemcode=item.itemcode,
            brand=item.brand,
            mrp=item.mrp,
            netPrice=item.netPrice,  # Fixed: Changed from item.price to item.netPrice
            quantity=item.quantity,
            discount=item.discount,
            item_name=item.item_name,
            unit=item.unit,
            amount_including_gst=item.amount_including_gst,
            without_gst=item.without_gst,
            gst_amount=item.gst_amount,
            amount_with_gst=item.amount_with_gst,
            remarks=item.remarks
        ) for item in items
    ]

# Include router in FastAPI app
app.include_router(router)