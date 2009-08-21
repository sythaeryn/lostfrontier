import direct.directbase.DirectStart
from pandac.PandaModules import *

world = loader.loadModel('models/environment')
world.reparentTo(render)
world.setScale(0.4, 0.4, 0.4)
world.setPos(-8, 90, -3.6)