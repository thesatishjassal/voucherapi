from fastapi import APIRouter, UploadFile, File
from app.controllers.woocommerce import upload_products_to_woocommerce
from app.utils.excel_parser import parse_excel

router = APIRouter()

@router.post("/upload-products")
async def upload_products(file: UploadFile = File(...)):
    content = await file.read()
    products = parse_excel(content)
    response = upload_products_to_woocommerce(products)
    return response
