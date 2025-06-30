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
        self.ground_level = position.y
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.jumping:
                self.jumping = True
                self.velocity_y = -25
                self.set_animation("jump")
                
    def set_animation(self, name):
        self.current_animation = self.animations[name]
        self.current_animation.reset()
    
    def handle_pressed_keys(self, pressed_keys):
        if pressed_keys[pygame.K_RIGHT]:
            self.position.x += 4
        if pressed_keys[pygame.K_LEFT]:
            self.position.x -= 4
            
    def update(self, _scroll_speed):
        self.position.y += self.velocity_y
        if self.position.y < self.ground_level:
            self.velocity_y += 1
        elif self.velocity_y != 0:
            self.position.y = self.ground_level
            self.velocity_y = 0
            self.jumping = False
            self.set_animation("run")

    def draw(self, screen):
        self.current_animation.draw(screen, self.position)


class Animation:
    def __init__(self, name, frame_count, delay) -> None:
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
        
    def draw(self, screen, position):
        
        image = self.images[self.current_frame]
        
        screen.blit(image, position)

        self.frame_counter += 1
        if self.frame_counter > self.delay:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_counter = 0
