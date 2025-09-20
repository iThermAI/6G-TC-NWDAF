import os
import subprocess
import pingparsing
from logger.app_logger import AppLogger


class DelayHandler:

	def __init__(self):

		self.ping_parser = pingparsing.PingParsing()
		self.oai_ext_cn = os.environ.get("OAI_EXT_CN")

		self.delay_logger = AppLogger()
		self.delay_logger.create_log("delay_handler_error")

	def get_network_stats(self):

		network_map = {}
		containers_map = {
			"ue1": os.environ.get("UE1_CN"),
			"ue2": os.environ.get("UE2_CN"),
			"ue3": os.environ.get("UE3_CN")}
		
		for container_id, container_name in containers_map.items():
			ip_cmd = f"docker exec {container_name} hostname -I | tr ' ' '\n' | grep '^12\.' | head -n 1"
			run_result = subprocess.run(ip_cmd, capture_output=True, text=True, shell=True)

			if run_result.returncode == 1:
				self.delay_logger.submit_log(
					message=f"IP Retrieve Error - ({container_id}):\n\n{run_result.stderr}")

				network_map[container_id] = ""
				continue

			network_map[container_id] = run_result.stdout.strip()

		return network_map

	def get_e2e_delay(self):

		network_map = self.get_network_stats()

		e2e_delay = {}
		for container_id, container_ip in network_map.items():
			ping_cmd = f"docker exec {self.oai_ext_cn} ping -c 5 {container_ip}"
			run_result = subprocess.run(ping_cmd, capture_output=True, text=True, shell=True)

			if run_result.returncode == 1:
				self.delay_logger.submit_log(
					message=f"Ping Retrieve Error - ({container_id}):\n\n{run_result.stderr}")

				e2e_delay[container_id] = ""
				continue

			ping_result = self.ping_parser.parse(run_result.stdout)
			e2e_delay[container_id] = float(ping_result.rtt_avg)
		
		return e2e_delay
