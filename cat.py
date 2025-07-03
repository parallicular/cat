import pygame
from gameEntity import Obstacle
from animation import Animation


class Cat:
    def __init__(self, position: pygame.Vector2) -> None:
        self.animations = {
            "walk": Animation("walk", 8, 7),
            "run": Animation("run", 5, 7),
            "highjump": Animation("jump", 5, 15),
            "jump": Animation("jump", 5, 10),
            "dead": Animation("dead", 1, 10)
        }
        self.current_animation = self.animations["walk"]
        self.velocity_y = 0
        self.jumping = False
        self.in_air = False
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.ground_level = self.rect.top
        self.alive = True
        self.sounds = {
            "oof": pygame.mixer.Sound("sounds/oof.mp3")
        }
        self.sounds["oof"].set_volume(0.5)
                
    def set_animation(self, name: str):
        if self.current_animation.name == name:
            return

        self.current_animation = self.animations[name]
        self.current_animation.reset()
    
    def update(self, scroll_speed: float, obstacles: list[Obstacle]):
        if scroll_speed < -2.0:
            self.set_animation("run")

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            self.position.x += 6
        if pressed_keys[pygame.K_LEFT]:
            self.position.x -= 6
            
        if not self.jumping and not self.in_air:
            if pressed_keys[pygame.K_SPACE]:
                self.jumping = True
                self.velocity_y = -30
                self.set_animation("highjump")
            if pressed_keys[pygame.K_UP]:
                self.jumping = True
                self.velocity_y = -24
                self.set_animation("jump")

        self.position.x += scroll_speed

        self.position.y += self.velocity_y
        if self.position.y < self.ground_level:
            self.velocity_y += 1
        elif self.velocity_y != 0:
            self.position.y = self.ground_level
            self.velocity_y = 0
            self.jumping = False
            self.set_animation("run")
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.sounds["oof"].play()
                self.set_animation("dead")
                self.alive = False
                
        self.rect.left = int(self.position.x)
        self.rect.top = int(self.position.y)

    def draw(self, screen: pygame.Surface, scroll_offset: float):
        if not self.alive:
            self.rect.top -= 2
            
        draw_rect = self.rect.move(-scroll_offset, 0)

        self.current_animation.draw(screen, draw_rect, self.alive)
        # pygame.draw.rect(screen, "white", self.rect, 1)
