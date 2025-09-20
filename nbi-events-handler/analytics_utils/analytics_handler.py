import os
import json
from pathlib import Path
from logger.app_logger import AppLogger
from datetime import datetime, timedelta


class AnalyticsHandler:

	def __init__(self):

		self.analytics_logger = AppLogger()
		self.analytics_logger.create_log("analytics_handler_error")

		self.analytics_url = os.environ.get("ANALYTICS_URL")
		self.num_ue_schema_path = (
			Path(__file__).resolve().parent.joinpath("num_ue_schema.json"))
		self.num_pdu_schema_path = (
			Path(__file__).resolve().parent.joinpath("num_pdu_schema.json"))
		
	def get_num_ue_request(self):

		try:
			with open(self.num_ue_schema_path) as schema_file:
				num_ue_data = json.load(schema_file)
		except:
			num_ue_data = {}

		if not num_ue_data:
			self.analytics_logger.submit_log(message="Empty Num UE Schema")
			return None

		end_time = datetime.now()
		start_time = end_time - timedelta(days=1)

		num_ue_data["ana-req"]["startTs"] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
		num_ue_data["ana-req"]["endTs"] = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

		request_parameters = {
			'event-id': num_ue_data['event-id'],
			'ana-req': json.dumps(num_ue_data['ana-req']),
			'event-filter': json.dumps(num_ue_data['event-filter']),
			'supported-features': json.dumps(num_ue_data['supported-features']),
			'tgt-ue': json.dumps(num_ue_data['tgt-ue'])}
		
		return request_parameters

	def get_num_pdu_request(self):

		try:
			with open(self.num_pdu_schema_path) as schema_file:
				num_pdu_data = json.load(schema_file)
		except:
			num_pdu_data = {}

		if not num_pdu_data:
			self.analytics_logger.submit_log(message="Empty Num PDU Schema")
			return None

		end_time = datetime.now()
		start_time = end_time - timedelta(days=1)

		num_pdu_data["ana-req"]["startTs"] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
		num_pdu_data["ana-req"]["endTs"] = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

		request_parameters = {
			'event-id': num_pdu_data['event-id'],
			'ana-req': json.dumps(num_pdu_data['ana-req']),
			'event-filter': json.dumps(num_pdu_data['event-filter']),
			'supported-features': json.dumps(num_pdu_data['supported-features']),
			'tgt-ue': json.dumps(num_pdu_data['tgt-ue'])}
		
		return request_parameters
