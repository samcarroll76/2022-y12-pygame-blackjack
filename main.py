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
        pygame.mixer.init()
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
        self.blackjack = Blackjack(17, 16)
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
                # self.draw()
                if event.key == pygame.K_r:
                    self.restart()
                if event.key == pygame.K_a:
                    self.rick_roll()
                if self.gamestate == 0:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up = True
                pass
        
        if self.gamestate == 1:
            self.progress_turns()                        

    
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
            
            self.mouse_up = False

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
            self.blackjack.initial_draw = True
        if dest == 'blackjack':
            self.gamestate = 1
            load_text = Text("Shuffling Decks...", (Utils.WIDTH/2, Utils.HEIGHT/2), Utils.CLR_BLACK)
            load_text.draw()
            self.restart()
            # pygame.time.wait(1000)
    
    def rick_roll(self):
        pygame.mixer.music.load(os.path.join(Utils.SOUNDS_FOLDER, 'rick.mp3'))
        pygame.mixer.music.play(1)

    def progress_turns(self):
        print("in progress_turns")
        p = self.blackjack.current_player
        if p.is_human():
            # listen for keys to advance game
            # buttons do this themselves
            pass
        else:
            pygame.time.wait(1000)
            # call decide move
            p.decide_move()
            pass
              
        self.blackjack.check_finish()
                
        # if event.key == pygame.K_h and not isinstance(self.blackjack.current_player, Bot):
        #     self.blackjack.current_player.hit()
        # # if <hitKeyPressed> and not isinstance(currentPlayer, Computer);
        # #     currentPlayer.hit()
        # if event.key == pygame.K_c:
        #     for player in self.blackjack.players:
        #         if isinstance(player, Bot):
        #             player.decide_move()

            
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
        self.button_open_blackjack = Button("Blackjack", Utils.WIDTH/2, Utils.HEIGHT/(12/4), self.menu_button_size[0], 
                                            self.menu_button_size[1], Utils.CLR_BLUE, Utils.CLR_RED, game.change_state, 'blackjack')
        
    
    def draw(self):
        game.window.blit(Utils.images["backgrounds"]["menu"], (0,0))
        self.button_open_blackjack.draw()
    
    
class Blackjack():
    def __init__(self, dealer_threshold, bot_threshold):
        self.player_count = 4
        self.suits = ['H','D','S','C']
        self.faces = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        self.deck_count = 3
        self.shuffle_factor = 5
        self.dealer_threshold = dealer_threshold
        self.bot_threshold = bot_threshold
        self.shoe = []
        self.players = []
        
        self.make_shoe()
        self.make_players()
        
        self.interaction_buttons = [Button("Hit", Utils.WIDTH/(32/17), Utils.HEIGHT/(18/11), Utils.INTERACTION_BUTTON_SIZE[0], 
                                      Utils.INTERACTION_BUTTON_SIZE[1], Utils.CLR_GREEN, Utils.CLR_GREY, self.players[1].hit, None), 
                                    Button("Stand", Utils.WIDTH/(32/15), Utils.HEIGHT/(18/11), Utils.INTERACTION_BUTTON_SIZE[0], 
                                      Utils.INTERACTION_BUTTON_SIZE[1], Utils.CLR_RED, Utils.CLR_GREY, self.players[1].stand, None), 
                                    # Button("Double", Utils.WIDTH/(32/19), Utils.HEIGHT/(18/11), Utils.INTERACTION_BUTTON_SIZE[0], 
                                    #   Utils.INTERACTION_BUTTON_SIZE[1], Utils.CLR_GREEN, Utils.CLR_GREY, self.players[1].hit, None), 
                                    # Button("Split", Utils.WIDTH/(32/13), Utils.HEIGHT/(18/11), Utils.INTERACTION_BUTTON_SIZE[0], 
                                    #   Utils.INTERACTION_BUTTON_SIZE[1], Utils.CLR_RED, Utils.CLR_GREY, None, None)
        ]
        self.initial_draw = True
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        
        
    def make_players(self):
        player_id = 0
        player_pos = 0
        for _ in range(self.player_count):
            player_id += 1
            player_pos += 1
            if player_id == 2:
                self.players.append(Player(player_id, player_pos, [self.get_card(),self.get_card()]))
            elif player_id == 4:
                self.players.append(Dealer(player_id, player_pos, [self.get_card(),self.get_card()], self.dealer_threshold))
            else:
                self.players.append(Bot(player_id, player_pos, [self.get_card(),self.get_card()], self.bot_threshold))
        
    def make_shoe(self):
        for _ in range(self.deck_count):
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
    
    def check_finish(self):
        if self.current_player.finished:
            if self.current_player_index >= 3:
                self.check_winners()
                pass
            else:   
                self.current_player_index += 1
                self.current_player = self.players[self.current_player_index]
    
    def check_winners(self):
        deal_val = self.players[3].hands[0].calculate_value()
        
        for player in self.players:
            if player.player_id < 4:
                print(player.player_id)
                val = player.hands[0].calculate_value()
                if val > 21:
                    player.show_outcome("lose")
                elif len(player.hands[0].cards) >= 5:
                    player.show_outcome("win")
                elif deal_val > 21:
                    player.show_outcome("win")
                elif val > deal_val:
                    player.show_outcome("win")
                elif val < deal_val:
                    player.show_outcome("lose")
                elif val == deal_val:
                    player.show_outcome("tie")
        pygame.time.wait(300)
        redeal_text = Text("Re-dealing Cards...", (Utils.WIDTH/2, Utils.HEIGHT/2), Utils.CLR_BLACK)
        redeal_text.draw()
        game.restart()
          
                
        
    def draw(self):
        if self.initial_draw:
            game.window.blit(Utils.images["backgrounds"]["game"], (0,0))
            for player in self.players:
                player.draw()
            self.initial_draw = False
        for button in self.interaction_buttons:
            button.draw()
            

