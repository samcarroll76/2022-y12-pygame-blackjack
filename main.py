import pygame
import random
import os
import sys



class Game():

    def __init__(self):
        self.setup_pygame()
    
    def setup_pygame(self):
        pygame.init()
        self.infoObject = pygame.display.Info()
        self.window_size = (self.infoObject.current_w // (3/2),
                            self.infoObject.current_h // (3/2))

        Utils.load_fonts()

        self.window = pygame.display.set_mode(
            (self.window_size[0], self.window_size[1]), pygame.SCALED | pygame.RESIZABLE, 32)
        pygame.display.set_caption('CyberCasino 2077')

        self.clock = pygame.time.Clock()

        self.running = True
        self.should_restart = False
        
    def start(self):
    
        self.main_loop()
    
    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode(
                    event.size, pygame.SCALED | pygame.RESIZABLE, 32)
                self.window_size = event.size
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                pass
    
    def draw(self):
        
        self.window.blit(Utils.BG_IMAGE_SCALED, (0,0))
        pass


    def main_loop(self):

        self.render_surface = pygame.Surface((900,900), pygame.SRCALPHA, 32).convert_alpha()

        while self.running:

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(Utils.FPS)

        if (self.should_restart):
            self.should_restart = False
            self.running = True
            self.start()

    # Determines if the game should restart based on its current state
    def restart(self):
        self.running = False
        self.should_restart = True
        
class Menu():
    def __init__(self):
        pass   

class Table():
    def __init__(self):
        pass 
    
class Player():
    def __init__(self):
        pass
    
class Hand():
    def __init__(self):
        pass
        
class Card():
    def __init__(self):
        pass   
    
class Button():
    def __init__(self, posx, posy):
        self.pos = (posx, posy)    
        
# A static class of utilities that are used all through to code in various applications
class Utils():
    
    # infoObject = pygame.display.Info()
    # WIDTH = infoObject.current_w // (3/2)
    # HEIGHT = infoObject.current_h // (3/2)
    
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')

    WINDOW_SCALED_FONT = None
    
    BG_IMAGE = pygame.image.load(os.path.join(ASSET_FOLDER, 'cybercity.png'))
    BG_IMAGE_SCALED = pygame.transform.scale(BG_IMAGE, (960, 600))
    
    FPS = 60

    # font loader
    def load_fonts():
        Utils.WINDOW_SCALED_FONT = pygame.font.Font(
            pygame.font.get_default_font(), 20)

    # colour constants
    CLR_RED = (255, 0, 0)
    CLR_BLUE = (0, 0, 255)
    CLR_GREEN = (0, 255, 0)
    CLR_BLACK = (0, 0, 0)
    CLR_WHITE = (255,255,255)

    # a limit function to limit the values of an expresion
    def limit(n, min_n, max_n):
        return max(min(max_n, n), min_n)

    # a function to return a random integer beteen 0 and 255, used for the unique colour constant generator
    def get_randint_255():
        return random.randint(0, 255)

    # unique colour constant generator
    def get_hexcolor(input):
        random.seed(input)
        return pygame.Color(Utils.get_randint_255(), Utils.get_randint_255(), Utils.get_randint_255())


# game object declaration and initialisation
game = Game()
game.start()