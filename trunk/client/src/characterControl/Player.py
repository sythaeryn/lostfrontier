from base.Person import Person

class Player(Person):

    def catch_events(self):
        #Caputra entrada dos teclados para rotacao
        self.accept( 'arrow_right', self.change_state, ['right',1] )
        self.accept( 'arrow_left', self.change_state, ['left',1] )
        self.accept( 'arrow_right-up', self.change_state, ['right',0] )
        self.accept( 'arrow_left-up', self.change_state, ['left',0] )

        self.accept( 'arrow_up', self.change_state, ['up',1] )
        self.accept( 'arrow_down', self.change_state, ['down',1] )
        self.accept( 'arrow_up-up', self.change_state, ['up',0] )
        self.accept( 'arrow_down-up', self.change_state, ['down',0] )

    def change_state(self, key, value):
        self.state_key[key] = value