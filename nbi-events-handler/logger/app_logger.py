import os
import logging
import datetime
from pathlib import Path


class AppLogger:

	"""
	A logging class to manage
	and write on the log files

	...

	Attributes:
		None
	"""

	def __init__(self):

		self.logger = None
		self.log_path = Path(__file__).resolve().parent.parent.joinpath("logs")

	def create_log(self, log_name: str):
		"""
		Create a log file with specified name (if not exist),
		and assign a logging module named FileHandler to it.

		Args:
			log_name: Name of the log file

		Returns:
			None
		"""

		file_name = f"{log_name}.log"

		if not os.path.exists(self.log_path):
			os.makedirs(self.log_path)

		file_path = os.path.join(self.log_path, file_name)

		logger = logging.getLogger(log_name)
		logger.setLevel(logging.DEBUG)

		file_handler = logging.FileHandler(file_path)
		file_handler.setLevel(logging.DEBUG)

		logger.addHandler(file_handler)

		self.logger = logger

	def submit_log(self, message: str):
		"""
		Writes a message to the log file using logging object 

		Args:
			message: Specified log message

		Returns:
			None
		"""

		log_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		log_context = "".join([log_time, "-" * 50, "\n", message])

		self.logger.info(log_context)
