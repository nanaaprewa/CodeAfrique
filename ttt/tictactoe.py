"""
    Primary module for Tic Tac Toe.
    
    Created by Jesse Phillips on December 19, 2018

"""

from game2d import *
from player import *


# Constants
GAME_WIDTH = 800
GAME_HEIGHT = 600
GRID_SIZE = 3
TIMER = 150
STATE_INACTIVE = 0
STATE_TUTORIAL = 1
STATE_NEWGAME = 2
STATE_ACTIVE = 3
STATE_PAUSED = 4
STATE_COMPLETE = 5



class TicTacToe(GameApp):
    """
    The primary controller class for the Tic Tac Toe application app

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

    Method start begins the application.

    Method update either changes the state or updates the Play object

    Method draw displays the Play object and any other elements on screen
    
    INSTANCE ATTRIBUTES:
    view:     the game view, used in drawing (see examples from class)
              [instance of GView; it is inherited from GameApp]
    input:    the user input, used to control the ship and change state
              [instance of GInput; it is inherited from GameApp]
    _turn:    represents whose turn it is
              [boolean, True if Player 1's turn and False if Player 2's turn]
    _grid:    the tic tac toe grid. 0 in a pos in the grid means spot is empty,
              1 means player 1 has a token there and 2 means player 2 has a token there
              [int 2d array in row-major order]
    _objgrid: the tic tac toe grid with the actual objects [2d list of GObjects or None]
    _gridlines: represents the grid lines of the grid
              [list of GPath objects]
    _player1: represents Player 1
              [instance of Player]
    _player2: represents Player 2
              [instance of Player]
    _state:   represents the state of the game
            [STATE_INACTIVE, STATE_NEWGAME, STATE_PAUSED, STATE_ACTIVE, STATE_COMPLETE]
    _text:   represents text on the screen [instance of GLabel]
    _winState: 0 if a draw, 1 if Player 1 won, 2 if Player 2 won
    _complete: True if the game is over, False otherwise
    _timer:    countdown timer, used for timed messages [int >= 0]
    _nextTurn: the player who will start the next turn [boolean]
    """
    
    def changeTurn(self):
        """ Changes whose turn it is """
        self._turn = not self._turn
        
        
    def gridSetup(self):        
        """Helper function to set up the grid"""
        self._grid = []
        self._objgrid = []
        for i in range(GRID_SIZE):
            self._grid.append([0] * GRID_SIZE)
            self._objgrid.append([None] * GRID_SIZE)
        
        
    def start(self):
        """ Initializes the application """
        self._turn = True
        self.gridSetup()
        self._player1 = None
        self._player2 = None
        self._state = STATE_INACTIVE
        self._text = GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            text="Press 'P' to play Tic Tac Toe!",
                            font_size=32, font_name = "ArialBold.ttf")
        
        self.createGridLines()
        self._winState = 0
        self._complete = False
        self._timer = 2*TIMER
        self._nextTurn = not self._turn
    
    
    def update(self,dt):
        """ Animates a single frame in the game
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            if self.input.is_key_down('p'):
                self._state = STATE_TUTORIAL
        
        elif self._state == STATE_TUTORIAL:
            self._timer -= 1
            if self._timer > TIMER:
                self._text.text = "Player 1: Arrow keys to move, Space bar to select"
                
            elif self._timer == 0:
                self._timer = TIMER
                self._text = None
                self._state = STATE_NEWGAME
                
            else:
                self._text.text = "Player 2: WASD keys to move, E to select"
            
        elif self._state == STATE_NEWGAME:
            self._player1 = Player("Player 1",1)
            self._player2 = Player("Player 2",2)
            self._state = STATE_PAUSED
            
            
        elif self._state == STATE_ACTIVE:
            if self._turn:
                self._player1.play(self.input, self._grid, self._objgrid)
                playerDone = self._player1.getDone()
            else:
                self._player2.play(self.input, self._grid, self._objgrid)
                playerDone = self._player2.getDone()
                
            
            if playerDone:
                self.checkWinConditions()
                self.checkGridFull()
                
                if self._complete:
                    self._state = STATE_COMPLETE
                else:
                    self.changeTurn()
                    if self._turn:
                        self._player1.resetPointer()
                        self._player1.setDone(False)
                    else:
                        self._player2.resetPointer()
                        self._player2.setDone(False)
                    
                    self._state = STATE_PAUSED
        
        
        elif self._state == STATE_PAUSED:
            self.pauseHelper()
            
        elif self._state == STATE_COMPLETE:
            self.completeHelper()
            
    
    
    def draw(self):
        """ Draws the game objects to the view """
        if self._state == STATE_ACTIVE:
            for line in self._gridlines:
                line.draw(self.view)
                
            # Draw grid
            for i in range(3):
                for j in range(3):
                    if self._objgrid[i][j] is not None:
                        self._objgrid[i][j].draw(self.view)
                        
            if self._turn:
                self._player1.draw(self.view)
            else:
                self._player2.draw(self.view)
                
        if self._text is not None:
            self._text.draw(self.view)
    
        
    def createGridLines(self):
        """ Creates the tic tac toe grid lines """
        # Lower horizontal line
        self._gridlines = []
        self._gridlines.append(GPath(points = [0, GAME_HEIGHT/3, GAME_WIDTH, GAME_HEIGHT/3],
                            linewidth = 2, linecolor = 'black'))
        
        # Upper horizontal line
        self._gridlines.append(GPath(points = [0, 2*GAME_HEIGHT/3, GAME_WIDTH, 2*GAME_HEIGHT/3],
                            linewidth = 2, linecolor = 'black'))
        
        # Leftmost vertical line
        self._gridlines.append(GPath(points = [GAME_WIDTH/3, 0, GAME_WIDTH/3, GAME_HEIGHT],
                            linewidth = 2, linecolor = 'black'))
        
        self._gridlines.append(GPath(points = [2*GAME_WIDTH/3, 0, 2*GAME_WIDTH/3, GAME_HEIGHT],
                            linewidth = 2, linecolor = 'black'))
        
        
    def pauseHelper(self):
        """ Helper method for pause state """
        if self._turn and self._text is None:
            self._text = GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                        text=self._player1.getName() + "'s turn! Press Enter to Play!",
                        font_size=32, font_name = "ArialBold.ttf")
            
        elif self._text is None:
            self._text = GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                        text=self._player2.getName() + "'s turn! Press Enter to Play!",
                        font_size=32, font_name = "ArialBold.ttf")
            
        if self.input.is_key_down('enter'):
            self._state = STATE_ACTIVE
            self._text = None
            
            
    def checkWinConditions(self):
        """ Helper function to check the win conditions """
        # Check rows
        for i in range(3):
            if (self._grid[i][0] == self._grid[i][1] and self._grid[i][0] == self._grid[i][2]
                and self._grid[i][0] != 0):
                
                self._winState = self._grid[i][0]
                self._complete = True
                return
            
        # Check columns
        for i in range(3):
            if (self._grid[0][i] == self._grid[1][i] and self._grid[0][i] == self._grid[2][i]
                and self._grid[0][i] != 0):
                
                self._winState = self._grid[0][i]
                self._complete = True
                return
            
        # Check diagonals 
        if (self._grid[0][0] == self._grid[1][1] and self._grid[0][0] == self._grid[2][2]
            and self._grid[0][0] != 0):
            
            self._winState = self._grid[0][0]
            self._complete = True
            return
        
        if (self._grid[0][2] == self._grid[1][1] and self._grid[0][2] == self._grid[2][0]
            and self._grid[0][2] != 0):
            
            self._winState = self._grid[0][2]
            self._complete = True
            return
        
        
    def completeHelper(self):
        """ Helper function to handle when the game is over """
        if self._timer != 0:
            self._timer -= 1
            
        if self._winState == 1 and self._text is None:
            self._text = GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            text=self._player1.getName() + " wins!",
                            font_size=32, font_name = "ArialBold.ttf")
            
        elif self._winState == 2 and self._text is None:
            self._text = GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            text=self._player2.getName() + " wins!",
                            font_size=32, font_name = "ArialBold.ttf")
            
        elif self._text is None:
            self._text =  GLabel(x= GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            text="It's a draw!",
                            font_size=32, font_name = "ArialBold.ttf")
            
        if self._timer == 0:
            self._text.text = "Press 'P' to Play Again"
            if self.input.is_key_down('p'):
                self._timer = TIMER
                self.resetGame()
                
       
            
    def checkGridFull(self):
        """ Helper function to check if the grid is full """
        full = True
        for i in range(3):
            for j in range(3):
                if self._grid[i][j] == 0:
                    full = False
                    
        if full:
            self._complete = True
            self._winState = 0
        
        
    def resetGame(self):
        """ Helper function to reset the game """
        self.gridSetup()
        # Alternate the player who starts the game
        self._turn = self._nextTurn
        self._nextTurn = not self._turn
        self._complete = False
        self._winState = 0
        self._text = None
        self._state = STATE_NEWGAME
        
        
        
        