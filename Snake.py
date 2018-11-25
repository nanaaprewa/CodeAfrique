'''
This method implements the popular snake game we all use to play as kids:
You have a snake and a food. The snake moves towards the food to eat it and
grows anytime it eats the food.
You are responsible for implementing code that conntrols the
navigation of the snake. That is, if the up key is pressed, the snake should
move, if the down key is pressed, it should move down etc.
You're given an given the variable "key", which is the key that the user pressed
on the keyboard, and new_head which is the current position of the snake.

Structure of new_head:
Increase new_head[0] by one if you want to down and decrease by one if you
want to go up.
Increase  new_head[1] by one if you want to right and decrease by one if you
want to go left.
'''
import random
import curses

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)
DOWN_ARROW = curses.KEY_DOWN
UP_ARROW = curses.KEY_UP
RIGHT_ARROW = curses.KEY_RIGHT
LEFT_ARROW = curses.KEY_LEFT
snk_x = sw/4
snk_y = sh/2

snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2],
    [snk_y, snk_x-3]
]
food = [sh/2, sw/2]
w.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:
    ## get key pressed
    next_key = w.getch()
    key = key if next_key == -1 else next_key
    ## Quit game if the snake hits any of the walls
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        quit()
    new_head = [snake[0][0], snake[0][1]]
    ###DONOT CHANGE CODE ABOVE
    ##Implement me (Students will be responsible for implementing the commented
    ##out section)

    # if key == DOWN_ARROW:
    #     new_head[0] += 1
    # if key == UP_ARROW:
    #     new_head[0] -= 1
    # if key == LEFT_ARROW:
    #     new_head[1] -= 1
    # if key == RIGHT_ARROW:
    #     new_head[1] += 1

    ##DONOT CHANGE CODE BELOW
    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sh-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
