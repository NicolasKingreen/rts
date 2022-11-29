import pygame
from pygame.locals import *


from unit import Unit


WIN_SIZE = (640, 420)
FPS_LOCK = 60

FILL_COLOR = (231, 231, 231)


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("RTS")
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.is_running = False

        self.lmb_pressed = False
        self.last_click_pos = None

        self.unit = Unit((100, 100))

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick(FPS_LOCK)
            self._handle_events()
            self._update_states(frame_time_ms)
            self._draw_graphics()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.stop()
            elif event.type == KEYUP:
                pass
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(f"LMB on {event.pos}")
                    self.lmb_pressed = True
                    self.last_click_pos = event.pos
                elif event.button == 3:
                    print(f"RMB on {event.pos}, unit on {self.unit.pos}")
                    self.unit.move_order(event.pos)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.lmb_pressed = False

    def _update_states(self, frame_time_ms):
        self.unit.update(frame_time_ms)

    def _draw_graphics(self):
        self.screen.fill(FILL_COLOR)
        self.unit.draw(self.screen)
        if self.lmb_pressed:
            self._draw_selection_frame()
        pygame.display.update()

    def _draw_selection_frame(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click_x, click_y = self.last_click_pos
        if mouse_x > click_x and mouse_y > click_y:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.last_click_pos,
                              (mouse_x - click_x,
                               mouse_y - click_y)),
                             1)
        elif mouse_x > click_x and mouse_y < click_y:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (click_x, mouse_y,
                              mouse_x - click_x,
                              click_y - mouse_y),
                             1)
        elif mouse_x < click_x and mouse_y > click_y:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (mouse_x, click_y,
                              click_x - mouse_x,
                              mouse_y - click_y),
                             1)
        else:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (pygame.mouse.get_pos(),
                              (click_x - mouse_x, click_y - mouse_y)),
                             1)

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    Game().run()
