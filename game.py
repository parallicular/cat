import pygame


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60


def init():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    cat_img = pygame.image.load("images/cat/walk1.png")
    cat_img = pygame.transform.scale(cat_img, (64, 64))
    
    images = {
        'background': pygame.image.load("images/blue-sky.jpg"),
        'cat': cat_img
    }
    
    return {
        "screen": screen,
        "clock": clock,
        "images": images
    }


def run_game(game):
    running = True
    screen: pygame.Surface = game["screen"]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(game["images"]["background"], (0, 0))
        screen.blit(game["images"]["cat"], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        game["clock"].tick(FPS)


def main():
    game = init()
    run_game(game)
    pygame.quit()


if __name__ == '__main__':
    main()
