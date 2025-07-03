import pygame
import os


class Animation:
    def __init__(self, name: str, frame_count: int, delay: int, path: str = "cat") -> None:
        self.name = name
        self.current_frame = 0
        self.frame_counter = 0
        self.delay = delay

        images = []
        for i in range(1, frame_count + 1):
            image_path = os.path.join("images", path, name, f"{i}.png")
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (100, 100))
            images.append(image)
        self.images = images
        
    def reset(self):
        self.current_frame = 0
        self.frame_counter = 0
        
    def draw(self, screen: pygame.Surface, rect: pygame.Rect, animate: bool = True):
        
        image = self.images[self.current_frame]
        
        screen.blit(image, rect)

        if animate:
            self.frame_counter += 1
            if self.frame_counter > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.frame_counter = 0
