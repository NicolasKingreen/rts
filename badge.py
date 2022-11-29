import pygame.draw

DEFAULT_COLOR = (255, 0, 0)
CONTOUR_COLOR = (231, 231, 231)


class Badge:
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
    def center(self, new_center):
        pass

    def update_pos(self):
        self._calculate_points()

    def _calculate_points(self):
        pass

    def draw(self, surface):
        pygame.draw.polygon(surface, DEFAULT_COLOR, self.points)
        if self.unit.selected:
            pygame.draw.polygon(surface, CONTOUR_COLOR, self.points, 1)


class Rhombus(Badge):
    def __init__(self, unit):
        self.width = 30
        self.height = 40
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

    def _calculate_points(self):
        # it has to know its dimensions
        center = self.center
        self.points = [
            (center[0], center[1] - self.height // 2),
            (center[0] + self.width // 2, center[1]),
            (center[0], center[1] + self.height // 2),
            (center[0] - self.width // 2, center[1])
        ]


