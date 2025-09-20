import os
import docker
from traceback import format_exc
from logger.app_logger import AppLogger


class ResourcesHandler:

	def __init__(self):

		self.resources_logger = AppLogger()
		self.resources_logger.create_log("resources_handler_error")

		self.docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

		self.containers_map = {
			"gnb1": os.environ.get("GNB1_CN"),
			"gnb2": os.environ.get("GNB2_CN"),
			"gnb3": os.environ.get("GNB3_CN")}

	def get_resources_usages(self):

		resources_usages = {}
		for container_id, container_name in self.containers_map.items():
			try:
				container = self.docker_client.containers.get(container_name)
				stats = container.stats(stream=False)

				cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
				system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
				online_cpus = stats['cpu_stats'].get('online_cpus', 1)
				cpu_percentage = (cpu_delta / system_delta) * online_cpus * 100 if system_delta > 0 else 0

				memory_usage = stats['memory_stats']['usage'] / (1024 ** 3)

				resources_usages[container_id] = {
					"cpu": cpu_percentage,
					"ram": memory_usage}
			except:
				self.resources_logger.submit_log(
					message=f"Resources Update Failed - ({container_id}):\n\n{format_exc()}")
				
				resources_usages[container_id] = {
					"cpu": 0,
					"ram": 0}

		return resources_usages
