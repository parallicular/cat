import pygame
from cat import Cat
from background import Background
from gameEntity import Block
from gameEntity import Obstacle
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
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.background = Background()
        
        self.obstacles: list[Obstacle] = []
        
        cat_pos = pygame.Vector2(SCREEN_WIDTH // 4, GROUND_LEVEL - BLOCK_SIZE)
        self.cat = Cat(cat_pos)
        self.scroll_offset = 0.0
        self.scroll_speed = 0.1
        self.generated_until = 0
        self.block_chance = 0.1
        self.fireball_chance = 0.01
        
        self.blocks: list[Block] = []
        self.generate_world()
        
    def generate_world(self):
        while self.generated_until < self.scroll_offset + self.screen.get_width():
            position = pygame.Vector2(self.generated_until, GROUND_LEVEL)
            block = Block(position)
            self.blocks.append(block)
            
            if random() < self.block_chance:
                row_index = int(7 - abs(7 * (random() + random()) - 7))
                position = pygame.Vector2(self.generated_until, BLOCK_SIZE * row_index)
                block = Block(position)
                self.blocks.append(block)
                
            elif random() < self.fireball_chance:
                row_index = int(7 - abs(7 * (random() + random()) - 7))
                new_pos = pygame.Vector2(self.generated_until, BLOCK_SIZE * row_index)
                new_obstacle = Obstacle(new_pos)
                self.obstacles.append(new_obstacle)
            self.fireball_chance = min(0.2, self.fireball_chance + 0.001)
            
            self.generated_until += BLOCK_SIZE

    def update(self):
        self.scroll_speed += 0.003
        self.scroll_speed = min(self.scroll_speed, 12)
        
        self.scroll_offset += self.scroll_speed
        
        self.generate_world()
        
        self.cat.update(self.scroll_speed, self.obstacles, self.blocks)

    def draw(self):
        self.background.draw(self.screen, self.scroll_offset)
        for block in self.blocks:
            block.draw(self.screen, self.scroll_offset)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.scroll_offset)
        self.cat.draw(self.screen, self.scroll_offset)

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
                self.update()
            elif pressed_keys[pygame.K_r]:
                self.cat = Cat(pygame.Vector2(self.scroll_offset + SCREEN_WIDTH // 4, GROUND_LEVEL - BLOCK_SIZE))

            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
