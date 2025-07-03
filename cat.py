import pygame
from pygame import Rect, Vector2, Surface
from gameEntity import Obstacle, Block
from animation import Animation


class Cat:
    def __init__(self, position: Vector2) -> None:
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
        self.rect = Rect(position[0], position[1], 100, 100)
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
    
    def update(self, scroll_speed: float, obstacles: list[Obstacle], blocks: list[Block]):
        if scroll_speed < -2.0:
            self.set_animation("run")

        dx = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            dx += 6
        if pressed_keys[pygame.K_LEFT]:
            dx -= 6
            
        if not self.jumping and not self.in_air:
            if pressed_keys[pygame.K_SPACE]:
                self.jumping = True
                self.velocity_y = -30
                self.set_animation("highjump")
            if pressed_keys[pygame.K_UP]:
                self.jumping = True
                self.velocity_y = -22
                self.set_animation("jump")

        dx += scroll_speed

        dy = self.velocity_y
        
        self.velocity_y += 1
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.die()

        new_rect = Rect(self.position.x + dx, self.position.y, self.rect.width, self.rect.height)
        for block in blocks:
            if new_rect.colliderect(block.rect):
                if new_rect.centerx < block.rect.centerx:
                    dx = block.rect.left - self.rect.right
                else:
                    dx = block.rect.right - self.rect.left

        self.in_air = True
        new_rect = Rect(self.position.x, self.position.y + dy, self.rect.width, self.rect.height)
        for block in blocks:
            if new_rect.colliderect(block.rect):
                if new_rect.centery < block.rect.centery:
                    # we are above the block
                    dy = block.rect.top - self.rect.bottom
                    self.velocity_y = 0
                    self.in_air = False
                    self.jumping = False
                    self.set_animation("run")

                else:
                    # we are below the block
                    dy = block.rect.bottom - self.rect.top
                    self.velocity_y = 0

        self.position.x += dx
        self.position.y += dy
        self.rect.left = int(self.position.x)
        self.rect.top = int(self.position.y)

    def die(self):
        self.sounds["oof"].play()
        self.set_animation("dead")
        self.alive = False

    def draw(self, screen: Surface, scroll_offset: float):
        if not self.alive:
            self.rect.top -= 2

        draw_rect = self.rect.move(-scroll_offset, 0)
        
        if self.alive and draw_rect.centerx < 50:
            self.die()

        self.current_animation.draw(screen, draw_rect, self.alive)
        # pygame.draw.rect(screen, "white", self.rect, 1)
