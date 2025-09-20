from typing import Union
from pydantic import BaseModel
from pymongo import MongoClient
from traceback import format_exc
from logger.app_logger import AppLogger


class MongoConfig(BaseModel):
	
	user: Union[str, None] = None
	password: Union[str, None] = None
	host: str = "localhost"
	port: Union[str, int] = 27017
	name: Union[str, None] = None
	collection: Union[str, None] = None


class MongoConnect:

	"""
	Connect to Mongo database

	...

	Attributes:
		None
	"""

	def __init__(self):

		self.db_logger = AppLogger()
		self.db_logger.create_log("mongodb_connection_error")

	def connect(self, mongo_config: MongoConfig):
		"""
		Initiate a connection to Mongo database.

		Args:
			mongo_config: Object of Mongo configuration

		Returns:
			Connection to Mongo database (collection object)
		"""

		if mongo_config.user or mongo_config.password:
			mongo_url = (
				f"mongodb://{mongo_config.user}:{mongo_config.password}"
				f"@{mongo_config.host}:{mongo_config.port}/{mongo_config.name}")
		
		else:
			mongo_url = f"mongodb://{mongo_config.host}:{mongo_config.port}/{mongo_config.name}"
		
		connection = MongoClient(mongo_url)

		try:
			db = connection[mongo_config.name]
			collection = db[mongo_config.collection]

		except:
			self.db_logger.submit_log(
				message=f"Mongo Connection Failed:\n\n{format_exc()}")
			collection = None

		return collection
