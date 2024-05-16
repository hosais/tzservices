import pymongo
from pymongo import IndexModel, ASCENDING, DESCENDING

connnect_str = "mongodb+srv://tzmongo:pymonjoe1@tzcluster.fp5yu.mongodb.net/tzdb?retryWrites=true&w=majority"
conneect_str34 = "mongodb://tzmongo:pymonjoe1@tzcluster-shard-00-00.fp5yu.mongodb.net:27017,tzcluster-shard-00-01.fp5yu.mongodb.net:27017,tzcluster-shard-00-02.fp5yu.mongodb.net:27017/?ssl=true&replicaSet=atlas-ajnnj9-shard-0&authSource=admin&retryWrites=true&w=majority"

client = pymongo.MongoClient(conneect_str34)
db = client.test
