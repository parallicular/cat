import pygame
from animation import Animation

class Obstacle:
    def __init__(self, position: pygame.Vector2):
        self.animation = Animation("fireball", 4, 7, "")
        # self.image = pygame.image.load("images/fireball.png")
        # self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(position, (100, 100))
        self.position = position
        self.deleted = False

    def draw(self, screen: pygame.Surface, scroll_offset: float):
        draw_rect = self.rect.move(-scroll_offset, 0)
        if draw_rect.right >= 0:
            self.animation.draw(screen, draw_rect)
        else:
            self.deleted = True
