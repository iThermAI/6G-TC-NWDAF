import requests
from fastapi import APIRouter
from traceback import format_exc
from logger.app_logger import AppLogger
from starlette.responses import Response
from network_utils.delay_handler import DelayHandler
from analytics_utils.analytics_handler import AnalyticsHandler
from resources_utils.resources_handler import ResourcesHandler
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST


router = APIRouter()
delay_handler = DelayHandler()
analytics_handler = AnalyticsHandler()
resources_handler = ResourcesHandler()

metrics_logger = AppLogger()
metrics_logger.create_log("metrics_handler_error")

num_ue_metric = Gauge('num_ue', 'Number of UEs in the network')
num_pdu_metric = Gauge('num_pdu', 'Number of PDU Sessions in the network')

gnb_cpu_metric = Gauge('gnb_cpu', 'CPU usages of gNB containers', ['name'])
gnb_ram_metric = Gauge('gnb_ram', 'Memory usages of gNB containers', ['name'])

ue_e2e_delay_metric = Gauge('ue_e2e_delay', 'End-to-End Delay of UE containers', ['name'])

def update_num_ue_metric():
	try:
		request_parameters = analytics_handler.get_num_ue_request()
		response = requests.get(
			url=analytics_handler.analytics_url,
			params=request_parameters,
			timeout=5)
		result = response.json()

		absolute_num = 0
		if 'nwPerfs' in result and isinstance(result['nwPerfs'], list):
			for perf in result['nwPerfs']:
				if perf.get("nwPerfType") == "NUM_OF_UE":
					absolute_num = perf.get("absoluteNum", 0)
					break

		num_ue_metric.set(absolute_num)

	except:
		metrics_logger.submit_log(message=f"Num UE Update Failed:\n\n{format_exc()}")

def update_num_pdu_metric():
	try:
		request_parameters = analytics_handler.get_num_pdu_request()
		response = requests.get(
			url=analytics_handler.analytics_url,
			params=request_parameters,
			timeout=5)
		result = response.json()

		absolute_num = 0
		if 'nwPerfs' in result and isinstance(result['nwPerfs'], list):
			for perf in result['nwPerfs']:
				if perf.get("nwPerfType") == "SESS_SUCC_RATIO":
					absolute_num = perf.get("absoluteNum", 0)
					break

		num_pdu_metric.set(absolute_num)

	except:
		metrics_logger.submit_log(message=f"Num PDU Update Failed:\n\n{format_exc()}")

def update_resources_metric():

	resources_usages = resources_handler.get_resources_usages()
	for resource_name, resource_detail in resources_usages.items():
		gnb_cpu_metric.labels(name=resource_name).set(resource_detail["cpu"])
		gnb_ram_metric.labels(name=resource_name).set(resource_detail["ram"])

def update_e2e_delay_metric():

	e2e_delay = delay_handler.get_e2e_delay()
	for network_name, network_detail in e2e_delay.items():
		ue_e2e_delay_metric.labels(name=network_name).set(network_detail)

def collect_metrics():
	update_num_ue_metric()
	update_num_pdu_metric()
	update_resources_metric()
	update_e2e_delay_metric()

@router.get("/metrics")
async def metrics():
	collect_metrics()
	return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
