from pymongo import MongoClient
from model import User, UserLogin, UserCreate
from passlib.context import CryptContext
import bcrypt
import pydantic
from bson import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.users_collection = self.db['users'] 
    
    def load_user(self):
        user_data = self.db['users'].find()
        user_list = []
        for item in user_data:
            item["_id"] = str(item["_id"])
            user_list.append(item)
        return user_list
    
    def load_user_id(self, user_id: str): 
        user_data = self.db['users'].find_one({'id': user_id}) 
        return user_data
    
    def load_user_userID(self, user_id: int):
        user_data = self.db['users'].find_one({'userId': user_id})
        return user_data
    
    def create_user(self, user_name: str, user_age: int, user_gender: str, user_email: str, user_id: str, hashed_password: str, user_size: object):
        userId = self.db['users'].estimated_document_count() + 1
        user_data = {
            "userId": userId,
            "userName": user_name, 
            "age": user_age, 
            "gender": user_gender, 
            "email": user_email, 
            "id": user_id, 
            "password": hashed_password, 
            "shoesSizes": user_size 
        }
        self.users_collection.insert_one(user_data)

    def load_username(self, username: str):
        user_data = self.db['users'].find_one({'userName': username})
        return user_data

    def hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode("utf-8")
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def check_user_cred(self, username: str, password: str) -> bool:
        return bool(self.db.users.find_one({'username': username, 'password': password}))

    def add_user(self, user: User) -> bool:
        try:
            self.db.users.insert_one(user.dict())
            return True
        except Exception:
            return False

    def update_size(self, id: int, brand: str, size: int):
        target_user = self.db['users'].find_one({'userId': id })
        size_obj = target_user['shoesSizes']
        size_obj[brand] = size
        print(target_user)
        print(size_obj)
        self.db['users'].update_one({'userId': id}, {"$set": {"shoesSizes": size_obj}})
        user_data = self.db['users'].find_one({"userId": id})
        print(user_data)
        
        return user_data