from logging import getLogger, StreamHandler, DEBUG
from requests import *
from .utils import *
from .components import *


formatter = JsonFormatter('{"timestamp": "%(asctime)-15s", "level": "%(levelname)s", "message": %(message)s}')
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Standup():

    def __init__(self, instance_logger=logger):
        self.logger = instance_logger

    def start_instance(self, project, zone, target):
        self.logger.debug('start_instance')
        self.logger.debug({'project': project, 'zone': zone, 'target': target})
        instance = GCPInstance()
        compute = instance.get_compute()
        instance.start(compute, project, zone, target)

    def get_instance_external_ip_address(self, project, zone, target):
        self.logger.debug('get_instance_external_ip_address')
        self.logger.debug({'project': project, 'zone': zone, 'target': target})
        instance = GCPInstance()
        compute = instance.get_compute()
        return instance.get_external_ip_address(compute, project, zone, target)

    def add_dns_record(self, mail, zone, auth_key, dns, ip):
        self.logger.debug('add_dns_record')
        self.logger.debug({'mail': mail, 'zone': zone, 'auth_key': anonymization(auth_key), 'dns': dns, 'ip': ip})
        dns_service = CloudflareDNSRecord()
        return dns_service.create_record(mail, zone, auth_key, dns, ip)

