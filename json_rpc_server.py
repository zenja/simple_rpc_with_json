import socket
import logging
import json
import threading


logging.basicConfig(level=logging.DEBUG)


class JsonRpcServer(object):
    HOST = '127.0.0.1'
    PORT = 50000
    BUFSIZE = 4096

    def __init__(self):
        self.delegator_map = {}

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((JsonRpcServer.HOST, JsonRpcServer.PORT))
        self.sock.listen(0)
        logging.info("Server listening on {0}:{1}.".format(JsonRpcServer.HOST, JsonRpcServer.PORT))
        while True:
            client_sock, client_addr = self.sock.accept()
            logging.info("Connected with client from {0}".format(client_addr))
            _HandlerThread(client_sock, self.delegator_map).start()

    def stop(self):
        self.sock.close()
        logging.info("Server stopped.")

    def register(self, delegator_name, delegator):
        if not isinstance(delegator_name, basestring):
            raise TypeError('delegator_name should be a string')
        self.delegator_map[delegator_name] = delegator


class _HandlerThread(threading.Thread):
    def __init__(self, client_sock, delegator_map):
        super(_HandlerThread, self).__init__()
        self.client_sock = client_sock
        self.delegator_map = delegator_map

    def run(self):
        while True:
            request_json = self.client_sock.recv(JsonRpcServer.BUFSIZE)
            if not request_json:
                break
            self.client_sock.sendall(self._handle_request(request_json))
        self.client_sock.close()

    def _handle_request(self, request_json):
        delegator_name, method_name, param_list = self._parse_request_json(request_json)
        the_method = getattr(self.delegator_map[delegator_name], method_name)
        raw_result = the_method(*param_list)
        return json.dumps(raw_result)

    def _parse_request_json(self, request_json):
        request_obj = json.loads(request_json)
        return request_obj['delegator'], request_obj['method'], request_obj['param_list']
