#!/usr/bin/python
# -*- coding: latin-1 -*-
import curses
import time
import random
from playsound import playsound
import threading
import pickle
from curses import textpad

menu = ['New Game', 'Quit']
hi_score = 0
    
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    texto = "S  N  A  K  E   G  A  M  E"
    x = w//2 - len(texto)//2
    stdscr.addstr(10, x, texto)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def center_text(stdscr,text):
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    
def print_center(stdscr, text):
    stdscr.clear()
    center_text(stdscr,text)
    stdscr.refresh()

def pantalla(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    current_row = 0

    print_menu(stdscr, current_row)

    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row== len(menu)-1:
                print_center(stdscr, "See you later".format(menu[current_row]))
                playsound("seeyou.mp3")
                time.sleep(1)
                break
            else:
                stdscr.clear()
                main(stdscr)
                break
        print_menu(stdscr, current_row)      
          
def create_food(snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food

def main(stdscr):
    global FT, hi_score
    curses.curs_set(0)
    
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    stdscr.addstr(1,81,"'q'=QUIT  <SPACE BAR>=PAUSE/CONTINUE")
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    for y,x in snake:
        stdscr.addstr(y, x, '#')

    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    score = 0
    score_text = "Score: {}".format(score)
    hi_score_text = "Hi-Score: {}".format(hi_score)
    stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)
    stdscr.addstr(1, 4, hi_score_text)

    def pause_sound():
        playsound("gamepaused.mp3")

    def init_pausesound():
        t = threading.Thread(target=pause_sound)
        t.start()

    PAUSE = False

    while 1:
        key = stdscr.getch()

        if key == ord(' '):
            if PAUSE == False:
                PAUSE = True
                init_pausesound()
                center_text(stdscr,"PAUSE")
            else:
                PAUSE = False
                center_text(stdscr,"     ")


        if key == ord('q') or key == ord('Q'):
            break

        if PAUSE == False:
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
                curses.beep()
                score += 1
                if score > hi_score:
                    hi_score+=1
            
                hi_score_text = "Hi-Score: {}".format(hi_score)
                score_text = "Score: {}".format(score)
                stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)
                stdscr.addstr(1, 4, hi_score_text) 

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
                stdscr.getch()
                playsound("game over.mp3")
                stdscr.nodelay(0)
                time.sleep(1)
                break
    pantalla(stdscr)

curses.wrapper(pantalla)
