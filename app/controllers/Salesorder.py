from datetime import datetime
from sqlite3 import IntegrityError as SQLiteIntegrityError
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.products import Products
from app.models.salesoders import SalesOrder
from app.models.salesoderitems import SalesorderItems
from app.schema.SalesOrder import SalesOrderCreate, SalesOrder as SalesOrderSchema, SalesOrderUpdate
from app.schema.Salesoderitems import SalesorderItemCreate, SalesorderItemResponse


# --- Sales Order Item Functions ---

def create_salesorder_item(db: Session, salesorder_id: int, item: SalesorderItemCreate) -> SalesorderItemResponse:
    try:
        with db.begin():
            # Check if sales order exists
            db_salesorder = db.query(SalesOrder).filter(SalesOrder.salesorder_id == salesorder_id).first()
            if not db_salesorder:
                raise HTTPException(status_code=404, detail="Sales order not found")

            # # Product ID is required
            # if not item.product_id:
            #     raise HTTPException(status_code=400, detail="Product ID is required")

            # # Check if product exists
            # product = db.query(Products).filter(Products.itemcode == item.product_id).first()
            # if not product:
            #     raise HTTPException(status_code=404, detail=f"Product with itemcode '{item.product_id}' not found")

            # Exclude the Pydantic field salesorderitems_id before creating DB object
            item_data = item.dict(exclude={"salesorderitems_id"})
            db_item = SalesorderItems(salesorder_id=salesorder_id, **item_data)
            db.add(db_item)
            db.flush()
            db.refresh(db_item)

        # Construct response
        return SalesorderItemResponse(
            item_id=db_item.id,
            salesorderitems_id=db_item.id,
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
            unit=db_item.unit
        )

    except (IntegrityError, SQLiteIntegrityError) as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def bulk_update_salesorder_items(db: Session, salesorder_id: int, items: List[SalesorderItemCreate]) -> List[SalesorderItemResponse]:
    try:
        updated_items_list = []

        with db.begin():
            salesorder = db.query(SalesOrder).filter(SalesOrder.salesorder_id == salesorder_id).first()
            if not salesorder:
                raise HTTPException(status_code=404, detail="Sales order not found")

            existing_items = db.query(SalesorderItems).filter(SalesorderItems.salesorder_id == salesorder_id).all()
            existing_items_map = {item.product_id: item for item in existing_items}
            submitted_product_ids = set()

            for item_data in items:
                product_id = item_data.product_id
                submitted_product_ids.add(product_id)

                if not product_id:
                    raise HTTPException(status_code=400, detail="Product ID is required")

                product = db.query(Products).filter(Products.itemcode == product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with itemcode '{product_id}' not found")

                if product_id in existing_items_map:
                    existing_item = existing_items_map[product_id]
                    for key, value in item_data.dict().items():
                        setattr(existing_item, key, value)
                    db.add(existing_item)
                    updated_items_list.append(SalesorderItemResponse(
                        item_id=existing_item.id,
                        salesoderitems_id=existing_item.id,
                        product_id=existing_item.product_id,
                        customercode=existing_item.customercode,
                        customerdescription=existing_item.customerdescription,
                        image=existing_item.image,
                        itemcode=existing_item.itemcode,
                        brand=existing_item.brand,
                        mrp=existing_item.mrp,
                        price=existing_item.price,
                        quantity=existing_item.quantity,
                        discount=existing_item.discount,
                        item_name=existing_item.item_name,
                        unit=existing_item.unit
                    ))
                else:
                    new_item_data = item_data.dict(exclude={"salesoderitems_id"})
                    new_item = SalesorderItems(salesorder_id=salesorder_id, **new_item_data)
                    db.add(new_item)
                    db.flush()
                    updated_items_list.append(SalesorderItemResponse(
                        item_id=new_item.id,
                        salesoderitems_id=new_item.id,
                        product_id=new_item.product_id,
                        customercode=new_item.customercode,
                        customerdescription=new_item.customerdescription,
                        image=new_item.image,
                        itemcode=new_item.itemcode,
                        brand=new_item.brand,
                        mrp=new_item.mrp,
                        price=new_item.price,
                        quantity=new_item.quantity,
                        discount=new_item.discount,
                        item_name=new_item.item_name,
                        unit=new_item.unit
                    ))

            # Delete removed items
            for product_id, existing_item in existing_items_map.items():
                if product_id not in submitted_product_ids:
                    db.delete(existing_item)

        return updated_items_list

    except (IntegrityError, SQLiteIntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_items_by_salesorder_id(db: Session, salesorder_id: int) -> List[SalesorderItemResponse]:
    items = db.query(SalesorderItems).filter(SalesorderItems.salesorder_id == salesorder_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this sales order ID")

    return [
        SalesorderItemResponse(
            item_id=item.id,
            salesoderitems_id=item.id,
            product_id=item.product_id,
            customercode=item.customercode,
            customerdescription=item.customerdescription,
            image=item.image,
            itemcode=item.itemcode,
            brand=item.brand,
            mrp=item.mrp,
            price=item.price,
            quantity=item.quantity,
            discount=item.discount,
            item_name=item.item_name,
            unit=item.unit
        ) for item in items
    ]


# --- Sales Order CRUD Functions ---

def create_salesorder(db: Session, salesorder_data: SalesOrderCreate) -> SalesOrderSchema:
    try:
        # ✅ Include issue_slip_no automatically if not provided
        data = salesorder_data.dict()
        if not data.get("issue_slip_no"):
            # Example: Auto-generate Issue Slip like IS-2025-0001
            count = db.query(SalesOrder).count() + 1
            data["issue_slip_no"] = f"IS-{datetime.now().year}-{count:04d}"

        # ✅ Automatically set date to current datetime if not provided
        if not data.get("date"):
            data["date"] = datetime.now()

        new_salesorder = SalesOrder(**data)
        db.add(new_salesorder)
        db.commit()
        db.refresh(new_salesorder)
        return SalesOrderSchema.from_orm(new_salesorder)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_salesorder_by_id(db: Session, salesorder_id: int) -> SalesOrderSchema:
    salesorder = db.query(SalesOrder).filter(SalesOrder.salesorder_id == salesorder_id).first()
    if not salesorder:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return SalesOrderSchema.from_orm(salesorder)


def get_all_salesorders(db: Session, skip: int = 0, limit: int = 100) -> List[SalesOrderSchema]:
    salesorders = db.query(SalesOrder).offset(skip).limit(limit).all()
    return [SalesOrderSchema.from_orm(order) for order in salesorders]


def update_salesorder(db: Session, salesorder_id: int, update_data: SalesOrderUpdate) -> SalesOrderSchema:
    try:
        salesorder = db.query(SalesOrder).filter(SalesOrder.salesorder_id == salesorder_id).first()
        if not salesorder:
            raise HTTPException(status_code=404, detail="Sales order not found")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(salesorder, key, value)

        db.commit()
        db.refresh(salesorder)
        return SalesOrderSchema.from_orm(salesorder)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def delete_salesorder(db: Session, salesorder_id: int) -> bool:
    salesorder = db.query(SalesOrder).filter(SalesOrder.salesorder_id == salesorder_id).first()
    if salesorder:
        db.delete(salesorder)
        db.commit()
        return True
    return False