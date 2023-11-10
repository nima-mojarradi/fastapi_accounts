import motor

mongo_url = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

db = client['accountdb']  

collection = db['account'] 
