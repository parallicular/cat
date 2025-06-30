import pygame
from cat import Cat
from background import Background
from block import Block
from random import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60
GROUND_LEVEL = 700
BLOCK_SIZE = 100


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.blocks = self.create_blocks()
        cat_pos: pygame.Vector2 = pygame.Vector2(SCREEN_WIDTH // 2, GROUND_LEVEL - BLOCK_SIZE)
        self.cat = Cat(cat_pos)
        self.scroll_offset = 0.0
        self.generated_until = float(self.screen.get_width())
        self.scroll_speed = -0.1
        
    def create_blocks(self):
        blocks: list[Block] = []
        offset_x = 0
        while offset_x < self.screen.get_width():
            position = pygame.Vector2(offset_x, GROUND_LEVEL)
            block = Block(position)
            blocks.append(block)
            offset_x += BLOCK_SIZE
        return blocks
    
    def update(self):
        self.scroll_speed -= 0.01
        self.scroll_speed = max(self.scroll_speed, -10)
        
        # generate world
        self.generated_until += self.scroll_speed
        if self.generated_until < self.screen.get_width():
            new_pos = pygame.Vector2(self.generated_until, GROUND_LEVEL)
            new_block = Block(new_pos)
            self.blocks.append(new_block)
            
            if random() < 0.05:
                row_index = int(7 * random())
                new_pos = pygame.Vector2(self.generated_until, BLOCK_SIZE * row_index)
                new_block = Block(new_pos)
                self.blocks.append(new_block)

            self.generated_until += BLOCK_SIZE
        
        self.background.update(self.scroll_speed)
        new_blocks = []
        for block in self.blocks:
            if block.update(self.scroll_speed):
                new_blocks.append(block)
        self.blocks = new_blocks
        self.cat.update(self.scroll_speed)

    def draw(self):
        self.background.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)
        self.cat.draw(self.screen)

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            self.cat.handle_events(events)
            
            pressed_keys = pygame.key.get_pressed()
            self.cat.handle_pressed_keys(pressed_keys)
            if pressed_keys[pygame.K_ESCAPE]:
                running = False

            self.update()

            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
