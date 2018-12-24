""" This module contains the subcontroller to control a single player in a
Tic Tac Toe game

Created by Jesse Phillips on December 19, 2018

"""
from game2d import *

POINTER_SIZE = 120
GAME_WIDTH = 800
GAME_HEIGHT = 600

class Player(object):
    """ This class controls a single player in a Tic Tac Toe game
    
    INSTANCE ATTRIBUTES:
    _name:      the name of the player [string]
    _id:        the id of the player [int, either 1 or 2]
    _pointer:   pointer to indicate current spot in the grid [instance of GRectangle or GEllipse]
    _done:      whether this player is done with their current turn [boolean, True if done, False otherwise]
    _inputAxes: the input axes for this player [string list, length 5]
    _gridPos:   grid position of pointer in grid. [0,0] in bottom left corner [int list of length 2]
    _lastkey:   if the movement keys were pressed in the last animation frame.
                Prevents the player from moving multiple spaces when they hold down a
                movement key. [boolean]
                
    """
    
    def getName(self):
        """ Returns the name of this player """
        
        return self._name
    
    def getDone(self):
        """ Returns whether this player is done with their current turn or not """
        
        return self._done
    
    def setDone(self, done):
        """ Changes whether the player is done with their turn
        
        Parameter done: True if the player is done with their turn, False otherwise
        Precondition: done is a boolean """
        
        assert type(done) == bool
        self._done = done
    
    
    def __init__(self, name, num):
        """ The initializer for a Player object
        
        Parameter name: the player's name
        Precondtion: name is a string
        
        Parameter num: the player's id number
        Precondition: id is an int either 1 or 2 """
        
        assert type(name) == str
        assert num in [1,2]
        self._name = name
        self._id = num
        if num == 1:
            self._pointer = GRectangle(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                        width=POINTER_SIZE, height=POINTER_SIZE,fillcolor='red')
            self._inputAxes = ['up', 'down', 'right', 'left', 'spacebar']
        else:
            self._pointer = GEllipse(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                        width=POINTER_SIZE,height=POINTER_SIZE,fillcolor='blue')
            self._inputAxes = ['w', 's', 'd', 'a', 'e']
            
        self._done = False
        self._gridPos = [1,1]
        self._lastkey = False
            
            
        
        
    def play(self, inputs, grid, objgrid):
        """ Controls one turn of Tic Tac Toe for this player
        
        Parameter inputs: the player's input
        Precondition: inputs is an instance of GInput
        
        Parameter grid: the tic tac toe grid
        Precondition: grid is a two-dimensional list of integers
        
        Parameter objgrid: the tic tac toe grid in object representation
        Precondition: grid is a two-dimensional list of GObjects or None"""
        
        if (not self._lastkey):
            # Right
            if inputs.is_key_down(self._inputAxes[2]):
                if (self._pointer.x < 5*GAME_WIDTH/6):
                    self._pointer.x += GAME_WIDTH/3
                    self._gridPos[0] += 1
                
            # Left
            if inputs.is_key_down(self._inputAxes[3]):
                if (self._pointer.x > GAME_WIDTH/6 + 3):
                    self._pointer.x -= GAME_WIDTH/3
                    self._gridPos[0] -= 1
             
            # Up   
            if inputs.is_key_down(self._inputAxes[0]):  
                if (self._pointer.y < 5*GAME_HEIGHT/6):
                    self._pointer.y += GAME_HEIGHT/3
                    self._gridPos[1] += 1
            
            # Down   
            if inputs.is_key_down(self._inputAxes[1]):
                if (self._pointer.y > GAME_HEIGHT/6):
                    self._pointer.y -= GAME_HEIGHT/3
                    self._gridPos[1] -= 1
                    
            # Enter
            if inputs.is_key_down(self._inputAxes[4]):
                x = self._gridPos[0]
                y = self._gridPos[1]
                
                if (grid[x][y] == 0):
                    grid[x][y] = self._id
                    if self._id == 1:
                        objgrid[x][y] = GRectangle(x=self._pointer.x,y=self._pointer.y,
                            width=POINTER_SIZE, height=POINTER_SIZE,fillcolor='magenta')
                    else:
                        objgrid[x][y] = GEllipse(x=self._pointer.x,y=self._pointer.y,
                            width=POINTER_SIZE,height=POINTER_SIZE,fillcolor='cyan')
                        
                    self._done = True
        
    
        self._lastkey = (inputs.is_key_down(self._inputAxes[0]) or inputs.is_key_down(self._inputAxes[1])
                         or inputs.is_key_down(self._inputAxes[2]) or inputs.is_key_down(self._inputAxes[3]))
        
    
    def draw(self, view):
        """ Draws the player's pointer to view
        
        Parameter view: the view to draw on
        Precondition: view is an instance of GView"""
        self._pointer.draw(view)
        
        
    def resetPointer(self):
        """ Reset the pointer to the center of the screen """
        self._pointer.x = GAME_WIDTH/2
        self._pointer.y = GAME_HEIGHT/2
        self._gridPos = [1,1]