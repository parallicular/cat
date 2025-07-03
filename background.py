import pygame


class Background:
    def __init__(self):
        self.image = pygame.image.load("images/small.png")
        
    def draw(self, screen: pygame.Surface, scroll_offset: float):
        offset_y = 0
        while offset_y < screen.get_height():
            offset_x = (-scroll_offset % screen.get_width()) - screen.get_width()
            while offset_x < screen.get_width():
                screen.blit(self.image, (offset_x, offset_y))
                offset_x += self.image.get_width()
            offset_y += self.image.get_height()
