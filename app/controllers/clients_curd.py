from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.clients import Clients
from app.schema.clients_schema import ClientCreate, ClientUpdate
from database import get_db_connection as db

def create_client(client_data: ClientCreate, db: Session):
    client = Clients(BuisnessName=client_data.BuisnessName, GST_Number= client_data.GST_Number, Address= client_data.Address, Pincode=client_data.Pincode, City=client_data.City, State=client_data.State, Client_Name=client_data.Client_Name, Client_Phone=client_data.Client_Phone, Client_Email=client_data.Client_Email, Client_Type=client_data.Client_Type)
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
        if client_data.BuisnessName:
            client.BuisnessName = client_data.BuisnessName
        if client_data.GST_Number:
            client.GST_Number = client_data.GST_Number
        if client_data.Address:
            client.Address = client_data.Address
        if client_data.Pincode:
            client.Pincode = client_data.Pincode
        if client_data.City:
            client.City = client_data.City
        if client_data.State:
            client.State = client_data.State
        if client_data.Client_Name:
            client.Client_Name = client_data.Client_Name
        if client_data.Client_Phone:
            client.Client_Phone = client_data.Client_Phone
        if client_data.Client_Email:
            client.Client_Email = client_data.Client_Email
        if client_data.Client_Type:
            client.Client_Type = client_data.Client_Type
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
    return db.query(Clients).filter(Clients.Client_Phone == phone).first()