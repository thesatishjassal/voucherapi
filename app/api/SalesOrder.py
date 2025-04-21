from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection
from app.controllers.Salesorder import (
    create_salesorder,
    get_salesorder_by_id,
    get_all_salesorders,
    update_salesorder,
    delete_salesorder,
    create_salesorder_item,
    bulk_update_salesorder_items,
    get_items_by_salesorder_id,
)
from app.schema.SalesOrder import SalesOrder, SalesOrderCreate, SalesOrderUpdate
from app.schema.Salesoderitems import SalesorderItemCreate, SalesorderItemResponse
from app.models.salesoderitems import SalesorderItems

router = APIRouter(tags=["Sales Orders API"])

# --- Sales Order Endpoints ---

@router.post("/salesorder/", response_model=SalesOrder)
def create_salesorder_api(salesorder: SalesOrderCreate, db: Session = Depends(get_db_connection)) -> SalesOrder:
    return create_salesorder(db, salesorder)

@router.get("/salesorder/{salesorder_id}", response_model=SalesOrder)
def read_salesorder_api(salesorder_id: int, db: Session = Depends(get_db_connection)) -> SalesOrder:
    salesorder = get_salesorder_by_id(db, salesorder_id)
    if not salesorder:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return salesorder

@router.get("/salesorder/", response_model=List[SalesOrder])
def read_all_salesorders_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)) -> List[SalesOrder]:
    return get_all_salesorders(db, skip, limit)

@router.put("/salesorder/{salesorder_id}", response_model=SalesOrder)
def update_salesorder_api(salesorder_id: int, update_data: SalesOrderUpdate, db: Session = Depends(get_db_connection)) -> SalesOrder:
    updated_salesorder = update_salesorder(db, salesorder_id, update_data)
    if not updated_salesorder:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return updated_salesorder

@router.delete("/salesorder/{salesorder_id}")
def delete_salesorder_api(salesorder_id: int, db: Session = Depends(get_db_connection)) -> dict:
    success = delete_salesorder(db, salesorder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return {"message": "Sales order deleted successfully"}

# --- Sales Order Item Endpoints ---

@router.post("/salesorder/{salesorder_id}/items/", response_model=SalesorderItemResponse)
def create_salesorder_item_api(salesorder_id: int, item: SalesorderItemCreate, db: Session = Depends(get_db_connection)) -> SalesorderItemResponse:
    return create_salesorder_item(db, salesorder_id, item)

@router.put("/salesorder/{salesorder_id}/items/", response_model=List[SalesorderItemResponse])
def bulk_update_salesorder_items_api(salesorder_id: int, items: List[SalesorderItemCreate], db: Session = Depends(get_db_connection)) -> List[SalesorderItemResponse]:
    return bulk_update_salesorder_items(db, salesorder_id, items)

@router.get("/salesorder/{salesorder_id}/items/", response_model=List[SalesorderItemResponse])
def read_salesorder_items_api(salesorder_id: int, db: Session = Depends(get_db_connection)) -> List[SalesorderItemResponse]:
    return get_items_by_salesorder_id(db, salesorder_id)

@router.delete("/salesorder/{salesorder_id}/items/{item_id}")
def delete_salesorder_item_api(salesorder_id: int, item_id: int, db: Session = Depends(get_db_connection)) -> dict:
    try:
        with db.begin():
            item = db.query(SalesorderItems).filter(
                SalesorderItems.salesorder_id == salesorder_id,
                SalesorderItems.id == item_id
            ).first()
            if not item:
                raise HTTPException(status_code=404, detail="Sales order item not found")
            db.delete(item)

        db.commit()
        return {"message": "Sales order item deleted successfully"}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
