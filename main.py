import pygame
import sys
from enum import Enum
from level import Level, Goal
from player import Player

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    END = 2
    BETWEEN_LEVELS = 3

class Game:
    def __init__(self):
        self.paused = False
        self.player = Player()
        self.game_state = GameState.MENU
        self.levels = [Level([
            pygame.Rect(0, 0, 20, 480),
            pygame.Rect(0, 460, 640, 20),
            pygame.Rect(620, 0, 20, 480),
            pygame.Rect(200, 250, 80, 20),
            pygame.Rect(300, 300, 80, 20),
            pygame.Rect(400, 350, 80, 20),
            pygame.Rect(500, 400, 80, 20),
        ], [Goal(0, 200, 50, 50)]),
        Level([
            pygame.Rect(0, 0, 20, 480),
            pygame.Rect(0, 460, 640, 20),
            pygame.Rect(620, 0, 20, 480),
            pygame.Rect(300, 300, 80, 20),
        ], [Goal(150, 150, 50, 50)]),       
        ]
        self.level_index = 0

        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()  
        self.surface.fill((255,255,255))

        #create title screen
        self.title_text = pygame.freetype.SysFont('Comic Sans MS', size=48)
        self.title_rect = self.title_text.get_rect("Platformer")
        self.title_rect.center = (320, 100)

        #create start button and get bounding box
        self.start_button_text = pygame.freetype.SysFont('Comic Sans MS', italic=True, size=36)
        self.start_button_rect = self.start_button_text.get_rect("START")
        self.start_button_rect.center = (320, 240)

        #create end screen
        self.end_text = pygame.freetype.SysFont('Comic Sans MS', italic=True, size=36)
        self.end_rect = self.end_text.get_rect("START")
        self.end_rect.center = (320, 240)

        self.screen.blit(self.surface, (0,0))

        self.clock = pygame.time.Clock()

    def render(self):
        self.surface.fill((32,32,32))
        match self.game_state:
            case GameState.MENU:
                self.start_button_text.render_to(self.surface, self.start_button_rect.topleft, "START", fgcolor=(255,255,255), bgcolor=(255,0,0))
                self.title_text.render_to(self.surface, self.title_rect.topleft, "Platformer", fgcolor=(255,255,255))
            case GameState.PLAYING:
                self.levels[self.level_index].render(self.surface)
                self.player.render(self.surface)
            case GameState.END:
                self.end_text.render_to(self.surface, self.end_rect.topleft, "THE END", fgcolor=(255,255,255))
        
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()
    
    def poll(self):
        for ev in pygame.event.get():
            match ev.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break
                case pygame.KEYDOWN:
                    match ev.key:
                        case pygame.K_p:
                             self.paused = not self.paused
                       
    def update(self):
        dt = self.clock.tick(120)/1000
        if not self.paused:
            match self.game_state:
                case GameState.MENU:
                    if self.start_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        self.game_state = GameState.PLAYING
                case GameState.PLAYING:
                    self.player.update(dt, self.levels[self.level_index])
                    if self.levels[self.level_index].finished:
                        self.level_index += 1
                    if self.level_index >= len(self.levels):
                        self.game_state = GameState.END
                case GameState.END:
                    pass

if __name__ == '__main__':
    game = Game()

    while True:
        game.poll()
        game.update()
        game.render()