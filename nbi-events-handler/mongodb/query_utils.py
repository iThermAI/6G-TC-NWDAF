from traceback import format_exc
from logger.app_logger import AppLogger
from pymongo.collection import Collection


class QueryUtils:

	"""
	A class containing a set of functionalities to 
	interact with Mongo database

	...

	Attributes:
		None
	"""

	def __init__(self):

		self.db_logger = AppLogger()
		self.db_logger.create_log("mongodb_query_error")

	def insert_data(self, collection: Collection, data: dict):

		try:
			collection.insert_one(document=data)
		except:
			self.db_logger.submit_log(
				message=f"Mongo Insert Failed:\n\n{format_exc()}")
