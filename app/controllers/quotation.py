from datetime import datetime
from sqlite3 import IntegrityError
from typing import List
from sqlalchemy.orm import Session
from app.models.products import Products
from app.models.quotation import Quotation
from app.models.quotationitems import QuotationItem
from app.models.QuotationItemHistory import QuotationItemHistory
from app.schema.quotation import QuotationCreate
from app.schema.quotation_items import QuotationItemCreate, QuotationItemResponse, QuotationItemBase
from fastapi import HTTPException
from app.schema.QuotationItemHistory import QuotationItemHistoryResponse

def add_or_update_item_image(db: Session, quotation_item_id: int, image_url: str) -> QuotationItem:
    """
    Add or update an image for a QuotationItem by its ID,
    and log the change in QuotationItemHistory.
    """

    # Fetch the item
    item = db.query(QuotationItem).filter(QuotationItem.id == quotation_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Quotation item with ID {quotation_item_id} not found")

    try:
        # Save history before updating
        history = QuotationItemHistory(
            quotation_item_id=item.id,
            quotation_id=item.quotation_id,
            product_id=item.product_id,
            customercode=item.customercode,
            customerdescription=item.customerdescription,
            image=item.image,  # old image before update
            itemcode=item.itemcode,
            brand=item.brand,
            mrp=item.mrp,
            price=item.price,
            quantity=item.quantity,
            discount=item.discount,
            item_name=item.item_name,
            unit=item.unit,
            amount=item.amount,
            amount_including_gst=item.amount_including_gst,
            without_gst=item.without_gst,
            gst_amount=item.gst_amount,
            amount_with_gst=item.amount_with_gst,
            remarks=item.remarks,
            edited_at=datetime.utcnow(),
            action="update_image"
        )
        db.add(history)

        # Update the image
        item.image = image_url
        if hasattr(item, "updated_at"):  
            item.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating image: {str(e)}")
        
# Helper function to delete a quotation item and log it in history
def delete_quotation_item(db: Session, item: QuotationItem) -> None:
    """
    Deletes a quotation item and logs the deletion in the QuotationItemHistory table.
    """
    # Save history before deletion
    history = QuotationItemHistory(
        quotation_item_id=item.id,
        quotation_id=item.quotation_id,
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
        unit=item.unit,
        # amount=item.amount,  # Added amount
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
        edited_at=datetime.utcnow(),
        action="delete"
    )
    db.add(history)
    db.delete(item)

def update_single_quotation_item(
    db: Session, quotation_id: int, item_id: int, item_data: QuotationItemCreate
) -> QuotationItemResponse:
    """
    Update a single quotation item by quotation_id and item_id,
    and log the previous state into QuotationItemHistory.
    """

    try:
        # Check if quotation exists
        quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
        if not quotation:
            raise HTTPException(status_code=404, detail=f"Quotation {quotation_id} not found")

        # Fetch the item
        db_item = (
            db.query(QuotationItem)
            .filter(QuotationItem.id == item_id, QuotationItem.quotation_id == quotation_id)
            .first()
        )
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f"Quotation item {item_id} not found for quotation {quotation_id}"
            )

        # Save history before update
        history = QuotationItemHistory(
            quotation_item_id=db_item.id,
            quotation_id=db_item.quotation_id,
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
            amount=db_item.amount,
            amount_including_gst=db_item.amount_including_gst,
            without_gst=db_item.without_gst,
            gst_amount=db_item.gst_amount,
            amount_with_gst=db_item.amount_with_gst,
            remarks=db_item.remarks,
            cct=db_item.cct,
            beamangle=db_item.beamangle,
            cri=db_item.cri,
            cutoutdia=db_item.cutoutdia,
            lumens=db_item.lumens,
            edited_at=datetime.utcnow(),
            action="update_single"
        )
        db.add(history)

        # Update fields
        for key, value in item_data.dict(exclude_unset=True).items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)

        return QuotationItemResponse(
            id=db_item.id,
            quotation_id=db_item.quotation_id,
            product_id=db_item.product_id,
            customercode=db_item.customercode,
            customerdescription=db_item.customerdescription,
            image=db_item.image,
            itemcode=db_item.itemcode,
            brand=db_item.brand,
            mrp=db_item.mrp,
            netPrice=db_item.netPrice,
            price=db_item.price,
            quantity=db_item.quantity,
            discount=db_item.discount,
            item_name=db_item.item_name,
            unit=db_item.unit,
            amount=db_item.amount,
            amount_including_gst=db_item.amount_including_gst,
            without_gst=db_item.without_gst,
            gst_amount=db_item.gst_amount,
            amount_with_gst=db_item.amount_with_gst,
            cct=db_item.cct,
            beamangle=db_item.beamangle,
            cri=db_item.cri,
            cutoutdia=db_item.cutoutdia,
            lumens=db_item.lumens,
            remarks=db_item.remarks,
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating item: {str(e)}")

def bulk_update_quotation_items(db: Session, quotation_id: int, items: List[QuotationItemCreate]) -> List[QuotationItemResponse]:
    try:
        updated_items_list = []

        with db.begin():  # Transaction start
            # Check if the quotation exists
            quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
            if not quotation:
                raise HTTPException(status_code=404, detail="Quotation not found")

            # Fetch existing items mapped by product_id
            existing_items = db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).all()
            existing_items_map = {item.product_id: item for item in existing_items}
            submitted_product_ids = set()

            # Process each item in the request
            for item_data in items:
                product_id = item_data.product_id
                submitted_product_ids.add(product_id)

                if product_id in existing_items_map:
                    existing_item = existing_items_map[product_id]

                    # Save history before update
                    history = QuotationItemHistory(
                        quotation_item_id=existing_item.id,
                        quotation_id=existing_item.quotation_id,
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
                        unit=existing_item.unit,
                        amount=existing_item.amount,  # Added amount
                        amount_including_gst=existing_item.amount_including_gst,
                        without_gst=existing_item.without_gst,
                        gst_amount=existing_item.gst_amount,
                        amount_with_gst=existing_item.amount_with_gst,
                        remarks=existing_item.remarks,
                        cct=existing_item.cct,
                        beamangle=existing_item.beamangle,
                        cri=existing_item.cri,
                        cutoutdia=existing_item.cutoutdia,
                        lumens=existing_item.lumens,
                        edited_at=datetime.utcnow(),
                        action="update"
                    )
                    db.add(history)

                    # Update existing item
                    for key, value in item_data.dict().items():  # Convert to dict before iterating
                        setattr(existing_item, key, value)
                    db.add(existing_item)

                    # Append updated item to response list
                    updated_items_list.append(
                        QuotationItemResponse(
                            id=existing_item.id,
                            quotation_id=existing_item.quotation_id,
                            product_id=existing_item.product_id,
                            customercode=existing_item.customercode,
                            customerdescription=existing_item.customerdescription,
                            image=existing_item.image,
                            itemcode=existing_item.itemcode,
                            brand=existing_item.brand,
                            mrp=existing_item.mrp,
                            netPrice=existing_item.netPrice,  # Fixed to use netPrice
                            price=existing_item.price,
                            quantity=existing_item.quantity,
                            discount=existing_item.discount,
                            item_name=existing_item.item_name,
                            unit=existing_item.unit,
                            amount=existing_item.amount,  # Added amount
                            amount_including_gst=existing_item.amount_including_gst,
                            without_gst=existing_item.without_gst,
                            gst_amount=existing_item.gst_amount,
                            amount_with_gst=existing_item.amount_with_gst,
                            cct=existing_item.cct,
                            beamangle=existing_item.beamangle,
                            cri=existing_item.cri,
                            cutoutdia=existing_item.cutoutdia,
                            lumens=existing_item.lumens,
                            remarks=existing_item.remarks
                        )
                    )

                else:
                    # Add new item
                    new_item_data = item_data.dict(exclude={"item_id", "quotation_id"})  # Exclude unnecessary fields
                    new_item = QuotationItem(quotation_id=quotation_id, **new_item_data)
                    db.add(new_item)
                    db.flush()  # To generate ID immediately

                    # Append new item to response list
                    updated_items_list.append(
                        QuotationItemResponse(
                            id=new_item.id,
                            quotation_id=new_item.quotation_id,
                            product_id=new_item.product_id,
                            customercode=new_item.customercode,
                            customerdescription=new_item.customerdescription,
                            image=new_item.image,
                            itemcode=new_item.itemcode,
                            brand=new_item.brand,
                            mrp=new_item.mrp,
                            netPrice=new_item.netPrice,  # Fixed to use netPrice
                            price=new_item.price,
                            quantity=new_item.quantity,
                            discount=new_item.discount,
                            item_name=new_item.item_name,
                            unit=new_item.unit,
                            amount=new_item.amount,  # Added amount
                            amount_including_gst=new_item.amount_including_gst,
                            without_gst=new_item.without_gst,
                            gst_amount=new_item.gst_amount,
                            amount_with_gst=new_item.amount_with_gst,
                            cct=new_item.cct,
                            beamangle=new_item.beamangle,
                            cri=new_item.cri,
                            cutoutdia=new_item.cutoutdia,
                            lumens=new_item.lumens,
                            remarks=new_item.remarks
                        )
                    )

            # Delete items that are in the database but not in the submitted list
            for product_id, existing_item in existing_items_map.items():
                if product_id not in submitted_product_ids:
                    delete_quotation_item(db, existing_item)

        db.commit()  # Commit transaction
        return updated_items_list  # Return updated/created items list

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def create_quotation_item(db: Session, quotation_id: int, item: QuotationItemCreate) -> QuotationItemResponse:
    try:
        with db.begin():  # Start transaction
            # Check if the quotation exists
            db_quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
            if not db_quotation:
                raise HTTPException(status_code=404, detail="Quotation not found")

            # Validate product_id
            product_id = item.product_id
            if not product_id:
                raise HTTPException(status_code=400, detail="Product ID is required")

            # Check if product exists
            # product = db.query(Products).filter(Products.itemcode == product_id).first()
            # if not product:
            #     raise HTTPException(
            #         status_code=404,
            #         detail=f"Product with itemcode '{product_id}' not found"
            #     )

            # Prepare data and exclude 'item_id', 'quotation_id' (quotation_id will be added separately)
            item_data = item.model_dump(exclude={"item_id", "quotation_id"})

            # Create and add the new QuotationItem
            db_item = QuotationItem(quotation_id=db_quotation.quotation_id, **item_data)
            db.add(db_item)
            db.flush()  # Get auto-generated ID
            db.refresh(db_item)  # Refresh to get the latest DB state

        # Return the response schema (automatically maps 'id' to 'item_id' in response)
        return QuotationItemResponse(
            item_id=db_item.id,
            quotation_id=db_item.quotation_id,
            product_id=db_item.product_id,
            customercode=db_item.customercode,
            customerdescription=db_item.customerdescription,
            image=db_item.image,
            itemcode=db_item.itemcode,
            brand=db_item.brand,
            mrp=db_item.mrp,
            netPrice=db_item.netPrice,  # Fixed to use netPrice
            price=db_item.price,
            quantity=db_item.quantity,
            discount=db_item.discount,
            item_name=db_item.item_name,
            unit=db_item.unit,
            amount=db_item.amount,  # Added amount
            amount_including_gst=db_item.amount_including_gst,
            without_gst=db_item.without_gst,
            gst_amount=db_item.gst_amount,
            amount_with_gst=db_item.amount_with_gst,
            remarks=db_item.remarks,
            cct=db_item.cct,
            beamangle=db_item.beamangle,
            cri=db_item.cri,
            cutoutdia=db_item.cutoutdia,
            lumens=db_item.lumens,
        )

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")

    except HTTPException:
        raise  # Re-raise HTTPExceptions without modification

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_all_quotation_item_histories(db: Session) -> List[QuotationItemHistoryResponse]:
    histories = db.query(QuotationItemHistory).all()
    if not histories:
        raise HTTPException(status_code=404, detail="No history records found")

    return [
        QuotationItemHistoryResponse(
            id=history.id,
            quotation_item_id=history.quotation_item_id,
            quotation_id=history.quotation_id,
            product_id=history.product_id,
            customercode=history.customercode,
            customerdescription=history.customerdescription,
            image=history.image,
            itemcode=history.itemcode,
            brand=history.brand,
            mrp=history.mrp,
            price=history.price,
            quantity=history.quantity,
            discount=history.discount,
            item_name=history.item_name,
            unit=history.unit,
            amount=history.amount,  # Added amount
            amount_including_gst=history.amount_including_gst,
            without_gst=history.without_gst,
            gst_amount=history.gst_amount,
            amount_with_gst=history.amount_with_gst,
            remarks=history.remarks,
            edited_at=history.edited_at,
            action=history.action,
            cct=history.cct,
            beamangle=history.beamangle,
            cri=history.cri,
            cutoutdia=history.cutoutdia,
            lumens=history.lumens,
        ) for history in histories
    ]

