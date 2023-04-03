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

# MAKE THIS SO IT APPENDS TO AN EMPTY STRING UNTIL IT'S FIVE CHARS
# the hard limit of the pre-existing string is silly.
# f strings for adding
# my_str = mystr[:-1] for removing
# how to stop string at five chars
# disregard everything added after five chars
# if len(this_guess) < 5: add
# if len(this_guess == 5: allow enter to submit guess
# can I do it without an if statement?
# five character guess = input?

# I THINK I'M STUCK IN THIS WHILE LOOP LOL
# I gotta add an argument to get me out of the while loop from another function?!?!?!
# it feels messy, but I'll look into it!!

def collect_guess():
    curses.noecho()
    i = 0
    break_flag = False
    guess = ""
    while True:
        letter = stdscr.getkey()
        if str.isalpha(letter) == True and len(guess) < 5:
            guess = f"{guess}{letter}"
        elif letter in ('KEY_BACKSPACE', '\b', '\x7f'):
            guess = guess[:-1]
        rows, cols = stdscr.getmaxyx()
        # printc(guess.ljust(cols),"this guess: ", -20)
        # printc(str(len(guess)).ljust(cols),"guess len: ", -19)
    guess = (''.join(this_guess[:5])).upper()
    return guess

def print_guess(y,x):
    while True:
        # print the characters inside the grid
        # the first character is in position one
        # ie guess[0] is in y,0
        # guess[1] should be in y,2
        # guess[2] should be in y,4
        # guess[3] should be in y,6
        # so the x position of each letter should be twice it's index...
        guess = collect_guess()
        printc(guess.ljust(cols),"this guess: ", -20)
        printc(str(len(guess)).ljust(cols),"guess len: ", -19)
        for i, c in enumerate(list(guess)):
            curses.addch(y,i*2,c)
            printc(str(guess),"print guess: ", -18)




"""
run guess on correct line
check guess against word
    count instances of each letter in the word
    cap feedback of each guess letter at quantity of word letters
    green feedback takes precedent over yellow or missing
    yellow takes precedent over missing

    iterate over word for letters not in the word, to mark on letterfeedback
    iterate over word for green letters, removing letters from wordletter list
    iterate over word for yellow letters
"""

def check_guess(y, x):
    this_guess = collect_guess(y, x)
    word_letters = list(word)
    n=1
    # check for green (1), red (2), yellow (3)
    while n < 3:
        # check for green
        # for each letter in the word, and it's index
        for i, l in enumerate(word):
            # if this letter equals the letter in the same position in the guess
            if l == list(this_guess)[i]:
                # mark correct in letter list (this should be a its own function)
                # mark correct in guess line
                # find letter in line, make it green
                guess_letter = list(this_guess).index(l)
                # NOT DOING THE LAST ONE HERE (but doing it next?)
                printc(str(guess_letter),"some kinda index: ",-24)
                if l in word_letters:
                    stdscr.addch(y,x+(guess_letter*2),"!")
                    word_letters.pop(word_letters.index(l))
                # I gotta check against the original word, and then only mark if there are instances of the word left in word_letters lol
        n += 1
        for i, l in enumerate(word):
            # if this letter is in the guess
            if l.upper() in list(this_guess):
                # mark yellow in letter list (this should be a its own function)
                # mark yellow in guess line
                # find letter in line, make it yellow
                guess_letter = list(this_guess).index(l)
                # stdscr.addstr(y,x+(guess_letter*2),str(guess_letter))
                # stdscr.addstr(y,x+(guess_letter*2),"?")
                # remove from wordletter list
                if l in word_letters:
                    stdscr.addch(y,x+(guess_letter*2),"?")
                    word_letters.pop(word_letters.index(l))
                n += 1
            else:
                # mark red
                # n += 1
                pass

guess1y = grid_y+1
guess1x = grid_x+1


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    grid(grid_y,grid_x,try_count)
    print_guess(guess1y,guess1x)
    stdscr.refresh()
    sleep(3)
    curses.curs_set(1)


wrapper(main)

