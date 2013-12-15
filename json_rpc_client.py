import socket
import json
import logging

from .json_rpc_server import JsonRpcServer


logging.basicConfig(level=logging.DEBUG)


class JsonRpcClient(object):
    def __init__(self):
        pass

    def connect(self, server_addr, server_port=50000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_addr, server_port))

    def get_remote_delegator(self, delegator_name):
        return _RemoteDelegator(self.sock, delegator_name)


class _RemoteDelegator(object):
    BUFSIZE = 4096

    def __init__(self, sock, delegator_name):
        self.sock = sock
        self.delegator_name = delegator_name

    def __getattr__(self, method_name):
        def remote_method(*args):
            self.sock.send(self._make_request_json(method_name, args))
            response_json = self.sock.recv(_RemoteDelegator.BUFSIZE)
            logging.debug("Response JSON received: {0}".format(response_json))
            return json.loads(response_json)
        return remote_method

    def _make_request_json(self, method_name, args):
        request_obj = {'delegator': self.delegator_name, 'method': method_name, 'param_list': args}
        request_json = json.dumps(request_obj)
        logging.debug("Request json made: {0}".format(request_json))
        return request_json
