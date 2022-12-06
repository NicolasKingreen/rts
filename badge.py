import pygame
from pygame.math import Vector2

from abc import ABC, abstractmethod


DEFAULT_COLOR = (255, 0, 0)
CONTOUR_COLOR = (212, 212, 212)


class Badge(ABC):
    def __init__(self, unit, points=None):
        self.unit = unit
        if points is not None:
            self.points = points
        else:
            self._calculate_points()

    @property
    def center(self):
        return self._center

    @center.setter
    @abstractmethod
    def center(self, new_center):
        pass

    @property
    @abstractmethod
    def rect(self):
        return None

    def update_pos(self):
        self._calculate_points()

    @abstractmethod
    def _calculate_points(self):
        pass

    def draw(self, surface):
        pygame.draw.polygon(surface, DEFAULT_COLOR, self.points)
        if self.unit.selected:
            pygame.draw.polygon(surface, CONTOUR_COLOR, self.points, 2)


class Rhombus(Badge):
    def __init__(self, unit):
        # absolute characteristics
        self.width = 30
        self.height = 40

        # relative characteristics
        self.size = 40  # long side

        self.distance = 10

        super().__init__(unit)

    @property
    def center(self):
        return self.unit.rect.centerx, self.unit.rect.top - self.distance - self.height // 2

    @property
    def rect(self):
        return pygame.Rect(self.points[0][0] - self.width,
                           self.points[0][1],
                           self.width,
                           self.height)

    def _calculate_relative_points(self):
        # should be used to simplify badge positioning and sizing
        # e. g. for zooming
        # in this case distance is measured from unit's top to the badge's center
        # height = 1
        # width = 0.75
        center = self.center
        relative_points = [
            (Vector2( 0    ,   -0.5)),
            (Vector2( 0.375,    0  )),
            (Vector2( 0    ,    0.5)),
            (Vector2(-0.375,    0  ))
        ]
        self.points = [center + point * self.size for point in relative_points]

    def _calculate_points(self):
        # badge has to know its absolute dimensions
        center = self.center
        self.points = [
            (center[0], center[1] - self.height // 2),
            (center[0] + self.width // 2, center[1]),
            (center[0], center[1] + self.height // 2),
            (center[0] - self.width // 2, center[1])
        ]


class Square(Badge):
    def __init__(self, unit):
        self.width = self.height = 25
        self.distance = 15
        super().__init__(unit)

    @property
    def center(self):
        return self.unit.rect.centerx, self.unit.rect.top - self.distance - self.height // 2

    @property
    def rect(self):
        return pygame.Rect(self.points[0], (self.width, self.height))

    def _calculate_points(self):
        center = self.center
        self.points = [
            (center[0] - self.width // 2, center[1] - self.height // 2),
            (center[0] + self.width // 2, center[1] - self.height // 2),
            (center[0] + self.width // 2, center[1] + self.height // 2),
            (center[0] - self.width // 2, center[1] + self.height // 2)
        ]
