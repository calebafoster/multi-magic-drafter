class StateMachine:
    def __init__(self):
        self.state_dict = {}
        self.done = False
        self.state_name = None
        
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self, surface):
        self.state.draw(surface)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(persist)
        self.state.previous = previous

class State:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def startup(self, persistant):
        self.persist = persistant

    def add_persistant(self, key, value):
        self.persist[key] = value

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
