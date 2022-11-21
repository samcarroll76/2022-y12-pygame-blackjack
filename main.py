import pygame
import random
import os
import sys
import time



class Game():

    def __init__(self):
        self.setup_pygame()
    
    def setup_pygame(self):
        pygame.init()
        self.infoObject = pygame.display.Info()
        self.window_size = (self.infoObject.current_w // (12/10),
                            self.infoObject.current_h // (12/10))
        
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
        self.global_button_size = (Utils.WIDTH/24, Utils.HEIGHT/15)
        self.global_buttons = [Button("Quit", Utils.WIDTH/48, Utils.HEIGHT/30, self.global_button_size[0], 
                                      self.global_button_size[1], Utils.CLR_DARK_GREY, Utils.CLR_RED, quit, 'quit'), 
                               Button("Back", Utils.WIDTH/48 + self.global_button_size[0], Utils.HEIGHT/30, self.global_button_size[0], 
                                      self.global_button_size[1], Utils.CLR_GREY, Utils.CLR_RED, game.change_state, 'menu')]
    
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
        for button in self.global_buttons:
            button.draw()


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
            
    # def t(self, msg): # TIMING FUNCTION
    #     global last
    #     new = time.time()
    #     print("Last:", "{:.3f}".format(new - last), ", Start:", "{:.3f}".format(new - START), " - ", msg)
    #     last = new
    
    # def quit(self):
    #     pygame.quit()
        
        
class Menu():
    def __init__(self):
        self.menu_button_size = (Utils.WIDTH/6, Utils.HEIGHT/12)
        self.button_offset = (self.menu_button_size[0]//2)
        self.button_open_blackjack = Button("Blackjack", Utils.WIDTH/2-self.button_offset, Utils.HEIGHT/(12/4), self.menu_button_size[0], 
                                            self.menu_button_size[1], Utils.CLR_BLUE, Utils.CLR_RED, game.change_state, 'blackjack')
        
    
    def draw(self):
        game.window.blit(Utils.images["backgrounds"]["menu"], (0,0))
        self.button_open_blackjack.draw()
    
    
class Blackjack():
    def __init__(self):
        self.player_num = 3
        self.suits = ['H','D','S','C']
        self.faces = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.deck_num = 3
        self.shuffle_factor = 5
        self.shoe = []
        self.make_shoe()
        self.hands = []
        self.make_hands()
    
    def make_hands(self):
        player_pos = 0
        for _ in range(self.player_num):
            player_pos += 1
            self.hands.append(Hand(f"{player_pos}", [self.get_card(),self.get_card()]))
        pass
        
    def make_shoe(self):
        for _ in range(self.deck_num):
            for suit in self.suits:
                for face in self.faces:
                    self.shoe.append(Card(face, suit))
        self.shuffle_shoe()
    
    def shuffle_shoe(self):
        for _ in range(self.shuffle_factor * 100000):
            
            index_1 = random.randint(0,len(self.shoe)-1)
            index_2 = random.randint(0,len(self.shoe)-1)
            
            tmp_card = self.shoe[index_1]
            self.shoe[index_1] = self.shoe[index_2]
            self.shoe[index_2] = tmp_card
    
    def get_card(self):
        return self.shoe.pop(0)
        
    def draw(self):
        game.window.blit(Utils.images["backgrounds"]["game"], (0,0))
        for hand in self.hands:
            hand.draw()
            
    
        
        
class Table():
    def __init__(self):
        
        pass

class Player():
    def __init__(self, table_pos):
        pass
    
class Dealer(Player):
    def __init__(self, table_pos):
        super().__init__(table_pos)
        pass
    
   
class Card():
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
        self.card_id = f"{self.face}-{self.suit}"
        
        
    def draw(self, position, card_num):
        offset = (card_num-1)*(Utils.WIDTH/32)
        game.window.blit(Utils.images["cards"][self.card_id], (position[0] + offset, position[1]))
        pass
    
class Hand():
    def __init__(self, pos, start_cards):
        self.table_positions = {
            "1": (Utils.WIDTH/(64/5), Utils.HEIGHT-(Utils.HEIGHT/(18/7))),
            "2": (Utils.WIDTH/(64/25), Utils.HEIGHT-(Utils.HEIGHT/(18/7))),
            "3": (Utils.WIDTH/(64/45), Utils.HEIGHT-(Utils.HEIGHT/(18/7)))
        }
        self.start_cards = start_cards
        self.table_pos = self.table_positions[pos]
        # self.hand_table_pos = (self.table_pos[0] + (card_number-1)*(Utils.WIDTH/24), self.table_pos[1])
        
    def draw(self):
        card_num = 0
        for card in self.start_cards:
            card_num += 1
            card.draw(self.table_pos, card_num)
        
        
    
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
                if self.dest == quit and game.gamestate == 0:
                    self.action()    
                elif self.dest != None:
                    self.action(self.dest)
        else:
            pygame.draw.rect(game.window, self.standby_colour, (self.pos_x, self.pos_y, self.width, self.height))

        textSurf, textRect = self.text_objects(self.msg, Utils.WINDOW_SCALED_FONT)
        textRect.center = ( (self.pos_x + (self.width/2)), (self.pos_y+(self.height/2)) )
        game.window.blit(textSurf, textRect)   
        
# A static class of utilities that are used all through to code in various applications
class Utils():
    
    # Need to figure out how to use the info-object parameters in here for width and height instead of hardcoding
    WIDTH, HEIGHT = 1200, 750
    CWIDTH, CHEIGHT = WIDTH/(12/2), HEIGHT/3
        
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    CARD_FOLDER = os.path.join(ASSET_FOLDER, 'cards/')

    WINDOW_SCALED_FONT = None
    
    FPS = 60
    
    # Image loader - in progress
   
    def load_image(path, fpath, width, height): 
        return pygame.transform.scale(
            pygame.image.load(
                os.path.join(
                    fpath, path
                )
            ), (width, height)
        )
        
    def load_card_image():
        pass
    
    
    images = {
        "backgrounds": {
            "menu": load_image('cybercity.png', ASSET_FOLDER, WIDTH, HEIGHT),
            "game": load_image('rick.png', ASSET_FOLDER, WIDTH, HEIGHT)
        },
        # I know this sucks - will be improving it later
        "cards": {
            "A-H": load_image('a_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "A-D": load_image('a_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "A-S": load_image('a_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "A-C": load_image('a_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "K-H": load_image('k_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "K-D": load_image('k_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "K-S": load_image('k_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "K-C": load_image('k_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "Q-H": load_image('q_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "Q-D": load_image('q_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "Q-S": load_image('q_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "Q-C": load_image('q_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "J-H": load_image('j_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "J-D": load_image('j_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "J-S": load_image('j_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "J-C": load_image('j_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "T-H": load_image('t_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "T-D": load_image('t_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "T-S": load_image('t_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "T-C": load_image('t_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "9-H": load_image('9_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "9-D": load_image('9_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "9-S": load_image('9_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "9-C": load_image('9_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "8-H": load_image('8_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "8-D": load_image('8_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "8-S": load_image('8_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "8-C": load_image('8_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "7-H": load_image('7_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "7-D": load_image('7_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "7-S": load_image('7_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "7-C": load_image('7_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "6-H": load_image('6_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "6-D": load_image('6_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "6-S": load_image('6_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "6-C": load_image('6_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "5-H": load_image('5_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "5-D": load_image('5_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "5-S": load_image('5_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "5-C": load_image('5_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "4-H": load_image('4_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "4-D": load_image('4_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "4-S": load_image('4_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "4-C": load_image('4_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "3-H": load_image('3_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "3-D": load_image('3_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "3-S": load_image('3_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "3-C": load_image('3_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "2-H": load_image('2_of_hearts.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "2-D": load_image('2_of_diamonds.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "2-S": load_image('2_of_spades.png', CARD_FOLDER, CWIDTH, CHEIGHT),
            "2-C": load_image('2_of_clubs.png', CARD_FOLDER, CWIDTH, CHEIGHT),
        }
        
    }
    
    
    
        

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