import requests
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


class CloudflareDNSRecord():

    def __init__(self, instance_logger=logger):
        self.logger = instance_logger

    def create_record(self, mail, zone, auth_key, dns, ip):
        self.logger.debug('create_record')
        url = f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records'
        headers = {
            'X-Auth-Email': mail,
            'X-Auth-Key': auth_key,
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'A',
            'name': dns,
            'content': ip,
            'ttl': 120,
            'priority': 10,
            'proxied': False
        }

        self.logger.info({'url': url})
        response = requests.post(
            url,
            json.dumps(data),
            headers=headers
        )
        self.logger.debug({'response': response.json()})

        return response.json()['success']

    def get_record_id(self, mail, zone, auth_key, dns):
        self.logger.debug('get_record_id')
        url = f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records'
        headers = {
            'X-Auth-Email': mail,
            'X-Auth-Key': auth_key,
            'Content-Type': 'application/json'
        }
        params = {
            'type': 'A',
            'name': '.'.join(filter(lambda x: x, dns.split('.'))),
            'page': 1,
            'per_page': 20,
            'order': 'type',
            'direction': 'desc',
            'match': 'all'
        }

        self.logger.info({'url': url})
        response = requests.get(
            url,
            headers=headers,
            params=params
        )
        self.logger.debug({'response': response.json()})

        return response.json()['result'][0]['id']

    def remove_record(self, mail, zone, auth_key, dns):
        self.logger.debug('remove_record')
        record = self.get_record_id(mail, zone, auth_key, dns)
        url = f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records/{record}'
        headers = {
            'X-Auth-Email': mail,
            'X-Auth-Key': auth_key,
            'Content-Type': 'application/json'
        }

        self.logger.info({'url': url})
        response = requests.delete(
            url,
            headers=headers
        )
        self.logger.debug({'response': response.json()})

        return response.json()['success']

