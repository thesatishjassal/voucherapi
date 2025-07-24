from datetime import datetime
from sqlite3 import IntegrityError
from typing import List
from sqlalchemy.orm import Session
from app.models.products import Products
from app.models.quotation import Quotation
from app.models.cus_quotationitems import CusQuotationItem
from app.models.QuotationItemHistory import QuotationItemHistory
from app.schema.cus_quotation_items import CusQuotationItemCreate, CusQuotationItemResponse
from fastapi import HTTPException

# Helper function to delete a quotation item and log it in history
def delete_quotation_item(db: Session, item: CusQuotationItem) -> None:
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
        price=item.netPrice,  # Changed to netPrice to match model
        quantity=item.quantity,
        discount=item.discount,
        item_name=item.item_name,
        unit=item.unit,
        amount_including_gst=item.amount_including_gst,
        without_gst=item.without_gst,
        gst_amount=item.gst_amount,
        amount_with_gst=item.amount_with_gst,
        remarks=item.remarks,
        edited_at=datetime.utcnow(),
        action="delete"
    )
    db.add(history)
    db.delete(item)

def bulk_update_quotation_items(db: Session, quotation_id: int, items: List[CusQuotationItemCreate]) -> List[CusQuotationItemResponse]:
    try:
        updated_items_list = []

        with db.begin():  # Transaction start
            # Check if the quotation exists
            quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
            if not quotation:
                raise HTTPException(status_code=404, detail="Quotation not found")

            # Fetch existing items mapped by product_id
            existing_items = db.query(CusQuotationItem).filter(CusQuotationItem.quotation_id == quotation_id).all()
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
                        price=existing_item.netPrice,  # Changed to netPrice
                        quantity=existing_item.quantity,
                        discount=existing_item.discount,
                        item_name=existing_item.item_name,
                        unit=existing_item.unit,
                        amount_including_gst=existing_item.amount_including_gst,
                        without_gst=existing_item.without_gst,
                        gst_amount=existing_item.gst_amount,
                        amount_with_gst=existing_item.amount_with_gst,
                        remarks=existing_item.remarks,
                        edited_at=datetime.utcnow(),
                        action="update"
                    )
                    db.add(history)

                    # Update existing item
                    for key, value in item_data.dict().items():
                        setattr(existing_item, key, value)
                    db.add(existing_item)

                    # Append updated item to response list
                    updated_items_list.append(
                        CusQuotationItemResponse(
                            id=existing_item.id,
                            quotation_id=existing_item.quotation_id,
                            product_id=existing_item.product_id,
                            customercode=existing_item.customercode,
                            customerdescription=existing_item.customerdescription,
                            image=existing_item.image,
                            itemcode=existing_item.itemcode,
                            brand=existing_item.brand,
                            mrp=existing_item.mrp,
                            netPrice=existing_item.netPrice,  # Changed to netPrice
                            quantity=existing_item.quantity,
                            discount=existing_item.discount,
                            item_name=existing_item.item_name,
                            unit=existing_item.unit,
                            amount_including_gst=existing_item.amount_including_gst,
                            without_gst=existing_item.without_gst,
                            gst_amount=existing_item.gst_amount,
                            amount_with_gst=existing_item.amount_with_gst,
                            remarks=existing_item.remarks
                        )
                    )

                else:
                    # Add new item
                    new_item_data = item_data.dict(exclude={"quotation_id"})  # Exclude unnecessary fields
                    new_item = CusQuotationItem(quotation_id=quotation_id, **new_item_data)
                    db.add(new_item)
                    db.flush()  # To generate ID immediately

                    # Append new item to response list
                    updated_items_list.append(
                        CusQuotationItemResponse(
                            id=new_item.id,
                            quotation_id=new_item.quotation_id,
                            product_id=new_item.product_id,
                            customercode=new_item.customercode,
                            customerdescription=new_item.customerdescription,
                            image=new_item.image,
                            itemcode=new_item.itemcode,
                            brand=new_item.brand,
                            mrp=new_item.mrp,
                            netPrice=new_item.netPrice,  # Changed to netPrice
                            quantity=new_item.quantity,
                            discount=new_item.discount,
                            item_name=new_item.item_name,
                            unit=new_item.unit,
                            amount_including_gst=new_item.amount_including_gst,
                            without_gst=new_item.without_gst,
                            gst_amount=new_item.gst_amount,
                            amount_with_gst=new_item.amount_with_gst,
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

def create_quotation_item(db: Session, quotation_id: int, item: CusQuotationItemCreate) -> CusQuotationItemResponse:
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
            product = db.query(Products).filter(Products.itemcode == product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with itemcode '{product_id}' not found"
                )

            # Prepare data and exclude 'quotation_id' (quotation_id will be added separately)
            item_data = item.model_dump(exclude={"quotation_id"})

            # Create and add the new CusQuotationItem
            db_item = CusQuotationItem(quotation_id=db_quotation.quotation_id, **item_data)
            db.add(db_item)
            db.flush()  # Get auto-generated ID
            db.refresh(db_item)  # Refresh to get the latest DB state

        # Return the response schema (automatically maps 'id' to 'item_id' in response)
        return CusQuotationItemResponse(
            id=db_item.id,
            quotation_id=db_item.quotation_id,
            product_id=db_item.product_id,
            customercode=db_item.customercode,
            customerdescription=db_item.customerdescription,
            image=db_item.image,
            itemcode=db_item.itemcode,
            brand=db_item.brand,
            mrp=db_item.mrp,
            netPrice=db_item.netPrice,  # Changed to netPrice
            quantity=db_item.quantity,
            discount=db_item.discount,
            item_name=db_item.item_name,
            unit=db_item.unit,
            amount_including_gst=db_item.amount_including_gst,
            without_gst=db_item.without_gst,
            gst_amount=db_item.gst_amount,
            amount_with_gst=db_item.amount_with_gst,
            remarks=db_item.remarks
        )

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")

    except HTTPException:
        raise  # Re-raise HTTPExceptions without modification

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_items_by_quotation_id(db: Session, quotation_id: str) -> List[CusQuotationItem]:
    items = db.query(CusQuotationItem).filter(CusQuotationItem.quotation_id == int(quotation_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this quotation id")
    return items