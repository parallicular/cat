import pygame


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60


class Cat:
    def __init__(self) -> None:
        self.images = self.load_images()
        self.current_frame = 0
        self.frame_counter = 0
        
        self.position = {
            "x": SCREEN_WIDTH // 2,
            "y": SCREEN_HEIGHT // 2
        }
        
    def load_images(self):
        images = []
        for i in range(1, 8 + 1):
            image = pygame.image.load(f"images/cat/walk/{i}.png")
            image = pygame.transform.scale(image, (84, 84))
            images.append(image)
        return images

    def draw(self, screen):
        position_tuple = (self.position["x"], self.position["y"])
        screen.blit(self.images[self.current_frame], position_tuple)
        self.frame_counter += 1
        if self.frame_counter > 8:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_counter = 0


class Background:
    def __init__(self):
        self.image = pygame.image.load("images/bricks.jpg")
        self.x = 0
    
    def draw(self, screen):
        self.x -= 1
        offset = self.x
        while offset < screen.get_width():
            screen.blit(self.image, (offset, 0))
            offset += self.image.get_width()


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.cat = Cat()

    
def run_game(game):
    running = True
    screen: pygame.Surface = game.screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            game.cat.position["x"] += 4
        if pressed_keys[pygame.K_LEFT]:
            game.cat.position["x"] -= 4
        if pressed_keys[pygame.K_UP]:
            game.cat.position["y"] -= 4
        if pressed_keys[pygame.K_DOWN]:
            game.cat.position["y"] += 4
        if pressed_keys[pygame.K_ESCAPE]:
            running = False

        game.background.draw(screen)
        game.cat.draw(screen)

        pygame.display.flip()
        game.clock.tick(FPS)


def main():
    game = Game()
    run_game(game)
    pygame.quit()


if __name__ == '__main__':
    main()
