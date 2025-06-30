import pygame


class Background:
    def __init__(self):
        self.image = pygame.image.load("images/small.png")
        self.x = 0
    
    def draw(self, screen):
        self.x -= 1
        
        offset_y = 0
        while offset_y < screen.get_height():
            offset_x = self.x
            while offset_x < screen.get_width():
                screen.blit(self.image, (offset_x, offset_y))
                offset_x += self.image.get_width()
            offset_y += self.image.get_height()