# class Table():
#     def __init__(self):
        
#         pass

class Player():
    def __init__(self, player_id, player_pos, start_cards):
        self.player_id = player_id
        self.player_pos = player_pos
        self.start_cards = start_cards
        self.hands = []
        self.finished = False
        self.stand_threshold = 17
        self._is_human = True
        
        self.add_hand()
        
    
    def add_hand(self):
        self.hands.append(Hand(f"{self.player_pos}", self.start_cards))
        self.draw()
        
    def hit(self):
        if self.hands[0].calculate_value() < 21:
            self.hands[0].add_card()
            self.draw()
            self.check_bust()
        else:
            self.finished = True
            
    def decide_move(self):
        assert not self.is_human()  # throw a fit if we call this on a player     
        if self.hands[0].calculate_value() < self.stand_threshold and len(self.hands[0].cards) < 5:
            self.hit() 
        else:
            self.stand()
        
    def stand(self):
        self.finished = True
        self.draw()
    
    # just for shits and giggles
    def check_bust(self):
        if self.hands[0].calculate_value() > 21:
            # self.finished = True
            game.rick_roll()
    
    def show_outcome(self, outcome):
        
        if self.player_id == 2:
            out_text = Text(f"You {outcome}!!", 
                            (Utils.table_positions[str(self.player_id)][0], 
                            Utils.table_positions[str(self.player_id)][1] - Utils.HEIGHT/(18/2)),
                            Utils.CLR_BLACK)
        else:
            out_text = Text(f"Player {self.player_id} {outcome}s!!",
                            (Utils.table_positions[str(self.player_id)][0], 
                            Utils.table_positions[str(self.player_id)][1] - Utils.HEIGHT/(18/2)),
                            Utils.CLR_BLACK)
        
        out_text.draw()
        
    def draw(self):
        for hand in self.hands:
            hand.draw(self.finished)
            
    def is_human(self):
        return self._is_human
    
class Bot(Player):
    def __init__(self, player_id, player_pos, start_cards, stand_threshold):
        super().__init__(player_id, player_pos, start_cards)
        self.stand_threshold = stand_threshold
        self._is_human = False
        
class Dealer(Player):
    def __init__(self, player_id, player_pos, start_cards, stand_threshold):
        super().__init__(player_id, player_pos, start_cards)
        self.stand_threshold = stand_threshold
        self._is_human = False
                
class Hand():
    def __init__(self, pos, start_cards):
        self.start_cards = start_cards
        self.pos = pos
        self.table_coords = Utils.table_positions[self.pos]
        self.cards = []
        
        self.add_start_cards()
        # self.hand_table_pos = (self.table_pos[0] + (card_number-1)*(Utils.WIDTH/24), self.table_pos[1])
    
    def add_start_cards(self):
        for card in self.start_cards:
            self.cards.append(card)
        # print(self.cards)
        
    def add_card(self):
        self.cards.append(game.blackjack.get_card())
        
    def calculate_value(self):
        value = 0 
        ace_count = 0
        
        for card in self.cards:
            cinfo = card.info()
            if cinfo[0] in Utils.ten_cards:
                value += 10
            elif cinfo[0] == "A":
                value += 11
                ace_count += 1
            else:
                value += int(cinfo[0])
        
        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1
                
        return value

    def show_value(self, active):
        colour = Utils.CLR_GREEN if active else Utils.CLR_BLACK
        val = Button(f"{self.calculate_value()}", 
                     Utils.table_positions[self.pos][0] + 2*Utils.CARD_SPACING, Utils.table_positions[self.pos][1] - Utils.VALUE_BUTTON_SIZE[1] - Utils.VALUE_OFFSET, 
                     Utils.VALUE_BUTTON_SIZE[0], Utils.VALUE_BUTTON_SIZE[1], 
                     colour, colour, None, None)
        # val = Text(f"Value: {self.calculate_value()}", (Utils.table_positions[self.pos][0], Utils.table_positions[self.pos][1] - Utils.VALUE_OFFSET), Utils.CLR_WHITE)
        val.draw()
        
        
    def draw(self, active):
        card_count = 0
        for card in self.cards:
            card_count += 1
            card.draw(self.table_coords, card_count)
        self.show_value(active)
        
        
        
        
   
