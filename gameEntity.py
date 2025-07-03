from pygame import Surface, Vector2, Rect
from animation import Animation


class GameEntity:
    def __init__(self, position: Vector2, animation: Animation):
        self.animation = animation
        self.rect = Rect(position, (100, 100))
        self.position = position
        self.deleted = False

    def draw(self, screen: Surface, scroll_offset: float):
        draw_rect = self.rect.move(-scroll_offset, 0)
        if draw_rect.right >= 0:
            self.animation.draw(screen, draw_rect)
        else:
            self.deleted = True


class Block(GameEntity):
    def __init__(self, position: Vector2):
        animation = Animation("ground", 1, 100)
        super().__init__(position, animation)


class Obstacle(GameEntity):
    def __init__(self, position: Vector2):
        animation = Animation("fireball", 4, 7, "")
        super().__init__(position, animation)
