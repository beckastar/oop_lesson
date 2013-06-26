import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

# should this be here?
rock = Rock()

class Character(GameElement):
    #IMAGE = "Girl"
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
    

    def next_pos(self, direction):
        if direction == "up": # use == if testing to see if equal
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))


pass
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    # Initialize and register rock 1
    #rock1 = Rock()
    #GAME_BOARD.register(rock1)
    #GAME_BOARD.set_el(1, 1, rock1)

    # Initialize and register rock 2
    #rock2 = Rock()
    #GAME_BOARD.register(rock2)
    #GAME_BOARD.set_el(2, 2, rock2)

    #initialize and register rock 3
    #rock3 = Rock()
    #GAME_BOARD.register(rock3)
    #GAME_BOARD.set_el(5,2, rock3)

    rock_positions = [(2,1),(1,2),(3,2),(2,3)]

    rocks = []
    #iterator
    for pos in rock_positions:
        #creates new rock 
        rock = Rock()
        #establish that rock is part of game board
        GAME_BOARD.register(rock)
        #When you register it knows to draw it on the screen
        #set el sets the position on the screen - put element on board at some 
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    # In the initialize() function
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

 

    pass

    for rock in rocks:
        print rock

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # step 12
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

def keyboard_handler():
    direction = None
    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        #Take keyboard input
        #test to see if coordinate is in the gameboard grid
        #else 
        next_location = PLAYER.next_pos(direction)
        #where we go next is the function next_pos called on player with the direction as param. 
        next_x = next_location[0]
        #next x coordinate is the first item in next_location
        next_y = next_location[1]
        #next y coordinate is the second item in next_location
        

        #testing deletion

        if next_x >= GAME_WIDTH or next_x<0:
            GAME_BOARD.draw_msg("Das is verboten")
            return
             #existing_el = GAME_BOARD.get_el(next_x, next_y)
        if next_y >= GAME_WIDTH or next_y<0:
            GAME_BOARD.draw_msg("Das is verboten")            
            return
            #existing_el = GAME_BOARD.get_el(next_x, next_y)

        #########
        
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
        #     except 
        #         if next_x >= GAME_WIDTH or next_x < 0
        #     except 
        #         if next_y >= GAME_HEIGHT or next_y < 0
        # #if next position is out of range of board
        #game board = game board




        #GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        #deleting player from old posn

        #GAME_BOARD.set_el(next_x, next_y, PLAYER)
        #resetting player to next/new position



