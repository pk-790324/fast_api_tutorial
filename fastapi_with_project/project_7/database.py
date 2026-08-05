from pymongo import MongoClient
from config import MONGODB_URI

client=MongoClient(MONGODB_URI)

db=client["my_db"] # get the default database from the uri


# collections
contract_collection=db["contracts"]
analysis_collection=db["analysis"]


def init_db():
    # create indexes for the collections if they don't exists
    contract_collection.create_index("filename",unique=True)
    analysis_collection.create_index("analysis_id",unique=True)
    