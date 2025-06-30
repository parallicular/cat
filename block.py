import pygame


class Block:
    def __init__(self, position):
        self.image = pygame.image.load("images/ground.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