def get_history_by_quotation_item_id(db: Session, quotation_item_id: int) -> List[QuotationItemHistoryResponse]:
    histories = db.query(QuotationItemHistory).filter(QuotationItemHistory.quotation_item_id == quotation_item_id).all()
    if not histories:
        raise HTTPException(status_code=404, detail=f"No history found for quotation item ID {quotation_item_id}")

    return [
        QuotationItemHistoryResponse(
            id=history.id,
            quotation_item_id=history.quotation_item_id,
            quotation_id=history.quotation_id,
            product_id=history.product_id,
            customercode=history.customercode,
            customerdescription=history.customerdescription,
            image=history.image,
            itemcode=history.itemcode,
            brand=history.brand,
            mrp=history.mrp,
            price=history.price,
            quantity=history.quantity,
            discount=history.discount,
            item_name=history.item_name,
            unit=history.unit,
            amount=history.amount,  # Added amount
            amount_including_gst=history.amount_including_gst,
            without_gst=history.without_gst,
            gst_amount=history.gst_amount,
            amount_with_gst=history.amount_with_gst,
            remarks=history.remarks,
            edited_at=history.edited_at,
            cct=history.cct,
            beamangle=history.beamangle,
            cri=history.cri,
            cutoutdia=history.cutoutdia,
            lumens=history.lumens,
            action=history.action
        ) for history in histories
    ]

def get_items_by_quotation_id(db: Session, quotation_id: str) -> List[QuotationItem]:
    items = db.query(QuotationItem).filter(QuotationItem.quotation_id == int(quotation_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this quotation id")
    return items

def create_quotation(db: Session, quotation_data: QuotationCreate):
    new_quotation = Quotation(**quotation_data.dict())  # Use SQLAlchemy Model
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    return new_quotation

def get_quotation_by_id(db: Session, quotation_id: int):
    return db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()

def get_all_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quotation).offset(skip).limit(limit).all()  # Ensure Using Model

def update_quotation(db: Session, quotation_id: int, update_data: dict):
    quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
    if not quotation:
        return None
    for key, value in update_data.items():
        setattr(quotation, key, value)
    db.commit()
    db.refresh(quotation)
    return quotation

def delete_quotation(db: Session, quotation_id: int):
    quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
    if quotation:
        db.delete(quotation)
        db.commit()
        return True
    return False