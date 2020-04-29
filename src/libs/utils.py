import json
from logging import getLogger, StreamHandler, DEBUG, Formatter
import ulid

class JsonFormatter(Formatter):

    def _str2json(self, msg):
        if type(msg) is str or \
            type(msg) is dict or \
            type(msg) is list:
            return json.dumps(msg)
        return msg

    def format(self, record):
        record.msg = self._str2json(record.msg)
        return super().format(record)


def anonymization(x):
    data = str(x)
    if len(data) < 1:
        return data
    elif len(data) == 1:
        return '*'
    elif len(data) <= 4:
        return data[0] + '*'*(len(data)-1)
    else:
        return data[0] + data[1] + '*'*(len(data)-3) + data[-1]


def update_transaction_id(handler, transaction_id=ulid.new().str):
    formatter = JsonFormatter('{"timestamp": "%(asctime)-15s", "transaction-id": ' + f'"{ulid.new().str}"' + ', "level": "%(levelname)s", "message": %(message)s}')
    handler.setFormatter(formatter)

