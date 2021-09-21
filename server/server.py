from twisted.internet import reactor, protocol
from serverControlCenter import ControlCenter
import json

class Echo(protocol.Protocol):

    def __init__(self):
        self._control = ControlCenter()
        reactor.callInThread(self._manageCallsQueue)
    
    def _manageCallsQueue(self):
        while True:
            response = self._control.manageCallsQueue()
            if response:
                self.transport.write(response.encode('utf-8'))

    def dataReceived(self, data):
        for data in data.decode('utf-8').replace('}{', '}|{').split('|'):
            data = json.loads(data)
            print(data)
            response = self._control.manageCommands(data)
            self.transport.write(response.encode('utf-8'))

def main(port):
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == "__main__":
    main(5678)
    