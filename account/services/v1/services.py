import motor.motor_asyncio
from fastapi import Depends
from passlib.context import CryptContext
from ...schemas.v1.schemas import UserCreate
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient as Client
from ...db.v1.db import collection


def get_user_service():
    return UserService()


class UserService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __int__(self, collection):
        self.collection = collection

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    async def get_user(self, username: str, password: str):
        user = await collection.find_one({'username': username})
        password = self.verify_password(password, user['password'])

        if not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password!')

        return user

    async def authenticate(self, username, password):
        user = await self.get_user(username, password)
        return user

    async def create_user(self, user: UserCreate):
        user = await collection.find_one({'username': user.username})
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Username Has Been Taken! Please Choose Another Username")

        hash_pwd = self.hash_password(user.password)

        new_user = {'username': user.username, 'email': user.email, 'password': hash_pwd}
        return await collection.insert_one(new_user)







