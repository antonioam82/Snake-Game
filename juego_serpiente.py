import random
import curses
import time
from curses import textpad

def create_food(snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]  
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    for y,x in snake:
        stdscr.addstr(y, x, '#')
        
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    score = 0
    score_text = "Puntuación: {}".format(score)
    stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)

    while 1:
        key = stdscr.getch()

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)

            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '*')

            stdscr.timeout(100 - (len(snake)//3)%90)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or 
            snake[0][1] in [box[0][1], box[1][1]] or 
            snake[0] in snake[1:]):
            msg = "Game Over!"
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            time.sleep(2)
            break

curses.wrapper(main)
