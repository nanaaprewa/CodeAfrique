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
import time

s = curses.initscr()
curses.start_color()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh+1, sw+1, 0, 0)
w.keypad(1)
w.timeout(100)
maxScore = 0
scores = []
score = 0
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
color = random.randint(1,6)
curses.init_pair(1, color, curses.COLOR_WHITE)
curses.init_pair(2, 2, curses.COLOR_WHITE)
try:
    with open("high score","r") as f:
        scores = [int(i)  for j in f for i in j.strip().split(" ") if i.isdigit()]
        f.close()
except:
    print("File doesn't exist")
if len(scores) > 0:
    maxScore = max(scores)

while True:
    w.addstr(0, 2, 'Score : ' + str(score) + ' ',curses.color_pair(1))
    w.addstr(0, 20, 'High Score : ' + str(maxScore) + ' ',curses.color_pair(2))

    prevKey = key
    #Increases the speed of Snake as its length increases
    w.timeout(100 - (len(snake)/5 + len(snake)/10)%120)

    next_key = w.getch()
    key = key if next_key == -1 else next_key

    if key == ord(' '):          # If SPACE BAR is pressed, wait for another
        key = -1                 # one (Pause/Resume)
        while key != ord(' '):
            key = w.getch()
        key = prevKey
        continue
         # If an invalid key is pressed
    if key not in [ curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, 27]:
        key = prevKey

### DO NOT CHANGE CODE ABOVE

### Students are responsible for implementing the commented out  code
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    ### DO NOT CHANGE CODE BELOW
    snake.insert(0, new_head)

     # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = sh-1
    if snake[0][1] == 0: snake[0][1] = sw -1
    if snake[0][0] == sh: snake[0][0] = 1
    if snake[0][1] == sw: snake[0][1] = 1


    if snake[0] in snake[1:]:
        file = open('high score', 'a+')
        file.write(str(score) + '\n')
        file.close()
        time.sleep(1)
        curses.endwin()
        quit()

    if snake[0] == food:
        food = None
        score += 1
        while food is None:
            nf = [
                random.randint(1, sh-2),
                random.randint(1, sh-2)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
