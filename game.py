import pygame


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60


class Cat:
    def __init__(self) -> None:
        self.image = pygame.image.load("images/cat/walk/1.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.position = {
            "x": SCREEN_WIDTH // 2,
            "y": SCREEN_HEIGHT // 2
        }

    def draw(self, screen):
        position_tuple = (self.position["x"], self.position["y"])
        screen.blit(self.image, position_tuple)


def init():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    images = {
        'background': pygame.image.load("images/blue-sky.jpg"),
    }
    
    return {
        "screen": screen,
        "clock": clock,
        "images": images,
        "cat": Cat()
    }


def run_game(game):
    running = True
    screen: pygame.Surface = game["screen"]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            game["cat"].position["x"] += 4
        if pressed_keys[pygame.K_LEFT]:
            game["cat"].position["x"] -= 4
        if pressed_keys[pygame.K_UP]:
            game["cat"].position["y"] -= 4
        if pressed_keys[pygame.K_DOWN]:
            game["cat"].position["y"] += 4
        if pressed_keys[pygame.K_ESCAPE]:
            running = False

        screen.blit(game["images"]["background"], (0, 0))
        game["cat"].draw(screen)

        pygame.display.flip()
        game["clock"].tick(FPS)


def main():
    game = init()
    run_game(game)
    pygame.quit()


if __name__ == '__main__':
    main()
