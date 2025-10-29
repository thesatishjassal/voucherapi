from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.clients import Client
from app.schema.clients_schema import ClientCreate, ClientUpdate
from database import get_db_connection as db

def create_client(client_data: ClientCreate, db: Session):
    client = Client(
        businessname=client_data.businessname,
        gst_number=client_data.gst_number,
        address=client_data.address,
        pincode=client_data.pincode,
        city=client_data.city,
        state=client_data.state,
        client_name=client_data.client_name,
        client_phone=client_data.client_phone,
        client_email=client_data.client_email,
        client_type=client_data.client_type,
        created_by=client_data.created_by,  # ✅ store logged-in user name
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_clients(db: Session):
    return db.query(Client).all()

def update_client(client_data: ClientUpdate, client_id: int, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        if client_data.businessname:
            client.businessname = client_data.businessname
        if client_data.gst_number:
            client.gst_number = client_data.gst_number
        if client_data.address:
            client.address = client_data.address
        if client_data.pincode:
            client.pincode = client_data.pincode
        if client_data.city:
            client.city = client_data.city
        if client_data.state:
            client.state = client_data.state
        if client_data.client_name:
            client.client_name = client_data.client_name
        if client_data.client_phone:
            client.client_phone = client_data.client_phone
        if client_data.client_email:
            client.client_email = client_data.client_email
        if client_data.client_type:
            client.client_type = client_data.client_type
        if client_data.created_by:
            client.created_by = client_data.created_by  # ✅ update creator if needed

        db.commit()
        db.refresh(client)
        return client
    else:
        raise HTTPException(status_code=404, detail="Client not found")

def delete_client(client_id: int, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
        return {"Message": "Client Deleted Successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

def get_client_by_phone(phone: str, db: Session):
    return db.query(Client).filter(Client.client_phone == phone).first()
