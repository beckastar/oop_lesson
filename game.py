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

class DoorKey(GameElement):
    IMAGE = "Key"
    SOLID = True

    def interact(instance, character):
        print type(instance)
        # if player has special gem, can get key
        # if player does not have special gem, gets error message to get it
        specialgem = SpecialGem()
        # using same convention as has_key because cannot have else in for loop
        has_specialgem = False
        for item in character.inventory:
            if type(specialgem) == type(item):
                has_specialgem = True
                character.inventory.append(instance) # instance is adding door key
                instance.SOLID = False
                GAME_BOARD.draw_msg("You just acquired the key!")
        if not has_specialgem: 
            GAME_BOARD.draw_msg("You need the Orange Gem to get the key!")

class OpenDoor(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class ClosedDoor(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    def interact(instance, character):
        #this is triggered when you run into the door
        #player is lowercase b/c is passed in as lowercase
        #interact function is when things happen most of the time in this game
        opendoor = OpenDoor()
        #need to register opendoor on gameboard
        GAME_BOARD.register(opendoor)
        doorkey = DoorKey()
        #opendoor = getattr(opendoor, OpenDoor())
        # if doorkey is in player inventory, change closeddoor to open door when player enters square
        print doorkey
        print character.inventory
        print type(doorkey)
        has_key = False
        for item in character.inventory:
            if type(doorkey) == type(item):
                #turn closed door into open door 
                has_key =True
                GAME_BOARD.del_el(instance.x, instance.y)
                GAME_BOARD.draw_msg("The key opened the door!")
                #delete instance
                GAME_BOARD.set_el(instance.x, instance.y, opendoor)
        # else, show message below
        if not has_key:
            GAME_BOARD.draw_msg("You need the key to open this door!")

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

class TallTree(Character):
    IMAGE = "TallTree"
    SOLID = True

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    # don't need to override next_pos cause only PLAYER is moving (see below)

class Gem(GameElement):
    IMAGE = "BlueGem"
    def interact(self, player):
        player.inventory.append(self) # when player runs into gem it's added to player stash
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class SpecialGem(GameElement):
    IMAGE = "OrangeGem"
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You got the special gem! You have %d items!" % (len(player.inventory)))

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

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

    for rock in rocks:
        print rock

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # step 12
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    specialgem = SpecialGem()
    GAME_BOARD.register(specialgem)
    GAME_BOARD.set_el(4, 4, specialgem)

    closedDoor = ClosedDoor()
    GAME_BOARD.register(closedDoor)
    GAME_BOARD.set_el(0,2, closedDoor)

    doorkey = DoorKey()
    GAME_BOARD.register(doorkey)
    GAME_BOARD.set_el(0,4, doorkey)

    talltree = TallTree()
    GAME_BOARD.register(talltree)
    GAME_BOARD.set_el(0,3, talltree)

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

        if next_x >= GAME_WIDTH or next_x<0:
            GAME_BOARD.draw_msg("Das is verboten")
            return
             #existing_el = GAME_BOARD.get_el(next_x, next_y)
        if next_y >= GAME_WIDTH or next_y<0:
            GAME_BOARD.draw_msg("Das is verboten")            
            return
            #existing_el = GAME_BOARD.get_el(next_x, next_y)
        
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)




