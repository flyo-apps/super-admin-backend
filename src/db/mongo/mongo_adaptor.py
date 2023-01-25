import os
import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db
from dotenv import load_dotenv

load_dotenv()
async def connect_to_mongo():
    # prod_db = "mongodb+srv://aashishgarg:" + urllib.parse.quote("Dataflyo1") + "@staging.uj997.mongodb.net/flyo?retryWrites=true&w=majority"
    prod_db = "mongodb+srv://" + os.environ.get("FLYODBUSER") + ":" + urllib.parse.quote(os.environ.get("FLYODBPASSWORD")) + "@" + os.environ.get("FLYODBURL") + "?retryWrites=true&w=majority"
    db.client = AsyncIOMotorClient(
        str(
            prod_db
        ),
        maxPoolSize=10,
        minPoolSize=10,
    )

async def close_mongo_connection():
    db.client.close()
