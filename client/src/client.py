import direct.directbase.DirectStart
from characterControl import Player
from worldControl import World
from pandac.PandaModules import WindowProperties
from communication.comm import Handler

from twisted.internet.task import LoopingCall
from twisted.internet import reactor

p = Player()
h = Handler()

def step():
    try:
        taskMgr.step()
    except:
        reactor.stop()

def sendInformation():
    global h, p

    if len(p.moviment_historic) > 0:
        moviment = p.moviment_historic.pop()
        message = "moviment;"+moviment[0]+";"+moviment[1]
        h.sendMessage(message)

if __name__ == '__main__':
    props = WindowProperties()
    props.setCursorHidden(True)
    base.win.requestProperties(props)

    #Twisted
    LoopingCall(step).start(1 / 60)
    LoopingCall(sendInformation).start(1 / 60)
    reactor.run()