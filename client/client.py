from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from clientCommands import Commands
import sys
import json

class EchoClient(Protocol):
    
    def __init__(self):
        reactor.callInThread(self._sendData)
        
    def dataReceived(self, data):
        for data in data.decode('utf-8').replace('}{', '}|{').split('|'):
            print(json.loads(data))
        
    def _sendData(self):
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as file:
                for line in file:
                    data = Commands().onecmd(line)
                    if data:
                        self.transport.write(data.encode('utf-8'))
                file.close()
        while True:
            data = Commands().onecmd(input())
            if data:
                self.transport.write(data.encode('utf-8'))
    
class EchoFactory(ClientFactory):
    protocol = EchoClient
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        reactor.stop()

def main(host, port):
    f = EchoFactory()
    reactor.connectTCP(host, port, f)
    reactor.run()

if __name__ == "__main__":
    main('localhost', 5678)
