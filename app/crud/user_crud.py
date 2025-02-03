from app.schemas.user_schema import UserResponse
from database import get_db_connection
from app.models import user
from mysql.connector import Error

def create_users(user: user):
    connection = get_db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor()
    query = "INSERT INTO users(name, email) VALUES (%s, %s)"
    values  = (user.name, user.email)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return{"Message": "User Created SuccesFully!"}
    except Error as e:
        cursor.close()
        connection.close()
        return {"Error": f"Error: {e}"}
    
def get_users():
        connection = get_db_connection()
        if connection is None:
            return []
        
        cursor =  connection.cursor(dictionary = True)
        query = "SELECT * FROM users"

        try:
            cursor.execute(query)
            users = cursor.fetchall()
            user_responses = [
                UserResponse(id=user['id'], name=user['name'], email=user['email'])
                    for user in users
                ]
            cursor.close()
            connection.close()
            return user_responses
        except Error  as e:
            cursor.close()
            connection.close()
            return {"Error": f"Error:{e}"}
        