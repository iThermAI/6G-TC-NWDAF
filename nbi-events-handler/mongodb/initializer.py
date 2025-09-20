import os
from mongodb.query_utils import QueryUtils
from mongodb.connection_utils import MongoConfig, MongoConnect


query_utils = QueryUtils()
mongo_connect = MongoConnect()

mongo_nwdaf_config = MongoConfig(
	user=os.environ.get("MONGO_NWDAF_USERNAME"),
	password=os.environ.get("MONGO_NWDAF_PASSWORD"),
	host=os.environ.get("MONGO_NWDAF_HOST"),
	port=os.environ.get("MONGO_NWDAF_PORT"),
	name=os.environ.get("MONGO_NWDAF_DB"),
	collection=os.environ.get("MONGO_NWDAF_COLLECTION"))

mongo_nwdaf_collection = mongo_connect.connect(
    mongo_config=mongo_nwdaf_config)
