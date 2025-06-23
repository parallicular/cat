import pygame


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60


class Cat:
    def __init__(self) -> None:
        self.images = self.load_images()
        self.current_frame = 0
        self.frame_counter = 0
        self.current_animation = "jump"
        
        self.position = {
            "x": SCREEN_WIDTH // 2,
            "y": SCREEN_HEIGHT // 2
        }
        
    def load_images(self):
        images = {}
        images["walk"] = self.load_animation("walk", 8)
        images["run"] = self.load_animation("run", 5)
        images["jump"] = self.load_animation("jump", 7)
        return images
    
    def load_animation(self, name, frame_count):
        images = []
        for i in range(1, frame_count + 1):
            image = pygame.image.load(f"images/cat/{name}/{i}.png")
            image = pygame.transform.scale(image, (100, 100))
            images.append(image)
        return images
    
    def handle_pressed_keys(self, pressed_keys):
        if pressed_keys[pygame.K_RIGHT]:
            self.position["x"] += 4
        if pressed_keys[pygame.K_LEFT]:
            self.position["x"] -= 4
        if pressed_keys[pygame.K_UP]:
            self.position["y"] -= 4
        if pressed_keys[pygame.K_DOWN]:
            self.position["y"] += 4

    def draw(self, screen):
        position_tuple = (self.position["x"], self.position["y"])
        
        image = self.images[self.current_animation][self.current_frame]
        
        screen.blit(image, position_tuple)
        self.frame_counter += 1
        if self.frame_counter > 8:
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_animation])
            self.frame_counter = 0


class Background:
    def __init__(self):
        self.image = pygame.image.load("images/small.png")
        self.x = 0
    
    def draw(self, screen):
        self.x -= 1
        
        offset_y = 0
        while offset_y < screen.get_height():
            offset_x = self.x
            while offset_x < screen.get_width():
                screen.blit(self.image, (offset_x, offset_y))
                offset_x += self.image.get_width()
            offset_y += self.image.get_height()

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.cat = Cat()

    def draw(self, screen):
        self.background.draw(screen)
        self.cat.draw(screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            pressed_keys = pygame.key.get_pressed()
            self.cat.handle_pressed_keys(pressed_keys)
            if pressed_keys[pygame.K_ESCAPE]:
                running = False

            self.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
