from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection
from app.controllers.purchaseorder import (
    create_purchaseorder,
    get_purchaseorder_by_id,
    get_all_purchaseorders,
    update_purchaseorder,
    delete_purchaseorder,
    create_purchaseorder_item,
    bulk_update_purchaseorder_items,
    get_items_by_purchaseorder_id,
)
from app.schema.PurchaseOrder import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
from app.schema.PurchaseOrderItem import PurchaseOrderItemCreate, PurchaseOrderItemResponse
from app.models.PurchaseOrderItem import PurchaseOrderItems


router = APIRouter(tags=["Purchase Orders API"])

# --- Purchase Order Endpoints ---

@router.post("/purchaseorder/", response_model=PurchaseOrder)
def create_purchaseorder_api(purchaseorder: PurchaseOrderCreate, db: Session = Depends(get_db_connection)) -> PurchaseOrder:
    return create_purchaseorder(db, purchaseorder)


@router.get("/purchaseorder/{purchaseorder_id}", response_model=PurchaseOrder)
def read_purchaseorder_api(purchaseorder_id: int, db: Session = Depends(get_db_connection)) -> PurchaseOrder:
    purchaseorder = get_purchaseorder_by_id(db, purchaseorder_id)
    if not purchaseorder:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return purchaseorder


@router.get("/purchaseorder/", response_model=List[PurchaseOrder])
def read_all_purchaseorders_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)) -> List[PurchaseOrder]:
    return get_all_purchaseorders(db, skip, limit)


@router.put("/purchaseorder/{purchaseorder_id}", response_model=PurchaseOrder)
def update_purchaseorder_api(purchaseorder_id: int, update_data: PurchaseOrderUpdate, db: Session = Depends(get_db_connection)) -> PurchaseOrder:
    updated_purchaseorder = update_purchaseorder(db, purchaseorder_id, update_data)
    if not updated_purchaseorder:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return updated_purchaseorder


@router.delete("/purchaseorder/{purchaseorder_id}")
def delete_purchaseorder_api(purchaseorder_id: int, db: Session = Depends(get_db_connection)) -> dict:
    success = delete_purchaseorder(db, purchaseorder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return {"message": "Purchase order deleted successfully"}


# --- Purchase Order Item Endpoints ---

@router.post("/purchaseorder/{purchaseorder_id}/items/", response_model=PurchaseOrderItemResponse)
def create_purchaseorder_item_api(purchaseorder_id: int, item: PurchaseOrderItemCreate, db: Session = Depends(get_db_connection)) -> PurchaseOrderItemResponse:
    return create_purchaseorder_item(db, purchaseorder_id, item)


@router.put("/purchaseorder/{purchaseorder_id}/items/", response_model=List[PurchaseOrderItemResponse])
def bulk_update_purchaseorder_items_api(purchaseorder_id: int, items: List[PurchaseOrderItemCreate], db: Session = Depends(get_db_connection)) -> List[PurchaseOrderItemResponse]:
    return bulk_update_purchaseorder_items(db, purchaseorder_id, items)


@router.get("/purchaseorder/{purchaseorder_id}/items/", response_model=List[PurchaseOrderItemResponse])
def read_purchaseorder_items_api(purchaseorder_id: int, db: Session = Depends(get_db_connection)) -> List[PurchaseOrderItemResponse]:
    return get_items_by_purchaseorder_id(db, purchaseorder_id)


@router.delete("/purchaseorder/{purchaseorder_id}/items/{item_id}")
def delete_purchaseorder_item_api(purchaseorder_id: int, item_id: int, db: Session = Depends(get_db_connection)) -> dict:
    try:
        with db.begin():
            item = db.query(PurchaseOrderItems).filter(
                PurchaseOrderItems.purchaseorder_id == purchaseorder_id,
                PurchaseOrderItems.id == item_id
            ).first()
            if not item:
                raise HTTPException(status_code=404, detail="Purchase order item not found")
            db.delete(item)

        db.commit()
        return {"message": "Purchase order item deleted successfully"}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
