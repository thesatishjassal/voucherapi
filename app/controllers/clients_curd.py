from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.clients import Clients
from app.schema.clients_schema import ClientCreate, ClientUpdate
from database import get_db_connection as db

def create_client(client_data: ClientCreate, db: Session):
    client = Clients(buisnessname=client_data.buisnessname, gst_number= client_data.gst_number, Address= client_data.Address, pincode=client_data.pincode, City=client_data.City, State=client_data.State, Client_Name=client_data.Client_Name, client_phone=client_data.client_phone, client_email=client_data.client_email, client_type=client_data.client_type)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

# Verify the password
def get_clients(db: Session):
    return db.query(Clients).all()

def update_client(client_data: ClientUpdate, client_id: int, db: Session):
    print(client_data)
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client:
        # Update the client details with the new data
        if client_data.buisnessname:
            client.buisnessname = client_data.buisnessname
        if client_data.gst_number:
            client.gst_number = client_data.gst_number
        if client_data.Address:
            client.Address = client_data.Address
        if client_data.pincode:
            client.pincode = client_data.pincode
        if client_data.City:
            client.City = client_data.City
        if client_data.State:
            client.State= client_data.State
        if client_data.Client_Name:
            client.Client_Name = client_data.Client_Name
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
    client =  db.query(Clients).filter(client_id ==client_id).first()
    if client:
        db.delete(client)
        db.commit()
        return {"Message" : "Client Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

def get_client_by_phone(phone: str, db: Session):
    return db.query(Clients).filter(Clients.client_phone == phone).first()