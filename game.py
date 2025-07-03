import pygame
from cat import Cat
from background import Background
from block import Block
from obstacle import Obstacle
from random import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60
GROUND_LEVEL = 700
BLOCK_SIZE = 100


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/ruins.mp3")
        pygame.mixer.music.play()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.blocks = self.create_blocks()
        self.obstacles = []
        cat_pos: pygame.Vector2 = pygame.Vector2(SCREEN_WIDTH // 4, GROUND_LEVEL - BLOCK_SIZE)
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
        self.scroll_speed -= 0.003
        self.scroll_speed = max(self.scroll_speed, -12)
        
        # generate world
        self.generated_until += self.scroll_speed
        if self.generated_until < self.screen.get_width():
            new_pos = pygame.Vector2(self.generated_until, GROUND_LEVEL)
            new_obstacle = Block(new_pos)
            self.blocks.append(new_obstacle)
            
            if random() < 0.5:
                row_index = int(7 * random())
                new_pos = pygame.Vector2(self.generated_until, BLOCK_SIZE * row_index)
                new_obstacle = Obstacle(new_pos)
                self.obstacles.append(new_obstacle)

            self.generated_until += BLOCK_SIZE
        
        self.background.update(self.scroll_speed)
        new_blocks = []
        for block in self.blocks:
            if block.update(self.scroll_speed):
                new_blocks.append(block)
        self.blocks = new_blocks

        new_obstacles = []
        for obstacle in self.obstacles:
            if obstacle.update(self.scroll_speed):
                new_obstacles.append(obstacle)
        self.obstacles = new_obstacles

        self.cat.update(self.scroll_speed, self.obstacles)

    def draw(self):
        self.background.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.cat.draw(self.screen)

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                running = False

            if self.cat.alive:
                self.cat.handle_events(events)
                
                self.cat.handle_pressed_keys(pressed_keys)

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
