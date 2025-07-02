import pygame


class Cat:
    def __init__(self, position: pygame.Vector2) -> None:
        self.animations = {
            "walk": Animation("walk", 8, 7),
            "run": Animation("run", 5, 7),
            "jump": Animation("jump", 5, 12)
        }
        self.current_animation = self.animations["walk"]
        self.velocity_y = 0
        self.jumping = False
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.ground_level = self.rect.top
        
    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.velocity_y = -25
                self.set_animation("jump")
                
    def set_animation(self, name: str):
        if self.current_animation.name == name:
            return

        self.current_animation = self.animations[name]
        self.current_animation.reset()
    
    def handle_pressed_keys(self, pressed_keys: pygame.key.ScancodeWrapper):
        if pressed_keys[pygame.K_RIGHT]:
            self.position.x += 4
        if pressed_keys[pygame.K_LEFT]:
            self.position.x -= 4
            
    def update(self, scroll_speed: float):
        if scroll_speed < -2.0:
            self.set_animation("run")

        self.position.y += self.velocity_y
        if self.position.y < self.ground_level:
            self.velocity_y += 1
        elif self.velocity_y != 0:
            self.position.y = self.ground_level
            self.velocity_y = 0
            self.jumping = False
            self.set_animation("run")
        
        self.rect.left = int(self.position.x)
        self.rect.top = int(self.position.y)

    def draw(self, screen: pygame.Surface):
        self.current_animation.draw(screen, self.rect)
        pygame.draw.rect(screen, "white", self.rect, 1)


class Animation:
    def __init__(self, name: str, frame_count: int, delay: int) -> None:
        self.name = name
        self.current_frame = 0
        self.frame_counter = 0
        self.delay = delay

        images = []
        for i in range(1, frame_count + 1):
            image = pygame.image.load(f"images/cat/{name}/{i}.png")
            image = pygame.transform.scale(image, (100, 100))
            images.append(image)
        self.images = images
        
    def reset(self):
        self.current_frame = 0
        self.frame_counter = 0
        
    def draw(self, screen: pygame.Surface, rect: pygame.Rect):
        
        image = self.images[self.current_frame]
        
        screen.blit(image, rect)

        self.frame_counter += 1
        if self.frame_counter > self.delay:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_counter = 0
