import os
import requests
from dotenv import load_dotenv

load_dotenv()

WC_URL = os.getenv("WC_URL")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")

def upload_products_to_woocommerce(products):
    for product in products:
        payload = {
            "name": product["itemname"],
            "type": "simple",
            "regular_price": str(product["price"]),
            "description": product["description"],
            "short_description": product["description"][:100],
            "sku": product["itemcode"],
            "categories": [{"name": product["category"]}, {"name": product["subcategory"]}],
            "images": [{"src": f"https://api.panvic.in{product['thumbnail']}"}],
            "attributes": [
                {"name": "Brand", "option": product["brand"]},
                {"name": "Color", "option": product["color"]},
                {"name": "Size", "option": product["size"]},
                {"name": "Model", "option": product["model"]}
            ]
        }

        res = requests.post(WC_URL, auth=(WC_KEY, WC_SECRET), json=payload)
        if res.status_code >= 400:
            return {"error": f"Error uploading product: {product['itemname']}", "details": res.text}

    return {"message": "All products uploaded successfully"}
