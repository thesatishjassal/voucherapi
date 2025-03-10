from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.clients_curd import update_client, delete_client, create_client, get_clients,get_client_by_phone
from app.schema.clients_schema import ClientCreate, ClientUpdate, ClientResponse
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException
import secrets

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/clients/", response_model=ClientResponse)
async def create_new_client(client: ClientCreate, db:Session = Depends(get_db_connection)):
    db_user = get_client_by_phone(client.client_phone, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone Number alredy exist!")
    else:
        result = create_client(client,db)
        session_id = secrets.token_hex(16)
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User added successfully",
            "user": {
                "id": result.id,
                "businessname": result.businessname,
                "GST Number": result.gst_number,
                "address": result.address,
                "address": result.address,
                "city": result.city,
                "state": result.state,
                "Picode": result.pincode,
                "Client Name": result.client_name,
                "Client Phone": result.client_phone,
                "Client Email": result.client_email,
                "Client Type": result.client_type
            },
            "session_id": session_id
        }
    )

@router.get("/clients/", response_model=list[ClientResponse])
async def get_all_clients(db:Session = Depends(get_db_connection)):
    return get_clients(db=db)

@router.put("/client/{client_id}")
def update_client_api(client_id: int, client_data: ClientUpdate, db: Session= Depends(get_db_connection)):
    print(client_id)
    try:
        updated_client= update_client(client_data, client_id, db)
        return {"message": "Client updated successfully", "client": updated_client}
    except HTTPException as e:
        raise e
    
@router.delete("/client/{client_id}")
def delete_client_api(client_id: int, db: Session = Depends(get_db_connection)):
    try:
        result = delete_client(client_id, db)
        return result
    except HTTPException as e:
        raise e

# Include the router in the main app
app.include_router(router)
