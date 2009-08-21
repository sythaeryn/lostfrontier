from base.Person import Person
from os import sep
import yaml

# Pega as teclas do arquivo de configuracao
configure_path = "config"+sep+"keycontrols.yml"
ymlfile = open(configure_path).read()
keyconfig = yaml.load(ymlfile)

class Player(Person):

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

        self.accept( keyconfig['walk_left_key'], self.change_state, ['walk_left',1] )
        self.accept( keyconfig['walk_right_key'], self.change_state, ['walk_right',1] )
        self.accept( keyconfig['walk_left_key']+'-up', self.change_state, ['walk_left',0] )
        self.accept( keyconfig['walk_right_key']+'-up', self.change_state, ['walk_right',0] )


    def change_state(self, key, value):
        self.state_key[key] = value