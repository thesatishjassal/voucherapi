from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database import get_db_connection
from app.models.inventory import InventoryLog, HoldItem, ActionType
from app.models.products import Products

router = APIRouter()

class InventoryAction(BaseModel):
    itemcode: str
    action_type: ActionType
    quantity: int
    hold_reason: str | None = None

@router.post("/inventory-action")
async def inventory_action(data: InventoryAction, db: AsyncSession = Depends(get_db_connection)):
    result = await db.execute(select(Products).where(Products.itemcode == data.itemcode))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.action_type == ActionType.RETURN:
        product.quantity += data.quantity

    elif data.action_type in [ActionType.BOOK, ActionType.HOLD]:
        if product.quantity < data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient quantity")
        product.quantity -= data.quantity

    # Always log
    log = InventoryLog(
        itemcode=data.itemcode,
        action_type=data.action_type,
        quantity=data.quantity,
    )
    db.add(log)

    # If hold, also save to hold table
    if data.action_type == ActionType.HOLD:
        hold = HoldItem(
            itemcode=data.itemcode,
            quantity=data.quantity,
            hold_reason=data.hold_reason or "Not specified"
        )
        db.add(hold)

    await db.commit()
    return {"status": "success", "message": f"{data.action_type.value} processed"}
