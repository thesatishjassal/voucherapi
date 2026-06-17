from sqlalchemy.orm import Session
from app.models.salesperson import SalesPerson


class SalesPersonController:

    @staticmethod
    def create(db: Session, payload):
        salesperson = SalesPerson(**payload.dict())

        db.add(salesperson)
        db.commit()
        db.refresh(salesperson)

        return salesperson

    @staticmethod
    def get_all(db: Session):
        return db.query(SalesPerson).all()

    @staticmethod
    def get_by_id(db: Session, salesperson_id: int):
        return (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

    @staticmethod
    def update(db: Session, salesperson_id: int, payload):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return None

        update_data = payload.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(salesperson, key, value)

        db.commit()
        db.refresh(salesperson)

        return salesperson

    @staticmethod
    def delete(db: Session, salesperson_id: int):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return False

        db.delete(salesperson)
        db.commit()

        return True