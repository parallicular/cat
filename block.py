import pygame


class Block:
    def __init__(self, position: pygame.Vector2):
        self.image = pygame.image.load("images/ground.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.position = position

    def update(self, scroll_speed):
        self.position.x += scroll_speed
        self.rect.left = int(self.position.x)
        return self.rect.right >= 0
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
