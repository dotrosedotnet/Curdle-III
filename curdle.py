#!/usr/bin/env python3

import curses
from curses import wrapper
from time import sleep
import random

stdscr = curses.initscr()

grid_x = 0
grid_y = 0
try_count = 6
letter_count = 5

# word = ("stops").upper()

words = []

with open("scrabble.txt", mode='r', encoding='utf-8') as f:
    for item in f:
        if len(item) == (letter_count + 1):
            words.append(str.rstrip(item).upper())


word = str(words[random.randint(0,len(words)-1)]).upper()

line_parts = ["┌","─┬","─┐","│" ," │"," │","├" ,"─┼","─┤","└" ,"─┴","─┘",]

grid_rows = {
    "grid_open": "",
    "grid_try": "",
    "grid_break": "",
    "grid_close": ""
}

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
        # printc(this_guess.ljust(cols),"this guess: ", -20)
        # printc(str(len(this_guess)).ljust(cols),"guess len: ", -19)

        # printing in grid begins here
        guess_list = list(this_guess)
        printable = '│'.join(this_guess).upper()
        stdscr.addch(y,del_ch," ")
        stdscr.addstr(y,x,printable)
        # printc(str(guess_list),"guess list: ", -18)
        # printc(printable,"printable: ", -17)

        # printc(str(len(guess_list)),"guess_list len: ", -16)
        # ADD LEGITIMATE WORD STIPULATION
        if len(guess_list) == letter_count and this_guess.upper() in words:
            if letter in ('\n', '\r', 'KEY_ENTER'):
                this_guess = this_guess.upper()
                # printc(this_guess.ljust(cols),"this guess: ", -14)
                return this_guess
        # printc(str(submitted),"submitted: ", -15)

used_letters = []

def check_guess(y,x):
    correct_f = curses.color_pair(1)
    present_f = curses.color_pair(2)
    absent_f = curses.color_pair(3)
    this_guess = a_guess(y,x,letter_count)
    correct_letters = []
    correct_popped = []
    present_letters = []
    present_popped = []
    absent_letters = []
    word_letters = []
    for l in list(this_guess.upper()):
        if l in used_letters:
            pass
        else:
            used_letters.append(l.upper())
    if this_guess == word:
        printc("SUCCESS!","Success?: ", -5)
        for l in list(word):
            stdscr.addch(y,x,l,correct_f)
            x += 2
        # need to mark success and stop taking guesses now
        # marks success = True in outer function
        return True
    else:
        score = {}
        for i, l in enumerate(list(this_guess)):
            score.update(
                {i:
                    {l: 0}
                }
            )

        word_letter_count = {}

        for l in list(word):
            if l in word_letter_count.keys():
                previous_quant = word_letter_count.get(l)
                word_letter_count.update({l:(previous_quant+1)})
            else:
                word_letter_count.update({l:1})

        # printc(str(word_letter_count),"WLC: ",0)

        # count missing letters
        for i, l in enumerate(list(this_guess)):
            if l not in list(word):
                score[i].update({l: 3})
                absent_letters.append([l,i])

        # check correct letters
        for i, l in enumerate(list(this_guess)):
            if word[i] == this_guess[i]:
                score[i].update({l: 1})
                correct_letters.append([l,i])
                word_letter_count[l] -= 1

        # check present letters
        for i, l in enumerate(list(this_guess)):
            # if l in word, isn't already marked present, and isn't already marked correct
            if l in list(word) and word_letter_count[l] > 0 and score[i].get(l) == 0:
                word_letter_count[l] -= 1
                score[i].update({l: 2})
                present_letters.append([l,i])


        # printc(str(word_letter_count),"WLC: ",1)

        for (i, d) in score.items():
            # printc(this_guess[i],"l: ",-1)
            # printc(str(d[this_guess[i]]),"s: ",-2)
            stdscr.refresh()
            sleep(0.04)
            if d[this_guess[i]] == 3:
                stdscr.addch(y,x+(i*2),this_guess[i],absent_f)
            if d[this_guess[i]] == 2:
                stdscr.addch(y,x+(i*2),this_guess[i],present_f)
            if d[this_guess[i]] == 1:
                stdscr.addch(y,x+(i*2),this_guess[i],correct_f)
        # printc(str(score),"score: ", -3)

    # printc(str(score),"score: ", -4)
    # printc(this_guess,"this_guess: ", -6)
    printc(word,"word: ", 0)
    # printc(str(score),"score: ", -7)
    # printc(str(correct_letters),"correct_letters: ", -13)
    # printc(str(present_letters),"present_letters: ", -12)
    # printc(str(absent_letters),"absent_letters: ", -11)
    # printc(str(word_letters),"word_letters: ", -10)
    # printc(str(correct_popped),"correct popped: ", -9)
    # printc(str(present_popped),"present popped: ", -8)
    # for item in present_letters:
    #     stdscr.addch(y,x+(item[1]*2),item[0],present_f)
    # for item in absent_letters:
    #     stdscr.addch(y,x+(item[1]*2),item[0],absent_f)
    return False

def used_letter_graph(y,x):
    line_one = "Q W E R T Y U I O P"
    line_two = "A S D F G H J K L"
    line_three = "Z X C V B N M"
    stdscr.addstr(grid_y+(try_count*2)+2,1,line_one)
    stdscr.addstr(grid_y+(try_count*2)+3,2,line_two)
    stdscr.addstr(grid_y+(try_count*2)+4,4,line_three)


def guess_conveyor(y,x):
    success = False
    guesses = 0
    while guesses < try_count and success == False:
        success = check_guess(y,x)
        guesses += 1
        y += 2
        printc(str(success),"success: ",1)


guess1y = grid_y+1
guess1x = grid_x+1


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)
    stdscr.clear()
    grid(grid_y,grid_x,try_count)
    used_letter_graph(grid_y,grid_x)
    guess_conveyor(guess1y,guess1x)
    stdscr.refresh()
    sleep(3)
    curses.curs_set(1)


wrapper(main)