class Card():
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
        self.card_id = f"{self.face}-{self.suit}"
        
    def draw(self, position, card_count):
        offset = (card_count-1)*(Utils.CARD_SPACING)
        game.window.blit(
            Utils.load_image(f"{self.card_id}.png", Utils.CARD_FOLDER, Utils.CWIDTH, Utils.CHEIGHT),
            (position[0] + offset, position[1])
            )
        pass
    
    def info(self):
        return (self.face, self.suit, self.card_id)
        
    def __repr__(self):
        return f"{self.face}, {self.suit}, {self.card_id}"
    

class Text():
    def __init__(self, msg, pos, colour):
        self.msg = msg
        self.size = Utils.WINDOW_SCALED_FONT.size(self.msg)
        
        self.pos = (pos[0] - self.size[0]//2, pos[1] - self.size[1]//2)
        self.colour = colour
        
        self.make_text()
        
    def make_text(self):
        self.text_object = Utils.WINDOW_SCALED_FONT.render(self.msg, False, self.colour)
        
    def draw(self):
        game.window.blit(self.text_object, self.pos)
    

    
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
    
    def get_text_width(self):
        text_dimensions = Utils.WINDOW_SCALED_FONT.size(f"{self.msg}")
        return text_dimensions
    
    def text_objects(self, text, font):
        textSurface = font.render(text, True, Utils.CLR_WHITE)
        return textSurface, textSurface.get_rect()

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.pos_x + self.width//2 > mouse[0] > self.pos_x - self.width//2 and self.pos_y + self.height//2 > mouse[1] > self.pos_y - self.height//2:
            pygame.draw.rect(game.window, self.hover_colour,(self.pos_x - self.width//2, self.pos_y - self.height//2, self.width, self.height))

            if game.mouse_up and self.action != None:   
                if self.dest != None:
                    self.action(self.dest)
                else:
                    self.action()
        else:
            pygame.draw.rect(game.window, self.standby_colour, (self.pos_x - self.width//2, self.pos_y - self.height//2, self.width, self.height))

        textSurf, textRect = self.text_objects(self.msg, Utils.WINDOW_SCALED_FONT)
        textRect.center = ( (self.pos_x), (self.pos_y) )
        game.window.blit(textSurf, textRect)   
        
# A static class of utilities that are used all through to code in various applications
class Utils():
    
    # Need to figure out how to use the info-object parameters in here for width and height instead of hardcoding
    WIDTH, HEIGHT = 1200, 750
    CWIDTH, CHEIGHT = WIDTH/(18/2), HEIGHT/(9/2)
    
    VALUE_OFFSET = HEIGHT/75
    
    CARD_SPACING = WIDTH/32
        
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    CARD_FOLDER = os.path.join(ASSET_FOLDER, 'cards/')
    BG_FOLDER = os.path.join(ASSET_FOLDER, 'backgrounds/')
    SOUNDS_FOLDER = os.path.join(ASSET_FOLDER, 'sounds/')


    fonts = [["default", 20],
             ["default", 40],
        ]
    
    WINDOW_SCALED_FONT = None
    
    INTERACTION_BUTTON_SIZE = (WIDTH/18, HEIGHT/18)
    
    VALUE_BUTTON_SIZE = (WIDTH/24, HEIGHT/24)
    
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
    
    ten_cards = ["T", "J", "Q", "K"]
    
    
    images = {
        "backgrounds": {
            "menu": load_image('cybercity.png', BG_FOLDER, WIDTH, HEIGHT),
            "game": load_image('rick.png', BG_FOLDER, WIDTH, HEIGHT)
        }
    }
    
    
    table_positions = {
            "1": (WIDTH/(64/5), HEIGHT-(HEIGHT/(18/5))),
            "2": (WIDTH/(64/25), HEIGHT-(HEIGHT/(18/5))),
            "3": (WIDTH/(64/45), HEIGHT-(HEIGHT/(18/5))),
            "4": (WIDTH/(64/25), (HEIGHT/(18/2)))
        }
    

        

    # # font loader
    def load_fonts():
        Utils.WINDOW_SCALED_FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
        

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
