from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import reactor

from Crypto.Cipher import Blowfish

class Echo(Protocol):
    '''
    def connectionMade(self):
        global login
        self.transport.write('connect;loginaqui;passhere')'''

    def sendMessage(self, message):
        secureMessage = self.handler.encrypt(message)
        self.transport.write(secureMessage)

    def dataReceived(self, data):
        plainData =  self.handler.decrypt(data)
        self.handler.computeData(plainData)

class EchoClientFactory(ReconnectingClientFactory):
    protocol = None
    handler = None

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        self.resetDelay()
        self.protocol = Echo()
        self.protocol.handler = self.handler
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

        self.crypt = Blowfish.new('lostfrontier', 1)
        self.crypt_blocksize = 8

    def computeData(self, data):
        pass

    def sendMessage(self, message):
        self.factory.protocol.sendMessage(message)
        
    def decrypt(self, data):
        if len(data)%8 == 0:
            plain = self.crypt.decrypt(data)
            return plain.strip(';X')
        else:
            return None

    def encrypt(self, data):
        data += ';'
        data += 'X'*(self.crypt_blocksize-len(data)%self.crypt_blocksize)
        return self.crypt.encrypt(data)

        