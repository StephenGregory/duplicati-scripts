import jsonpickle
import requests
import logging

logger = logging.getLogger()


class Exporter:
    def __init__(self):
        pass

    def export(self, operation):
        """

        :type operation: Operation
        """
        pass


class Webhook(Exporter):
    def __init__(self, endpoint):
        Exporter.__init__(self)
        self.endpoint = endpoint

    def export(self, operation):
        response = self.post_json(operation)

        if response.status_code != 200:
            raise RuntimeError('Could not post operation to web hook', response)

    def post_json(self, operation):
        headers = {'content-type': 'application/json'}
        json = jsonpickle.encode(operation, unpicklable=False)
        logger.debug(json)
        response = requests.post(self.endpoint, data=json, headers=headers)
        return response
