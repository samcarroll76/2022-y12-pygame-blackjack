import pygame
import random
import os
import sys



class Game():

    def __init__(self):
        self.setup_pygame()
    
    def setup_pygame(self):
        pygame.init()
        Utils.setup_utils()
        self.infoObject = pygame.display.Info()
        self.window_size = (self.infoObject.current_w // (3/2),
                            self.infoObject.current_h // (3/2))
        
        WIDTH = self.window_size[0]
        HEIGHT = self.window_size[1]

        Utils.load_fonts()

        self.window = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE, 32)
        pygame.display.set_caption('CyberCasino 2077')

        self.clock = pygame.time.Clock()

        self.running = True
        self.should_restart = False
        self.gamestate = 0
        
    def start(self):
        
        self.menu = Menu()
        self.blackjack = Blackjack()
    
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
        if self.gamestate == 0:
            self.menu.draw()
        elif self.gamestate == 1:
            self.blackjack.draw()


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
        
    def change_state(self, dest):
        if dest == 'menu':
            self.gamestate = 0
        if dest == 'blackjack':
            self.gamestate = 1
        
        
class Menu():
    def __init__(self):
        pass
    
    def draw(self):
        game.window.blit(Utils.BG_IMAGE_SCALED, (0,0))
        open_blackjack = Button("BRUH", 300, 300, 50, 50, Utils.CLR_BLUE, Utils.CLR_RED, game.change_state, 'blackjack')
        open_blackjack.draw()
        pass
    
class Blackjack():
    def __init__(self):
        pass
    
    def draw(self):
        game.window.fill(Utils.CLR_BLUE)
        open_menu = Button("Back", 50, 50, 100, 50, Utils.CLR_GREY, Utils.CLR_RED, game.change_state, 'menu')
        open_menu.draw()
        
        
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
    def __init__(self, msg, posx, posy, width, height, standby_colour, hover_colour, action=None, dest=None):
        self.msg = msg
        self.pos_x = posx
        self.pos_y = posy
        self.width = width
        self.height = height
        self.standby_colour = standby_colour
        self.hover_colour = hover_colour
        self.action = action
        self.dest = dest
        
    
    def text_objects(self, text, font):
        textSurface = font.render(text, True, Utils.CLR_WHITE)
        return textSurface, textSurface.get_rect()

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.pos_x + self.width > mouse[0] > self.pos_x and self.pos_y + self.height > mouse[1] > self.pos_y:
            pygame.draw.rect(game.window, self.hover_colour,(self.pos_x, self.pos_y, self.width, self.height))

            if click[0] == 1 and self.action != None:
                self.action(self.dest)     
        else:
            pygame.draw.rect(game.window, self.standby_colour, (self.pos_x, self.pos_y, self.width, self.height))

        textSurf, textRect = self.text_objects(self.msg, Utils.WINDOW_SCALED_FONT)
        textRect.center = ( (self.pos_x + (self.width/2)), (self.pos_y+(self.height/2)) )
        game.window.blit(textSurf, textRect)   
        
# A static class of utilities that are used all through to code in various applications
class Utils():
    
    WIDTH, HEIGHT = 0, 0
    
    def setup_utils():
        global WIDTH, HEIGHT
        infoObject = pygame.display.Info()
        WIDTH = infoObject.current_w // (3/2)
        HEIGHT = infoObject.current_h // (3/2)
        
    
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')

    WINDOW_SCALED_FONT = None
    
    BG_IMAGE = pygame.image.load(os.path.join(ASSET_FOLDER, 'cybercity.png'))
    BG_IMAGE_SCALED = pygame.transform.scale(BG_IMAGE, (960, 600))
    
    FPS = 60
    
    # Image loader - in progress
    def image_loader(path): 
        pygame.transform.scale(
            pygame.image.load(
                os.path.join(
                    Utils.ASSET_FOLDER, path
                )
            ), (Utils.WIDTH, Utils.HEIGHT)
        )
        

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
    CLR_GREY = (122, 122, 122)
    CLR_DARK_GREY = (61, 61, 61, 200)
    CLR_LIGHT_BLUE = (100, 100, 255)
    CLR_ORANGE = (255, 165, 0)
    
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