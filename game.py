import pygame


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
FPS = 60
GROUND_LEVEL = 600


class Cat:
    def __init__(self) -> None:
        self.load_images()
        self.current_frame = 0
        self.frame_counter = 0
        self.current_animation = "run"
        self.velocity_y = 0
        self.jumping = False
        
        self.position = {
            "x": SCREEN_WIDTH // 2,
            "y": GROUND_LEVEL
        }
        
    def load_images(self):
        self.images = {}
        self.load_animation("walk", 8)
        self.load_animation("run", 5)
        self.load_animation("jump", 5)
    
    def load_animation(self, name, frame_count):
        images = []
        for i in range(1, frame_count + 1):
            image = pygame.image.load(f"images/cat/{name}/{i}.png")
            image = pygame.transform.scale(image, (100, 100))
            images.append(image)
        self.images[name] = images
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.velocity_y = -15
                self.current_animation = "jump"
                self.current_frame = 0
                self.frame_counter = 0
    
    def handle_pressed_keys(self, pressed_keys):
        if pressed_keys[pygame.K_RIGHT]:
            self.position["x"] += 4
        if pressed_keys[pygame.K_LEFT]:
            self.position["x"] -= 4

    def draw(self, screen):
        self.position["y"] += self.velocity_y
        if self.position["y"] < GROUND_LEVEL:
            self.velocity_y += 1
        elif self.velocity_y != 0:
            self.position["y"] = GROUND_LEVEL
            self.velocity_y = 0
            self.jumping = False
            self.current_animation = "run"
            self.current_frame = 0
            self.frame_counter = 0
            
        position_tuple = (self.position["x"], self.position["y"])
        
        image = self.images[self.current_animation][self.current_frame]
        
        screen.blit(image, position_tuple)
        self.frame_counter += 1
        if self.frame_counter > 7:
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

    def draw(self):
        self.background.draw(self.screen)
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
