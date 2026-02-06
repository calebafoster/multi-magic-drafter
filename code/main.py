import pygame
import threading
import sys
from listener import Listener
from state_machine import StateMachine
import game

# idea for powerups: click on card to guarantee color identity match
# as well as click to reroll or block cards for the next person to take

STATE_DICT = {
        "GAME": game.Game(),
        }

class Main:
    def __init__(self, host = "127.0.0.1", port = 55885):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Ethan's Birthday Game 2")
        self.clock = pygame.time.Clock()

        self.player_id = 0

        self.listener = Listener()

        self.state_machine = StateMachine()

        self.state_machine.setup_states(STATE_DICT, "GAME")
        self.state_machine.state.startup({'listener': self.listener})

    def run(self):
        threading.Thread(target=self.listener.run_listener).start()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.listener.kill = True
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(120) / 1000

            self.state_machine.state.update(dt)
            self.state_machine.state.draw(self.display_surface)

            self.display_surface.fill('black')

            pygame.display.update()

if __name__ == "__main__":
    Main().run()
