# Stdlib Imports
import os

# Third party Imports
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient


# Set up motor client and odmantic engine
client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
engine = AIOEngine(
    client=client, database="<project_db>"
)  # replace <project_db> with database name
