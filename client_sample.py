from .json_rpc_client import JsonRpcClient


client = JsonRpcClient()
client.connect('127.0.0.1', 50000)
calculator = client.get_remote_delegator('calculator')
print "Calculate by remote calculator: 2 + 3 = {0}".format(calculator.add(2, 3))
