import pygame


class Block:
    def __init__(self, position: pygame.Vector2):
        self.image = pygame.image.load("images/ground.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.position = position
        self.deleted = False

    def draw(self, screen: pygame.Surface, scroll_offset: float):
        draw_rect = self.rect.move(-scroll_offset, 0)
        if draw_rect.right >= 0:
            screen.blit(self.image, draw_rect)
        else:
            self.deleted = True
