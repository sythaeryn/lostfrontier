from character.Player import Player

from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from Crypto.Cipher import Blowfish

class Echo(Protocol):
    def connectionMade(self):
        print "Abrindo uma Conexao."
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Fechando uma Conexao."
        self.factory.clients.remove(self)

    def sendMessage(self, message):
        secureMessage = self.factory.handler.encrypt(message)
        self.transport.write(secureMessage)

    def dataReceived(self, data):
        plainData =  self.factory.handler.decrypt(data)
        self.factory.handler.computeData(self, plainData)

class Handler:
    def __init__(self):
        self.crypt = Blowfish.new('lostfrontier', 1)
        self.crypt_blocksize = 8

    def computeData(self, echo, data):
        print data
        if data != None:
            datas = data.split(';')
            response = ''

            # Verify the login and password to connect
            if len(datas) == 3 and datas[0] == "connect":
                #TODO: Verificar no banco
                if(True):
                    response = 'connect;yes'
                    print 'user '+datas[1]+' online.'
                else:
                    response ='connect;no'

            echo.sendMessage(response)

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

variavel = 1
f = Factory()

def nextMessage():
    pass
    '''
    global variavel, f
    #f.protocol.message(f.protocol, str(variavel))
    for client in f.clients:
        client.sendMessage('recebi um numero: '+str(variavel))
    variavel += 1
    print variavel
    '''

def run():
    global f
    f.clients = []
    f.handler = Handler()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    LoopingCall(nextMessage).start(1)
    reactor.run()