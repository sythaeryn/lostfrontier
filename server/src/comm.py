from character.Player import Player

from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Echo(Protocol):
    def connectionMade(self):
        print "Abrindo uma Conexao."
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Fechando uma Conexao."
        self.factory.clients.remove(self)

    def sendMessage(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        self.factory.handler.computeData(self, data)        

class Handler:
    def __init__(self):
        pass

    def computeData(self, echo, data):
        print data
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