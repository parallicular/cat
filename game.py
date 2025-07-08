import pygame
from pygame import Vector2
from cat import Cat
from background import Background
from gameEntity import Block
from gameEntity import Obstacle
from random import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60
BLOCK_SIZE = 100
GROUND_LEVEL = SCREEN_HEIGHT - BLOCK_SIZE
ENDPOINT = 10000 
WALK_TO_ENDPOINT = ENDPOINT - 100
STOP_GENERATING_OBSTACLES = ENDPOINT - 1000 
FONT_SIZE = 48


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/ruins.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.background = Background()
        
        self.obstacles: list[Obstacle] = []
        
        cat_pos = Vector2(SCREEN_WIDTH // 4, GROUND_LEVEL - BLOCK_SIZE)
        self.cat = Cat(cat_pos)
        self.scroll_offset = 0.0
        self.scroll_speed = 0.1
        self.generated_until = 0
        self.block_chance = 0.1
        self.fireball_chance = 0.01
        
        self.blocks: list[Block] = []
        self.generate_world()

        self.pause = False

    def draw_pause_screen(self):
        pause_bar = pygame.Surface((SCREEN_WIDTH, BLOCK_SIZE), pygame.SRCALPHA)
        pause_bar.fill((0, 0, 0)) 
        self.screen.blit(pause_bar, (0, SCREEN_HEIGHT - BLOCK_SIZE)) # black color fills the bottom part of the screen only

        font = pygame.font.SysFont(None, FONT_SIZE)
        restart = font.render('[R] Restart', True, (255, 255, 255), None)
        pause = font.render('PAUSED', True, (255, 255, 0), None)
        quit = font.render('[Q] Quit', True, (255, 255, 255), None)
        self.screen.blit(restart, (SCREEN_WIDTH / 4, SCREEN_HEIGHT - BLOCK_SIZE / 1.5))
        self.screen.blit(quit, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - BLOCK_SIZE / 1.5))
        self.screen.blit(pause, (SCREEN_WIDTH / 2 - pause.get_width() / 2, SCREEN_HEIGHT / 2 - FONT_SIZE // 2))


    def generate_world(self):
        while self.generated_until < self.scroll_offset + self.screen.get_width():
            position = Vector2(self.generated_until, GROUND_LEVEL)
            block = Block(position)
            self.blocks.append(block)
            
            allow_obstacles = self.generated_until < STOP_GENERATING_OBSTACLES

            if allow_obstacles:
                if random() < self.block_chance:
                    row_index = int(7 - abs(7 * (random() + random()) - 7))
                    position = Vector2(self.generated_until, BLOCK_SIZE * row_index)
                    block = Block(position)
                    self.blocks.append(block)
                    
                if random() < self.fireball_chance:
                    row_index = int(7 - abs(7 * (random() + random()) - 7))
                    new_pos = Vector2(self.generated_until, BLOCK_SIZE * row_index)
                    new_obstacle = Obstacle(new_pos)
                    self.obstacles.append(new_obstacle)
                self.fireball_chance = min(0.2, self.fireball_chance + 0.001)

            self.generated_until += BLOCK_SIZE


    def update(self):
        self.scroll_speed += 0.003
        self.scroll_speed = min(self.scroll_speed, 12)
    
        self.scroll_offset += self.scroll_speed

        # print(f"game: {self.scroll_offset}")

        if self.scroll_offset >= ENDPOINT:
            self.cat.won = True
            self.scroll_speed = 0

        elif self.scroll_offset >= WALK_TO_ENDPOINT and self.cat.alive and not self.cat.in_air:
            self.cat.safe = True
            self.scroll_speed = 1

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
                if self.pause:
                    self.draw_pause_screen()
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        return 'q'
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.pause = not self.pause
                    
                        elif self.pause:
                            if event.key == pygame.K_r:
                                return 'r'
                            elif event.key == pygame.K_q:
                                return 'q'

                # pressed_keys = pygame.key.get_pressed()

                if not self.pause:
                    if self.cat.alive:
                        self.update()
                    # elif pressed_keys[pygame.K_r]:
                    #     self.cat = Cat(Vector2(self.scroll_offset + SCREEN_WIDTH // 4, GROUND_LEVEL - BLOCK_SIZE))

                    self.draw()

                pygame.display.flip()
                self.clock.tick(FPS)


def main():
    while True:
        game = Game()
        choice = game.run()
        if choice == 'q':
            break
        elif choice == 'r':
            continue
    pygame.quit()


if __name__ == '__main__':
    main()
