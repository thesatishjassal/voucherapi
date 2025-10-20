from datetime import datetime
from sqlite3 import IntegrityError as SQLiteIntegrityError
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.products import Products
from app.models.PurcahseOrder import PurchaseOrder
from app.models.PurchaseOrderItem import PurchaseOrderItems
# from app.schema.PurchaseOrder import PurchaseOrderCreate, PurchaseOrder as PurchaseOrderSchema, PurchaseOrderUpdate
from app.schema.PurchaseOrderItem import PurchaseOrderItemCreate, PurchaseOrderItemResponse
from app.schema.PurchaseOrder import (
    PurchaseOrderCreate,
    PurchaseOrder as PurchaseOrderSchema,
    PurchaseOrderUpdate
)


# --- Purchase Order Item Functions ---

def create_purchaseorder_item(db: Session, purchaseorder_id: int, item: PurchaseOrderItemCreate) -> PurchaseOrderItemResponse:
    try:
        with db.begin():
            # Check if purchase order exists
            db_po = db.query(PurchaseOrder).filter(PurchaseOrder.purchaseorder_id == purchaseorder_id).first()
            if not db_po:
                raise HTTPException(status_code=404, detail="Purchase order not found")

            # Optional: Validate product
            if item.product_id:
                product = db.query(Products).filter(Products.itemcode == item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product '{item.product_id}' not found")

            # Exclude Pydantic field ID
            item_data = item.dict(exclude={"id"})
            db_item = PurchaseOrderItems(purchaseorder_id=purchaseorder_id, **item_data)
            db.add(db_item)
            db.flush()
            db.refresh(db_item)

        return PurchaseOrderItemResponse(
            id=db_item.id,
            product_id=db_item.product_id,
            customercode=db_item.customercode,
            customerdescription=db_item.customerdescription,
            image=db_item.image,
            itemcode=db_item.itemcode,
            brand=db_item.brand,
            mrp=db_item.mrp,
            price=db_item.price,
            quantity=db_item.quantity,
            discount=db_item.discount,
            item_name=db_item.item_name,
            unit=db_item.unit,
            color=db_item.color,
            remarks=db_item.remarks
        )

    except (IntegrityError, SQLiteIntegrityError) as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def bulk_update_purchaseorder_items(db: Session, purchaseorder_id: int, items: List[PurchaseOrderItemCreate]) -> List[PurchaseOrderItemResponse]:
    try:
        updated_items_list = []

        with db.begin():
            po = db.query(PurchaseOrder).filter(PurchaseOrder.purchaseorder_id == purchaseorder_id).first()
            if not po:
                raise HTTPException(status_code=404, detail="Purchase order not found")

            existing_items = db.query(PurchaseOrderItems).filter(PurchaseOrderItems.purchaseorder_id == purchaseorder_id).all()
            existing_items_map = {item.product_id: item for item in existing_items}
            submitted_product_ids = set()

            for item_data in items:
                product_id = item_data.product_id
                submitted_product_ids.add(product_id)

                # Optional validation
                if product_id:
                    product = db.query(Products).filter(Products.itemcode == product_id).first()
                    if not product:
                        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

                if product_id in existing_items_map:
                    existing_item = existing_items_map[product_id]
                    for key, value in item_data.dict().items():
                        setattr(existing_item, key, value)
                    db.add(existing_item)
                    updated_items_list.append(PurchaseOrderItemResponse.from_orm(existing_item))
                else:
                    new_item_data = item_data.dict(exclude={"id"})
                    new_item = PurchaseOrderItems(purchaseorder_id=purchaseorder_id, **new_item_data)
                    db.add(new_item)
                    db.flush()
                    updated_items_list.append(PurchaseOrderItemResponse.from_orm(new_item))

            # Delete removed items
            for product_id, existing_item in existing_items_map.items():
                if product_id not in submitted_product_ids:
                    db.delete(existing_item)

        return updated_items_list

    except (IntegrityError, SQLiteIntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_items_by_purchaseorder_id(db: Session, purchaseorder_id: int) -> List[PurchaseOrderItemResponse]:
    items = db.query(PurchaseOrderItems).filter(PurchaseOrderItems.purchaseorder_id == purchaseorder_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this purchase order ID")

    return [PurchaseOrderItemResponse.from_orm(item) for item in items]


# --- Purchase Order CRUD Functions ---

def create_purchaseorder(db: Session, po_data: PurchaseOrderCreate) -> PurchaseOrderSchema:
    try:
        data = po_data.dict()

        # Auto-generate Purchase Order No if not provided
        if not data.get("purchaseorder_no"):
            count = db.query(PurchaseOrder).count() + 1
            data["purchaseorder_no"] = f"PO-{datetime.now().year}-{count:04d}"

        # Set default date
        if not data.get("date"):
            data["date"] = datetime.now()

        new_po = PurchaseOrder(**data)
        db.add(new_po)
        db.commit()
        db.refresh(new_po)
        return PurchaseOrderSchema.from_orm(new_po)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_purchaseorder_by_id(db: Session, purchaseorder_id: int) -> PurchaseOrderSchema:
    po = db.query(PurchaseOrder).filter(PurchaseOrder.purchaseorder_id == purchaseorder_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return PurchaseOrderSchema.from_orm(po)


def get_all_purchaseorders(db: Session, skip: int = 0, limit: int = 100) -> List[PurchaseOrderSchema]:
    purchaseorders = db.query(PurchaseOrder).offset(skip).limit(limit).all()
    return [PurchaseOrderSchema.from_orm(po) for po in purchaseorders]


def update_purchaseorder(db: Session, purchaseorder_id: int, update_data: PurchaseOrderUpdate) -> PurchaseOrderSchema:
    try:
        po = db.query(PurchaseOrder).filter(PurchaseOrder.purchaseorder_id == purchaseorder_id).first()
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(po, key, value)

        db.commit()
        db.refresh(po)
        return PurchaseOrderSchema.from_orm(po)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def delete_purchaseorder(db: Session, purchaseorder_id: int) -> bool:
    po = db.query(PurchaseOrder).filter(PurchaseOrder.purchaseorder_id == purchaseorder_id).first()
    if po:
        db.delete(po)
        db.commit()
        return True
    return False
