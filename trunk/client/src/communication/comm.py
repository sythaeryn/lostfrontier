from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import reactor

class Echo(Protocol):
    '''
    def connectionMade(self):
        global login
        self.transport.write('connect;loginaqui;passhere')'''

    def sendMessage(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        self.factory.handler.computeData(data)

class EchoClientFactory(ReconnectingClientFactory):
    protocol = None
    handler = None

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        self.resetDelay()
        self.protocol = Echo()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class Handler:
    def __init__(self):
        self.factory = EchoClientFactory()
        self.factory.handler = self
        reactor.connectTCP('localhost', 8000, self.factory)

    def computeData(self, data):
        pass

    def sendMessage(self, message):
        self.factory.protocol.sendMessage(message)
        