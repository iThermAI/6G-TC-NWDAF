import os
import json
import requests
from pathlib import Path
from traceback import format_exc
from logger.app_logger import AppLogger
from datetime import datetime, timedelta


class EventsHandler:

	def __init__(self):

		self.events_logger = AppLogger()
		self.events_logger.create_log("events_handler_error")

		self.notification_uri = os.environ.get("NOTIFICATION_URI")
		self.events_subscription_url = os.environ.get("SUBSCRIPTION_URL")
		self.events_schema_path = (
			Path(__file__).resolve().parent.joinpath("events_schema.json"))

	def get_events_request(self):

		try:
			with open(self.events_schema_path) as schema_file:
				events_request = json.load(schema_file)
		except:
			events_request = {}

		if events_request:
			events_request.update({"notificationURI": self.notification_uri})

			current_time = datetime.now()
			start_time = current_time - timedelta(weeks=48)
			end_time = current_time + timedelta(weeks=48)

			start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
			end_time_str =  end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

			for sub in events_request["eventSubscriptions"]:
				if "extraReportReq" in sub:
					sub["extraReportReq"]["startTs"] = start_time_str
					sub["extraReportReq"]["endTs"] = end_time_str
					if "anaMetaInd" in sub["extraReportReq"] and "dataWindow" in sub["extraReportReq"]["anaMetaInd"]:
						sub["extraReportReq"]["anaMetaInd"]["dataWindow"]["startTime"] = start_time_str
						sub["extraReportReq"]["anaMetaInd"]["dataWindow"]["stopTime"] = end_time_str
		else:
			self.events_logger.submit_log(message="Empty Events Schema")

		return events_request

	def send_events_subscription(self):

		events_request = self.get_events_request()

		try:
			response = requests.post(
				url=self.events_subscription_url,
				json=events_request,
				timeout=10)
			
			if response.status_code != 201:
				self.events_logger.submit_log(
					message=f"Events Subscription Error\n\n{response.content}")
		
		except:
			self.events_logger.submit_log(
				message=f"Sending Request Error\n\n{format_exc()}")
