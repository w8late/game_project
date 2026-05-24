import pygame

class Item:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def behaviour(self, player, level):
        pass

class Goal(Item):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def behaviour(self, player, level):
        level.finished = True
'''
class LevelReader:
    def read(file):
        return Level()
'''

class Level:
    def __init__(self, platforms, items = None):
        self.platforms = platforms
        self.items = items
        self.finished = False
        self.spawn_point = pygame.Vector2(300, 10)

    def render(self, surface):
        for p in self.platforms:
            pygame.draw.rect(surface, (255,255,255), p)
        for i in self.items:
            pygame.draw.rect(surface, (0,255,0), i.rect)