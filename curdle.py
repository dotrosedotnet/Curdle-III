#!/usr/bin/env python3

import curses
from curses import wrapper
from time import sleep
import random
from string import ascii_uppercase as abcs

""""
as far as what Max taught me:

restructuring is the part I'm really excited about here.

classes are functions with their own data/datatypes?

let's do some classes research...

(before I'm doing classes research: another way to do this is to pass in a dict with all the necessary info to all functions which need it)

Max spoke a lot about "functions as subroutines"
""""

TRY_COUNT = 6
LETTER_COUNT = 5

# collecting print stuff
stdscr = curses.initscr()
rows, cols = stdscr.getmaxyx()
grid_x = (round(cols / 2) - letter_count - 1)
grid_y = (round(rows / 10))

# word = ("stops").upper()

WORDS = []

with open("scrabble.txt", mode='r', encoding='utf-8') as f:
    for item in f:
        if len(item) == (letter_count + 1):
            words.append(str.rstrip(item).upper())

WORD = str(words[random.randint(0,len(words)-1)]).upper()

def repeat(thing, n):
    return [thing for _ in range(n)]


# move this into a grid function

GRID_ROWS = {
    "grid_open" :  "┌" + '┬'.join(repeat("─",LETTER_COUNT)) + "┐",
    "grid_try" :   "│" + '│'.join(repeat(" ",LETTER_COUNT)) + "│",
    "grid_break" : "├" + '┼'.join(repeat("─",LETTER_COUNT)) + "┤",
    "grid_close" : "└" + '┴'.join(repeat("─",LETTER_COUNT)) + "┘",
}

GRID = '''\
{grid_open}
{grid_repeat}
{grid_close}\
'''.format(
    **GRID_ROWS,
    grid_repeat = "\n".join(repeat(GRID_ROWS["grid_break"] + "\n" + GRID_ROWS["grid_try"], TRY_COUNT))
)

# python logging to file/tail
# debugging printing made easyish (replace this with a file/tail)
def printc(string,label="",yoffset=0):
    rows, cols = stdscr.getmaxyx()
    string = str(string)
    stdscr.addstr(rows-5+yoffset, 1,"".ljust(cols))
    stdscr.addstr(rows-5+yoffset, 1, ''.join([label,string]))

def a_guess(y,x,l):
    curses.noecho()
    this_guess = ""
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

        # if word is correct length and in the word list, allow submission
        if len(guess_list) == letter_count and this_guess.upper() in words:
            if letter in ('\n', '\r', 'KEY_ENTER'):
                this_guess = this_guess.upper()
                # printc(this_guess.ljust(cols),"this guess: ", -14)
                return this_guess
        # printc(str(submitted),"submitted: ", -15)

def print_letter_graph(y,x):
    correct_f = curses.color_pair(1)
    present_f = curses.color_pair(2)
    absent_f = curses.color_pair(3)
    line_one = "Q W E R T Y U I O P"
    line_two = "A S D F G H J K L"
    line_three = "Z X C V B N M"
    center = int(round(cols/2))
    center_x_one = int(center-(round(len(line_one))/2))
    center_x_two = int(center-(round(len(line_two))/2))
    center_x_three = int(center-(round(len(line_three))/2))
    y_one = grid_y+(try_count*2)+2
    y_two = grid_y+(try_count*2)+3
    y_three = grid_y+(try_count*2)+4
    stdscr.addstr(y_one,center_x_one,line_one)
    stdscr.addstr(y_two,center_x_two,line_two)
    stdscr.addstr(y_three,center_x_three,line_three)

KEYBOARD_FB = {}

for i, l in enumerate(list(abcs)):
    keyboard_fb.update(
        {l:
         {"score": 0, "line": 0}
         }
    )

def used_letter_graph(y,x,scores,keyboard_fb_graph):
    correct_f = curses.color_pair(1)
    present_f = curses.color_pair(2)
    absent_f = curses.color_pair(3)
    line_one = "Q W E R T Y U I O P"
    line_two = "A S D F G H J K L"
    line_three = "Z X C V B N M"
    center = int(round(cols/2))
    center_x_one = int(center-(round(len(line_one))/2))
    center_x_two = int(center-(round(len(line_two))/2))
    center_x_three = int(center-(round(len(line_three))/2))
    y_one = grid_y+(try_count*2)+2
    y_two = grid_y+(try_count*2)+3
    y_three = grid_y+(try_count*2)+4
    # stdscr.addstr(y_one,center_x_one,line_one)
    # stdscr.addstr(y_two,center_x_two,line_two)
    # stdscr.addstr(y_three,center_x_three,line_three)

    for letter, ldict in keyboard_fb.items():
        if letter in line_one:
            ldict["line"] = 1
        elif letter in line_two:
            ldict["line"] = 2
        else:
            ldict["line"] = 3

    for k, v in scores.items():
        l = v["letter"]
        if v["absent"] == 1:
            keyboard_fb[l]["score"] = 3
        if v["correct"] == 1:
            keyboard_fb[l]["score"] = 1
        if v["present"] == 1 and keyboard_fb[l]["score"] != 1:
            keyboard_fb[l]["score"] = 2

    for k, v in keyboard_fb.items():
        match v["line"]:
            case 1:
                print_x = line_one.index(k)+center_x_one
                match v["score"]:
                    case 3:
                        stdscr.addch(y_one,print_x,k,absent_f)
                    case 2:
                        stdscr.addch(y_one,print_x,k,present_f)
                    case 1:
                        stdscr.addch(y_one,print_x,k,correct_f)
            case 2:
                print_x = line_two.index(k)+center_x_two
                match v["score"]:
                    case 3:
                        stdscr.addch(y_two,print_x,k,absent_f)
                    case 2:
                        stdscr.addch(y_two,print_x,k,present_f)
                    case 1:
                        stdscr.addch(y_two,print_x,k,correct_f)
            case 3:
                print_x = line_three.index(k)+center_x_three
                match v["score"]:
                    case 3:
                        stdscr.addch(y_three,print_x,k,absent_f)
                    case 2:
                        stdscr.addch(y_three,print_x,k,present_f)
                    case 1:
                        stdscr.addch(y_three,print_x,k,correct_f)
    # printc(keyboard_fb,"kb_fb: ",-10)


