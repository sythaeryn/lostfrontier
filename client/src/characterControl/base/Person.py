from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor

class Person(DirectObject):

    person = None
    personActor = None
    state_key = None    

    def __init__(self):
        self.load_char()
        self.catch_events()

    def catch_events(self):
        pass

    def load_char(self):
        self.person = render.attachNewNode('persona')

        self.personActor = Actor('resources/eggs/personagem.egg',
                             {'idle':'resources/eggs/personagem-parado',
                              'run' :'resources/eggs/personagem-correr',
                              'jump':'resources/eggs/personagem-pular'}
                             )

        #self.personActor.setScale(.3)
        self.personActor.loop('idle')
        self.personActor.reparentTo(self.person)
        self.personActor.setPos(0,0,1.5)
        self.state_key = {'right':0, 'left':0,'jump': False, 'fall':0,
                          'speed' : 0.8, 'up' : 0, 'down': 0, 'moving' : False,
                          'walk_right' : 0, 'walk_left' : 0, 'crouch' : 0, 'crouching' : False,'aim' : 0}
                          
        self.personActor.enableBlend()
        self.personActor.loop('idle')
        self.personActor.loop('run')
        self.personActor.loop('jump')

        self.person.setPos(0,30,0)
        self.person.setH(0)

        taskMgr.add( self.walk, 'movePerson' )
        taskMgr.add( self.crouch, 'crouchPerson')

    def walk(self,task):

        elapsed = globalClock.getDt()

        #roda o sprite em seu propio eixo
        if (self.state_key['left']!=0):
            self.person.setH(self.person.getH() + ((elapsed*300) * self.state_key['speed'] ))
        if (self.state_key['right']!=0):
            self.person.setH(self.person.getH() - ((elapsed*300) * self.state_key['speed'] ))
        if (self.state_key['up']!=0):
            self.person.setY(self.person, -((elapsed*25) * self.state_key['speed'] ))
        if (self.state_key['down']!=0):
            self.person.setY(self.person, +((elapsed*25) * self.state_key['speed'] ))
        if (self.state_key['walk_right'] != 0):
            self.person.setX(self.person, - ((elapsed*25) * self.state_key['speed'] ))
        if (self.state_key['walk_left'] != 0):
            self.person.setX(self.person, + ((elapsed*25) * self.state_key['speed'] ))


        if ((self.state_key['up'] == 1) or (self.state_key['down'] == 1)):
            if (not self.state_key['moving']):                
                self.state_key['moving'] = True
        else:
            if (self.state_key['moving']):                
                self.state_key['moving'] = False

        self.animation()
        return task.cont

    def animation(self):
        if (self.state_key['crouching'] == True):
            blendAnim = [0, 0, 0, 1.0]
        elif (self.state_key['moving'] == False) and (self.state_key['jump'] == False):
            blendAnim = [1.0, 0.0, 0.0, 0.0]
        elif (self.state_key['moving'] == True) and (self.state_key['jump'] == False):
            blendAnim = [0.0, 1.0, 0.0, 0.0]
        elif (self.state_key['jump'] == True):
            blendAnim = [0.0, 0.0, 1.0, 0.0]
        else:
            blendAnim = [1.0, 0.0, 0.0, 0.0]

        self.personActor.setControlEffect( 'idle', blendAnim[0] )
        self.personActor.setControlEffect( 'run', blendAnim[1] )
        self.personActor.setControlEffect( 'jump', blendAnim[2] )
        self.personActor.setControlEffect( 'jump', blendAnim[3] )


    def attack(self):
        pass

    def jump(self):
        pass

    def aim(self):
        pass

    def shoot(self):
        pass

    def crouch(self, task):
        if self.state_key['crouch'] == 1:
            self.state_key['crouching'] = True
        else:
            self.state_key['crouching'] = False

        self.animation()

        return task.cont
    