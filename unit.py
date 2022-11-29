import pygame
from pygame import Vector2

DEFAULT_COLOR = (231, 196, 91)

WIDTH = 42
HEIGHT = 81
GROUND_HEIGHT = 21

DEFAULT_SPEED = 400 / 1000
MOVE_TARGET_CLOSENESS = 10


class Unit:

    def __init__(self, pos):
        self._pos = Vector2(pos)  # center of ground box

        self.rect = pygame.Rect(pos[0] - WIDTH // 2,
                                pos[1] + GROUND_HEIGHT // 2 - HEIGHT,
                                WIDTH,
                                HEIGHT)
        self.ground_box = pygame.Rect(pos[0] - WIDTH // 2,
                                      pos[1] - GROUND_HEIGHT // 2,
                                      WIDTH,
                                      GROUND_HEIGHT)

        self.move_direction = Vector2()
        self.speed = 400 / 1000  # pxls per sec

        self.move_target_pos = None

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        new_x, new_y = new_pos

        self._pos = new_pos

        self.rect.x = new_x - WIDTH // 2
        self.rect.y = new_y + GROUND_HEIGHT // 2 - HEIGHT

        self.ground_box.x = new_x - WIDTH // 2
        self.ground_box.y = new_y - GROUND_HEIGHT // 2

    def update(self, frame_time_ms):
        if self.move_target_pos is not None:
            # if has target position
            self.move_direction = (self.move_target_pos - self.pos).normalize()

            self.pos += self.move_direction * self.speed * frame_time_ms

            if (self.move_target_pos - self.pos).length() <= MOVE_TARGET_CLOSENESS:
                self.move_target_pos = None

    def move_order(self, target_pos):
        self.move_target_pos = Vector2(target_pos)

    def draw(self, surface):
        pygame.draw.rect(surface, DEFAULT_COLOR, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.ground_box, 1)
        pygame.draw.circle(surface, (255, 0, 0), self.pos, 1)
