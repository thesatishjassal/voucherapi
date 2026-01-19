from sqlalchemy.orm import Session, joinedload
from app.models.SwitchQuotationWa import SwitchQuotation_Wa
from app.models.switchquotationitemswa import SwitchQuotationItem_Wa
from app.schema.switch_quotation_wa import SwitchQuotationCreate


# CREATE
def create_switch_quotation(db: Session, payload: SwitchQuotationCreate, created_by="System"):
    quotation = SwitchQuotation_Wa(
        quotation_no=payload.quotation_no,
        salesperson=payload.salesperson,
        subject=payload.subject,
        amount_including_gst=payload.amount_including_gst,
        without_gst=payload.without_gst,
        gst_amount=payload.gst_amount,
        amount_with_gst=payload.amount_with_gst,
        warranty_guarantee=payload.warranty_guarantee,
        remarks=payload.remarks,
        status=payload.status,
        date=payload.date,
        client_id=payload.client_id,
        created_by=created_by
    )

    db.add(quotation)
    db.flush()

    for idx, item in enumerate(payload.items, start=1):
        db.add(
            SwitchQuotationItem_Wa(
                quotation_id=quotation.quotation_id,
                sr_no=item.sr_no or idx,
                **item.dict(exclude={"sr_no"})
            )
        )

    db.commit()
    db.refresh(quotation)
    return quotation


# READ ALL
def get_all_switch_quotations(db: Session):
    return db.query(SwitchQuotation_Wa).options(
        joinedload(SwitchQuotation_Wa.items)
    ).order_by(
        SwitchQuotation_Wa.quotation_id.desc()
    ).all()


# READ ONE
def get_switch_quotation_by_id(db: Session, quotation_id: int):
    return db.query(SwitchQuotation_Wa).options(
        joinedload(SwitchQuotation_Wa.items)
    ).filter(
        SwitchQuotation_Wa.quotation_id == quotation_id
    ).first()


# UPDATE (replace items)
def update_switch_quotation(db: Session, quotation_id: int, payload: SwitchQuotationCreate):
    quotation = get_switch_quotation_by_id(db, quotation_id)
    if not quotation:
        return None

    for field, value in payload.dict(exclude={"items"}).items():
        setattr(quotation, field, value)

    # Delete old items
    db.query(SwitchQuotationItem_Wa).filter(
        SwitchQuotationItem_Wa.quotation_id == quotation_id
    ).delete()

    # Insert new items
    for idx, item in enumerate(payload.items, start=1):
        db.add(
            SwitchQuotationItem_Wa(
                quotation_id=quotation_id,
                sr_no=item.sr_no or idx,
                **item.dict(exclude={"sr_no"})
            )
        )

    db.commit()
    db.refresh(quotation)
    return quotation


# DELETE
def delete_switch_quotation(db: Session, quotation_id: int):
    quotation = get_switch_quotation_by_id(db, quotation_id)
    if not quotation:
        return False

    db.delete(quotation)
    db.commit()
    return True