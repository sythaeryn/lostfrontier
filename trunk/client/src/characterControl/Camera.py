from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

class Camera(DirectObject):

    objSeguir = None
    
    def __init__(self,obj):
        base.disableMouse()
        lente = base.cam.node().getLens()
        lente.setFov(40)
        base.cam.node().setLens(lente)
        self.objSeguir = obj
        base.camera.reparentTo(self.objSeguir)

    def look(self,obj):
        base.camera.lookAt(obj)

    def set_cam_pos(self,x,y,z):
        cam = base.camera
        cammov = base.camera.posInterval(0.3,Point3(x,y,z), startPos=Point3(cam.getX(),cam.getY(),cam.getZ()))
        camInt = Sequence(cammov, name = "camInt")
        camInt.start()
        #base.camera.setPos(x,y,z)

    def cam_follow(self,dist,hei,sid = 0.0):
        base.camera.setPos( sid, dist, hei)

    def alt_cam_h(self):
        base.camera.setH(base.camera.getH() + 1)
