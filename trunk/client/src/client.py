import direct.directbase.DirectStart
from characterControl import Player
from worldControl import World
from pandac.PandaModules import WindowProperties

if __name__ == '__main__':
    props = WindowProperties()
    props.setCursorHidden(True)
    base.win.requestProperties(props)
    
    p = Player()
    run()
