from direct.showbase.DirectObject import DirectObject

class Camera(DirectObject):

    def __init__(self):
        lente = base.cam.node().getLens()
        lente.setFov(40)
        base.cam.node().setLens(lente)
        base.camera.reparentTo(render)

    def look(self,obj):
        base.camera.lookAt(obj)

    def set_cam_pos(self,x,y,z):
        base.camera.setPos(x,y,z)

    def cam_follow(self,obj,dist,hei,sid = 0):
        base.camera.setPos(obj, sid, dist, hei)
