import pygame
from pygame import Surface

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
ENDPOINT = 10000
SKY_TRANSITION = ENDPOINT - 1500
BLOCK_SIZE = 100
GROUND_LEVEL = SCREEN_HEIGHT - BLOCK_SIZE

class Background:
    def __init__(self):
        self.image1 = pygame.image.load("images/small.png")
        self.image2 = pygame.image.load("images/blue-sky-303x209.jpg")
        self.house = pygame.image.load("images/house.png")

        self.house_pos = (ENDPOINT + 600, GROUND_LEVEL - self.house.get_height()) # the 600 is arbitrary - the house gets drawn way before the endpoint otherwise and the cat walks past it

        self.tile_width = self.image1.get_width()
        self.tile_height = self.image1.get_height()

        self.sky_start = SKY_TRANSITION

    def draw(self, screen: Surface, scroll_offset: float): # ChatGPT's solution for drawing tile-by-tile so that the whole screen doesn't flip from bricks to sky instantly
        offset_y = 0
        while offset_y < screen.get_height():
            offset_x = (-scroll_offset % self.tile_width) - self.tile_width
            tile_index = 0

            while offset_x < screen.get_width():
                # Calculate absolute position of this tile in the world
                tile_world_x = scroll_offset - (scroll_offset % self.tile_width) + tile_index * self.tile_width

                if tile_world_x < self.sky_start:
                    image = self.image1 # brick
                else:
                    image = self.image2 # sky

                screen.blit(image, (offset_x, offset_y))
                offset_x += self.tile_width
                tile_index += 1

            offset_y += self.tile_height

        house_x = self.house_pos[0] - scroll_offset
        house_y = self.house_pos[1]
        screen.blit(self.house, (house_x, house_y))

