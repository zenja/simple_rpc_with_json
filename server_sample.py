from .json_rpc_server import JsonRpcServer


class Calculator(object):
    def add(self, a, b):
        return a + b


server = JsonRpcServer()
calculator = Calculator()
server.register('calculator', calculator)
server.start()
