from base.Person import Person
from os import sep
import yaml
from characterControl.Camera import Camera

# Pega as teclas do arquivo de configuracao
configure_path = "config"+sep+"keycontrols.yml"
ymlfile = open(configure_path).read()
keyconfig = yaml.load(ymlfile)

class Player(Person,object):

    smoth_mov = False
    camera = None

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

    def load_char(self):
        super(Player, self).load_char()
        taskMgr.add( self.adj_cam, 'adjustCamera')

    def adj_cam(self,task):

        if (self.state_key['aim'] == 0):

            if (self.smoth_mov):
                self.camera.set_cam_pos(0.0,30.0,3.0)
                self.smoth_mov = False
            else:
                self.camera.cam_follow(30.0,3.0)
                self.camera.look(self.person)
            
        else:
            if ( not self.smoth_mov):

                self.camera.set_cam_pos(-5.0,20.0,10.0)
                self.smoth_mov = True

            else:
                self.camera.cam_follow(20.0,10.0,-5.0)
        
        return task.cont

    def change_state(self, key, value):
        self.state_key[key] = value