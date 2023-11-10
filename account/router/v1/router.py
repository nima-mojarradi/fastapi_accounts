import asyncio
import motor.motor_asyncio
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from ...config.settings import port, mongodb_uri
from ...schemas.v1.schemas import UserSignUp, UserLogin, UserResponse
from fastapi import status
from ...db.v1.db import collection
import httpx
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from ...utils.authentication import hash_password


router = APIRouter()


client = motor.motor_asyncio.AsyncIOMotorClient()

db = client['accountdb'] 
collection = db['account'] 

@router.post('/user/create', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSignUp):
    print("2"*100)
    check_user = await collection.find_one({'username': user.username})
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Username Has Been Taken! Please Choose Another Username")
    user.password1 = hash_password(user.password1)
    user.password2 = hash_password(user.password2)
    result = await collection.insert_one(user.dict())
    print(result)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User didn't create")
    return {"user_id": str(result.inserted_id), "username": user.username}


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin):
    user_info = await collection.find_one({"username": user.username})
    print(user_info)
    if user_info:
        if user_info['password'] == user.password:
            return "User Logged In Successfully..."
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect.")
    else:
        print('your account does not exist, please create an account first')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")






