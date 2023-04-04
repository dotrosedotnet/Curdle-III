#!/usr/bin/env python3

import curses
from curses import wrapper
from time import sleep
import pdb

stdscr = curses.initscr()

word = ("stops").upper()

grid_x = 0
grid_y = 0
try_count = 6
letter_count = 5

line_parts = ["┌","─┬","─┐","│" ," │"," │","├" ,"─┼","─┤","└" ,"─┴","─┘",]

grid_rows = {
    "grid_open": "",
    "grid_try": "",
    "grid_break": "",
    "grid_close": ""
}

guess = list(" "*5)

def printc(string,label="",yoffset=0):
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(rows-5+yoffset, 1,"".ljust(cols))
    stdscr.addstr(rows-5+yoffset, 1, ''.join([label,string]))

p = 0
for k, v in grid_rows.items():
    grid_rows[k] = line_parts[p]
    p += 1
    grid_rows[k] = grid_rows[k]+(line_parts[p] * (letter_count-1))
    p += 1
    grid_rows[k] = grid_rows[k]+line_parts[p]
    p += 1


def grid(y,x,try_count):
    stdscr.addstr(y,x,grid_rows['grid_open'])
    i=1
    while i < try_count*2:
        stdscr.addstr(y+i,x,grid_rows['grid_try'])
        stdscr.addstr(y+1+i,x,grid_rows['grid_break'])
        i+=2
    stdscr.addstr(y+(try_count*2),x,grid_rows['grid_close'])

guess = ""

def a_guess(y,x,l):
    curses.noecho()
    this_guess = guess
    submitted = False
    rows, cols = stdscr.getmaxyx()
    del_ch=cols-1
    while True:

        # collection begins here
        letter = stdscr.getkey()
        if str.isalpha(letter) == True and len(this_guess) < l:
            this_guess = f"{this_guess}{letter}"
        elif letter in ('KEY_BACKSPACE', '\b', '\x7f'):
            this_guess = this_guess[:-1]
            del_ch = x+(len(this_guess)*2)
        printc(this_guess.ljust(cols),"this guess: ", -20)
        printc(str(len(this_guess)).ljust(cols),"guess len: ", -19)

        # printing in grid begins here
        guess_list = list(this_guess)
        printable = '│'.join(this_guess).upper()
        stdscr.addch(y,del_ch," ")
        stdscr.addstr(y,x,printable)
        printc(str(guess_list),"guess list: ", -18)
        printc(printable,"printable: ", -17)

        printc(str(len(guess_list)),"guess_list len: ", -16)
        # ADD LEGITIMATE WORD STIPULATION
        if len(guess_list) == 5:
            if letter in ('\n', '\r', 'KEY_ENTER'):
                this_guess = this_guess.upper()
                printc(this_guess.ljust(cols),"this guess: ", -14)
                return this_guess
        printc(str(submitted),"submitted: ", -15)

def check_guess(y,x):
    this_guess = a_guess(y,x,letter_count)
    correct_letters = []
    present_letters = []
    absent_letters = []
    if this_guess == word:
        printc("SUCCESS!","Success?: ", -5)
    else:
        for i, l in enumerate(list(this_guess)):
            word_letters = list(word)
            if word[i] == this_guess[i]:
                correct_letters.append(l)
                word_letters.pop(i)
            elif l in word_letters:
                present_letters.append(l)
            else:
                absent_letters.append(l)

    printc(str(correct_letters),"correct_letters: ", -13)
    printc(str(present_letters),"present_letters: ", -12)
    printc(str(absent_letters),"absent_letters: ", -11)
    printc(str(word_letters),"word_letters: ", -10)



guess1y = grid_y+1
guess1x = grid_x+1


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    grid(grid_y,grid_x,try_count)
    check_guess(guess1y,guess1x)
    stdscr.refresh()
    sleep(100)
    curses.curs_set(1)


wrapper(main)

