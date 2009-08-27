from base.Person import Person
from os import sep
import yaml
import math
from characterControl.Camera import Camera

# Pega as teclas do arquivo de configuracao
configure_path = "config"+sep
ymlfile_keys = open(configure_path+"keycontrols.yml").read()
keyconfig = yaml.load(ymlfile_keys)

ymlfile_conf = open(configure_path+"game_conf.yml").read()
gameconf = yaml.load(ymlfile_conf)

class Player(Person,object):

    smoth_mov = False
    camera = None
    sensivity_x = gameconf['sensivity_x']
    lastX = 0
    lastY = 0
    sensivity_y = gameconf['sensivity_y']

    moviment_historic = []

    def __init__(self):
        super(Player, self).__init__()
        self.camera = Camera(self.person)

    def catch_events(self):
        #Caputra entrada dos teclados para rotacao
        self.accept( keyconfig['right_key'], self.change_state, ['right',1] )
        self.accept( keyconfig['left_key'], self.change_state, ['left',1] )
        self.accept( keyconfig['right_key']+'-up', self.change_state, ['right',0] )
        self.accept( keyconfig['left_key']+'-up', self.change_state, ['left',0] )

        self.accept( keyconfig['up_key'], self.change_state, ['up',1] )
        self.accept( keyconfig['down_key'], self.change_state, ['down',1] )
        self.accept( keyconfig['up_key']+'-up', self.change_state, ['up',0] )
        self.accept( keyconfig['down_key']+'-up', self.change_state, ['down',0] )

        self.accept( keyconfig['aim_key'], self.change_state, ['aim',1] )
        self.accept( keyconfig['aim_key']+'-up', self.change_state, ['aim',0] )

        self.accept( keyconfig['crouch_key'], self.change_state, ['crouch', 1])
        self.accept( keyconfig['crouch_key']+'-up', self.change_state, ['crouch', 0])

        self.accept( keyconfig['walk_left_key'], self.change_state, ['walk_left',1] )
        self.accept( keyconfig['walk_right_key'], self.change_state, ['walk_right',1] )
        self.accept( keyconfig['walk_left_key']+'-up', self.change_state, ['walk_left',0] )
        self.accept( keyconfig['walk_right_key']+'-up', self.change_state, ['walk_right',0] )

        self.accept( 'wheel_down', self.adj_zoom, [1] )
        self.accept( 'wheel_up', self.adj_zoom, [-1] )

    def load_char(self):
        super(Player, self).load_char()
        taskMgr.add( self.adj_cam, 'adjustCamera')

    def adj_zoom(self,value):
        if (((gameconf['zoom'] < gameconf['zoom_limit_up']) and (value > 0)) or ((gameconf['zoom'] > gameconf['zoom_limit_down']) and (value < 0))):
            gameconf['zoom'] += value

    def adj_cam(self,task):

        if (self.state_key['aim'] == 0):

            if (self.smoth_mov):
                self.state_key['speed_side'] = gameconf['speed_side_keys']
                self.camera.set_cam_pos(0.0,gameconf['zoom'],gameconf['height'])
                self.smoth_mov = False
                self.change_state('right', 0)
                self.change_state('left', 0)
            else:
                self.camera.cam_follow(gameconf['zoom'],gameconf['height'])
                self.camera.look(self.person)
            
        else:
            if ( not self.smoth_mov):

                self.camera.set_cam_pos(-5.0,20.0,10.0)
                self.smoth_mov = True

            else:                
                mpos = base.mouseWatcherNode.getMouse()
                self.camera.cam_follow(20.0,10.0,-5.0)
                if base.mouseWatcherNode.hasMouse():
                    posx = mpos.getX()
                    posy = mpos.getY()
                    if (self.lastY != posy):
                        base.camera.setP(base.camera.getP() + (posy - self.lastY) * self.sensivity_y)
                        self.lastY = posy

                    if (self.lastX != posx):
                        if (posx > self.lastX):
                            self.state_key['speed_side'] = gameconf['speed_side_mouse']
                            self.change_state('right', 1)
                            self.change_state('left', 0)
                        elif (posx < self.lastX):
                            self.state_key['speed_side'] = gameconf['speed_side_mouse']
                            self.change_state('right', 0)
                            self.change_state('left', 1)
                        self.lastX = posx
                    else:
                        self.change_state('right', 0)
                        self.change_state('left', 0)

        return task.cont

    def change_state(self, key, value):
        if key != 'speed_side' and (self.state_key['aim'] == 0 or not (self.state_key['aim'] == 1 and key != 'aim')):
            self.moviment_historic.insert(0, (str(key), str(value)))

        self.state_key[key] = value