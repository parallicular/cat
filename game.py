import pygame
from cat import Cat
from background import Background
from block import Block

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60
GROUND_LEVEL = 700


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.blocks = self.create_blocks()
        cat_pos: pygame.Vector2 = pygame.Vector2(SCREEN_WIDTH // 2, GROUND_LEVEL - 100)
        self.cat = Cat(cat_pos)
        
    def create_blocks(self):
        blocks: list[Block] = []
        offset_x = 0
        while offset_x < self.screen.get_width():
            position = pygame.Vector2(offset_x, GROUND_LEVEL)
            block = Block(position)
            blocks.append(block)
            offset_x += 100

        return blocks

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

            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
