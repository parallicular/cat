import pygame


class Obstacle:
    def __init__(self, position: pygame.Vector2):
        self.image = pygame.image.load("images/fireball.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.position = position

    def update(self, scroll_speed: float):
        self.position.x += scroll_speed
        self.rect.left = int(self.position.x)
        return self.rect.right >= 0
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
