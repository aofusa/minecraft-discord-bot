import time
import googleapiclient
import googleapiclient.discovery
from logging import getLogger, StreamHandler, DEBUG
from ..utils import *


formatter = JsonFormatter('{"timestamp": "%(asctime)-15s", "level": "%(levelname)s", "message": %(message)s}')
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class GCPInstance():

    def __init__(self, instance_logger=logger):
        self.logger = instance_logger

    def get_compute(self):
        compute = googleapiclient.discovery.build('compute', 'v1')
        return compute

    def wait_for_operation(self, compute, project, zone, operation):
        self.logger.info('Waiting for operation to finish...')
        while True:
            result = compute.zoneOperations().get(
                project=project,
                zone=zone,
                operation=operation).execute()

            if result['status'] == 'DONE':
                self.logger.info('done.')
                if 'error' in result:
                    raise Exception(result['error'])
                return result

            time.sleep(1)

    def list_instances(self, compute, project, zone):
        self.logger.debug('list_instances')
        self.logger.debug({'project': project, 'zone': zone})
        result = compute.instances().list(project=project, zone=zone).execute()
        self.logger.debug({'instances': result})
        return result['items'] if 'items' in result else None

    def get_instance(self, compute, project, zone, instance_name):
        self.logger.debug('get_instance')
        self.logger.debug({'project': project, 'zone': zone, 'instance_name': instance_name})
        result = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
        self.logger.debug({'instances': result})
        return result

    def get_status(self, compute, project, zone, instance_name):
        self.logger.debug('get_status')
        self.logger.debug({'project': project, 'zone': zone, 'instance_name': instance_name})
        instance = self.get_instance(compute, project, zone, instance_name)
        self.logger.debug({'instance': instance})
        return instance['status']

    def get_external_ip_address(self, compute, project, zone, instance_name):
        self.logger.debug('get_external_ip_address')
        self.logger.debug({'project': project, 'zone': zone, 'instance_name': instance_name})
        instance = self.get_instance(compute, project, zone, instance_name)
        self.logger.debug({'instance': instance})
        if 'networkInterfaces' in instance and \
            len(instance['networkInterfaces']) > 0:
            networkInterface = instance['networkInterfaces'][0]
            if 'accessConfigs' in networkInterface and \
                len(networkInterface['accessConfigs']) > 0:
                return networkInterface['accessConfigs'][0]['natIP']
            else:
                return None
        else:
            return None

    def start(self, compute, project, zone, instance_name):
        self.logger.debug('start')
        self.logger.debug({'project': project, 'zone': zone, 'instance_name': instance_name})
        operation = compute.instances().start(project=project, zone=zone, instance=instance_name).execute()
        self.logger.info('start operation...')
        self.logger.debug({'operation': operation})
        self.wait_for_operation(compute, project, zone, operation['name'])
        self.logger.info('done operation.')

    def shutdown(self, compute, project, zone, instance_name):
        self.logger.debug('shutdown')
        self.logger.debug({'project': project, 'zone': zone, 'instance_name': instance_name})
        operation = compute.instances().stop(project=project, zone=zone, instance=instance_name).execute()
        self.logger.info('shutdown operation...')
        self.logger.debug({'operation': operation})
        self.wait_for_operation(compute, project, zone, operation['name'])
        self.logger.info('done operation.')