def check_guess(y,x):
    correct_f = curses.color_pair(1)
    present_f = curses.color_pair(2)
    absent_f = curses.color_pair(3)
    this_guess = a_guess(y,x,letter_count)

    if this_guess == word:
        printc("SUCCESS!","Success?: ", -5)
        for l in list(word):
            stdscr.addch(y,x,l,correct_f)
            x += 2
        return True
    else:
        scores = {}
        for i, l in enumerate(list(this_guess)):
            scores.update(
                {i:
                 {"letter": l, "correct": 0, "present": 0, "absent": 0, "marked": 0}
                }
            )

        letter_amounts = {}

        for l in list(word):
            if l not in letter_amounts.keys():
                letter_amounts.update({l: 1})
            else:
                letter_amounts[l] = letter_amounts[l] + 1

        # score word
        for i, l in enumerate(list(this_guess)):
            if l not in list(word):
                scores[i]["absent"] = 1
            if l == word[i]:
                scores[i]["correct"] = 1
            if l in list(word):
                scores[i]["present"] = 1

        # printc(scores,"scores:  ",-4)
        # printc(word,"word: ", 0)
        # look over word, checking each letter for its three scores
        # if letter is in word, count instances

        for k, v in scores.items():

            l = v["letter"]

            if v["correct"] == 1 and letter_amounts[l] > 0:
                letter_amounts[l] = letter_amounts[l]-1
                stdscr.addch(y,x+(k*2),l,correct_f)
                v["marked"] = 1

        for k, v in scores.items():

            l = v["letter"]

            # mark as red if not present, or unmarked and 0

            if v["absent"] == 1:
                stdscr.addch(y,x+(k*2),l,absent_f)

            if v["present"] == 1 and letter_amounts[l] > 0 and v["marked"] == 0:
                letter_amounts[l] = letter_amounts[l]-1
                stdscr.addch(y,x+(k*2),l,present_f)
                v["marked"] = 1

            if letter_amounts.get(l) == 0 and v["marked"] == 0:
                stdscr.addch(y,x+(k*2),l,absent_f)

        # for i, l in enumerate(scores.values()):
            # printc(l,"",-20+i)
        # printc(letter_amounts,"l #: ",-5)

        used_letter_graph(y,x,scores,keyboard_fb)

        # for (i, d) in score.items():
        #     # printc(this_guess[i],"l: ",-1)
        #     # printc(str(d[this_guess[i]]),"s: ",-2)
        #     stdscr.refresh()
        #     sleep(0.04)
        #     if d[this_guess[i]] == 3:
        #         stdscr.addch(y,x+(i*2),this_guess[i],absent_f)
        #     if d[this_guess[i]] == 2:
        #         stdscr.addch(y,x+(i*2),this_guess[i],present_f)
        #     if d[this_guess[i]] == 1:
        #         stdscr.addch(y,x+(i*2),this_guess[i],correct_f)
        # printc(str(score),"score: ", -3)

    # printc(str(score),"score: ", -4)
    # printc(this_guess,"this_guess: ", -6)
    # printc(str(score),"score: ", -7)
    # printc(str(present_letters),"present_letters: ", -12)
    # printc(str(absent_letters),"absent_letters: ", -11)
    # printc(str(correct_popped),"correct popped: ", -9)
    # printc(str(present_popped),"present popped: ", -8)
    # for item in present_letters:
    #     stdscr.addch(y,x+(item[1]*2),item[0],present_f)
    # for item in absent_letters:
    #     stdscr.addch(y,x+(item[1]*2),item[0],absent_f)
    return False


def guess_conveyor(y,x):
    success = False
    guesses = 0
    while guesses < try_count and success == False:
        success = check_guess(y,x)
        guesses += 1
        y += 2
        # printc(str(success),"success: ",1)

"""
for printing stuff to work, it has to be operating at a guess frequency

or maybe it should just update when it receives new info
"""

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)
    stdscr.clear()
    grid(grid_y,grid_x,try_count)
    print_letter_graph(grid_y,grid_x)
    guess_conveyor(grid_y+1,grid_x+1)
    stdscr.refresh()
    sleep(3)
    curses.curs_set(1)


if __name__ == "__main__":
    wrapper(main)

