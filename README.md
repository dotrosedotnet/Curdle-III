# Curdle-III

A Curses Wordle written in Python

This is my third attempt at an elegant, effective curses
Wordle (Curdle) in Python.

I love the terminal, and curses, and am finally learning to
program. I've learned a lot from my first two attempts, and
would love to finalize something that I'm proud of with this
one.

Some hopes for this attempt:

- appropriate use of for loops, functions
- clean, readable code
- separation of processes
	- separate guess creation from guess printing
	- separate guess feedback from guess creation/printing
		- feedback in grid (letter in word/not in word/in	the correct position)
		- feedback in keyboard representation of letters guessed
- learn more!

---

### It seems to be working! (20230418)

This Wordle implementation is presently culling from a
dictionary meant for Scrabble. As such, the words kinda
blow. Lots of esoteric garbage. If anybody wants to furnish
a more appropriate dictionary, that'd be great.

Also, plurals are allowed here. I would need a more robust
dictionary to remove plurals. Mine is just a list of words.

#### What's Special?

Besides it being exclusively in the terminal?

Baby, you can choose how many letters the word has! And how
many guesses you get!

At the moment, that's done by editing the `letter_count` and
`try_count` in the file. I'll add argument options later.

#### TODO:

- [ ] Add title
- [ ] Print correct word after losing
- [ ] Add argument options
	- [ ] Letter count
	- [ ] Guess count
- [ ] Offer [Q]uit at any time?

#### Aspirations for next projects:
- make use of `*args` and `**kwargs`
- use `pad` in `curses` to allow content beyond visible border
- implement `curses` redrawing with window resizing
- grok and use list/dict comprehension
- cleaner code babyyyy
