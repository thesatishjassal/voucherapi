from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.clients import Client
from app.schema.clients_schema import ClientCreate, ClientUpdate
from database import get_db_connection as db

def create_client(client_data: ClientCreate, db: Session):
    client = Client(buisnessname=client_data.buisnessname, gst_number= client_data.gst_number, address= client_data.address, pincode=client_data.pincode, city=client_data.city, state=client_data.state, client_name=client_data.client_name, client_phone=client_data.client_phone, client_email=client_data.client_email, client_type=client_data.client_type)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

# Verify the password
def get_clients(db: Session):
    return db.query(Client).all()

def update_client(client_data: ClientUpdate, client_id: int, db: Session):
    print(client_data)
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        # Update the client details with the new data
        if client_data.buisnessname:
            client.buisnessname = client_data.buisnessname
        if client_data.gst_number:
            client.gst_number = client_data.gst_number
        if client_data.address:
            client.address = client_data.address
        if client_data.pincode:
            client.pincode = client_data.pincode
        if client_data.city:
            client.city = client_data.city
        if client_data.state:
            client.state= client_data.state
        if client_data.client_name:
            client.client_name = client_data.client_name
        if client_data.client_phone:
            client.client_phone = client_data.client_phone
        if client_data.client_email:
            client.client_email = client_data.client_email
        if client_data.client_type:
            client.client_type = client_data.client_type
        # Commit the transaction and refresh the client object to get the updated state
        db.commit()
        db.refresh(client)
        
        return client
    else:
        # If client is not found, raise an exception
        raise HTTPException(status_code=404, detail="Client not found")


def delete_client(client_id: int, db: Session):
    # Find the existing client by ID
    client =  db.query(Client).filter(client_id ==client_id).first()
    if client:
        db.delete(client)
        db.commit()
        return {"Message" : "Client Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

def get_client_by_phone(phone: str, db: Session):
    return db.query(Client).filter(Client.client_phone == phone).first()