import pygame

FPS = 60


def init():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    
    return {
        "screen": screen,
        "clock": clock
    }


def run_game(game):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game["screen"].fill("red")
        pygame.display.flip()
        
        game["clock"].tick(FPS)


def main():
    game = init()
    run_game(game)
    pygame.quit()


if __name__ == '__main__':
    main()
