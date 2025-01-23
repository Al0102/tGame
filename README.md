# tGame

Python game engine for terminals

This is very crude, mostly for personal learning, but feel free to test it out.

## Getting Started

1. **Install**
`git clone https://github.com/Al0102/CP12-Collab-Assignment.git`
2. **Include**

* copy/move the files into your project or add to PATH
* import files:

``` py
import tGame
# Optional
import KEY, CONTROLS, Menu, Entity
```

* if not in same directory as main file:

``` py
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "relative/path/to/folder"))
import tGame
# Optional
import KEY, CONTROLS, Menu, Entity
```

3. **Initialise**

* call `tGame.init()`
* check if correct os is recognised:
* `tGame.POSIX` equals `True` for posix systems (mac, linux, etc.)
* `tGame.WINDOWS` equals `True` for windows systems

4. **Ending the Program**

* At the the of your code (especially if you are on posix system), run `tGame.quit()`

*tGame.py*

``` py
def end():
    if POSIX:
        import termios
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
```

* This should be in a `finally` block to ensure your terminal settings are returned to normal

## Features

### Input

* tty, termios, stdin for linux/mac
* msvcrt for windows

**Create KeyboardInput object**

``` py
import tGame

tGame.init()
input_ = tGame.KeyboardInput()
```

**KeyboardInput.keyIn(self)**

* returns symbol from `KEY` (or `CONTROLS` for arrow keys)
* sets `KeyboardInput.pressed` to the symbol or 0 if input was unrecognised
* if unbound control code is mashed more than `KeyboardInput.max_control_code_mash` (default: 5) times returns `KEY.QUIT`

### Using `tGame.render`

**render(\*commands)**

* stores everything in a string (`render_buffer`)
* display stuff to the screen
* Use ANSI escape sequences to:
    * move around cursor (will add more functions to replace this later)
    * clear specific areas of the screen
    * other cool stuff that may be terminal specific...

**renderCopy()**

* calls `sys.stdout.write(render_buffer)` and `sys.stdout.flush`
* clears `render_buffer` (calls `clearRenderBuffer()`)

**clearRenderBuffer()**

* sets `render_buffer` to empty string

### ASCII Images with Colour

* import text files with "images" and a colour map to go along with it
* colour corresponds to the second digit of the 3-bit colour ANSI escape sequence (found here: [Wikipedia: Ansi Escape Sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit))

**import\_image(file, height, start=1, do\_colour=False)**

* returns printable string ASCII image + ANSI colour sequences from file
* lines separated with `\n`

Parameters:

* `file`: name of file to import from - `str`
* `height`: height or lines taken up by image - `int` \> 0
* `start`: first line to search for image; starts at 1 - `int` \> 0
* `do_colour`: imports the next `height` lines after `height+start-1`; then calls `merge_ascii_colourmap`- `bool`

**merge\_ascii\_colourmap(image, bitmap)**

* returns printable string ASCII image + ANSI colour sequences
* lines separated with `\n`
* `image`: ASCII image - `\n` separated **string** or **2D list** of characters
* `bitmap`: matching colour bitmap - `\n` separated **string**, **list** of strings, or **2D list** of characters/integers
    * colour's corresponding integer must be from 0-7

Example:
*image.txt*

```
   |||
\\\|||/// 
 ┌─────┐
 │ 0 0 │
 │  o  │
 │\___/│
 └─────┘
   000
000000000 
 3333333
 3 7 7 3
 3  2  3
 3111113
 3333333
```

*main.py*

``` py
import tGame

print(tGame.import_image(file="images.txt", height=7, start=1, do_colour=True))
```

*output\**
   <span class="colour" style="color:black">\|\|\|</span>
<span class="colour" style="color:black">\\\\\\|\|\|///</span>
<span class="colour" style="color:yellow">┌──┐</span>
<span class="colour" style="color:yellow">│</span> 0 0<span class="colour" style="color:yellow">│</span>
<span class="colour" style="color:yellow">│</span>  0  <span class="colour" style="color:yellow">│</span>
<span class="colour" style="color:yellow">│</span><span class="colour" style="color:red">\\\_\_/</span><span class="colour" style="color:yellow">│</span>
<span class="colour" style="color:yellow">└──┘</span>

*\*probably won't show up properly on github*

### App title

* sends command to `render_buffer`,
    * needs to call `tGame.renderCopy()` after

**setTitle(title)**
Parameters:

* `title`: new title of current window - `str`

*Example:*

``` py
import tGame

tGame.init()
tGame.setTitle("This is tGame!")
```

### Clearing the screen

* sends `"\033[2J"` to render\_buffer via `tGame.render()`
    * clears screen and sets cursor to top left (DOS [ANSI.SYS](https://en.wikipedia.org/wiki/ANSI.SYS))
    * needs to call `tGame.renderCopy()` after

### Cursor

* sends command to `render_buffer`,
    * needs to call `tGame.renderCopy()` after

**moveCursor(direction, amount=1)**

* displaces cursor in the terminal

Parameters:

* `direction`: single character indicating direction of movement - `chr`
    * corresponds to ANSI escape code movement:
    * `'A'` \- UP
    * `'B'` - DOWN
    * `'C'` - RIGHT
    * `'D'` - LEFT
* `amount`: distance to move cursor - `int` \> 0

**setCursor(x, y)**

* moves cursor to position in the terminal

Parameters:

* `x`: column to move cursor to (starts at 1) - `int` \> 0
* `y`: row to move cursor to (starts at 1) - `int` \> 0

**showCursor()**

* turns on cursor

**hideCursor()**

* turns off cursor (can still move it around)

### Incomplete/Potentially Buggy Features

### Colour

* import Colour.py (does not require tGame.init())
* Get the ANSI escape sequence(s) for the input colour

Example

``` py
import Colour

Colour.FOREGROUND_COLOURS["RED"] # Any defined in Colour.AVAILABLE_COLOURS ("BLACK","RED","GREEN","YELLOW","BLUE","MAGENTA","CYAN","WHITE")
Colour.BACKGROUND_COLOURS["RED"] # Any defined in Colour.AVAILABLE_COLOURS ("BLACK","RED","GREEN","YELLOW","BLUE","MAGENTA","CYAN","WHITE")

contrastRGB((190, 55, 0)) # Returns a tuple containing RGB values contrasting the colour passed in (not true contrast, based off arbitrary numbers that mostly work)
contrast8Bit(200) # Returns an integer of the 8-bit colour that contrasts the colour passed in 

# Colour.py
# COLOUR_OPTION = Enum("COLOUR_OPTION", "FOREGROUND BACKGROUND AUTO_FRONT AUTO_BACK")

# AUTO options create contrasting background/foreground colour as well
# e.g AUTO_FRONT with white passed in would yield f"{code-for-white-foreground}{code-for-black-background}

# Returns a string for the ANSI escape code corresponding to the RGB colour passed in
# This is based on the option provided (Colour.COLOUR_OPTION)
getCodeRGB((0,0,255), Colour.COLOUR_OPTION.FOREGROUND)

# Returns a string for the ANSI escape code corresponding to the 4-bit (8) colour passed in
# This is based on the option provided (Colour.COLOUR_OPTION) and whether it is bright
getCodeBasic(AVAILABLE_COLOURS.index("RED"), Colour.COLOUR_OPTION.FOREGROUND, bright=True): 

# Returns a string for the ANSI escape code corresponding to the 8-bit (256) colour passed in
# This is based on the option provided (Colour.COLOUR_OPTION)
getCode8Bit(125, Colour.COLOUR_OPTION.AUTO_FRONT)
```

### Menu

* import Menu.py and tGame.py
* keypad style or classic vertical/horizontal style available

**Keypad**

- Create `Keypad` object

``` py
import tGame
from Menu import Keypad

nums = [9,8,7,
        6,5,4,
        3,2,1,
       ' ', 0]
# ' ' is put in for formatting, but won't affect the available options
# May make better solution for this or let you choose the whitespace character later on
numpad = Keypad(nums)
```

- Format your `Keypad`

```py
numpad.format(
            layout=Keypad.LAYOUT.HORIZONTAL, # VERTICAL HORIZONTAL
'''            Horizontal Layout
                9 8 7  
                6 5 4
                3 2 1
                  0

               Vertical Layout
                9 6 3  
                8 5 2 0
                7 4 1
'''
            items_per_layer=3, # Items in each row (LAYOUT.HORIZONTAL) or column (LAYOUT.VERTICAL)
            x=5,y=5, # Positions starting at topleft (x=1,y=1)
            padding=1, # Whitespace between items
            text_colour=(0,255,0) # Colour of items, calls getCodeRGB(self.colour,COLOUR_OPTION.AUTO_BACK) for item under cursor
            # Coming sometime later
            # text_align
            # fit
```

- Draw your `Keypad`
```py
numpad.draw() # Draws before getting stopped by input
tGame.renderCopy()
```

- Update your `Keypad`
   - Pass in input
   - Pass in the optional `draw` argument (default: True)
```py
Input = KeyoboardInput()

while Input.keyIn() != KEY.ESC: # Takes input, breaks out of the loop if it is KEY.ESC

   selection = numpad.update(Input.pressed, draw=True) # returns (index, choice) if CONTROLS.ACTION is pressed, else None

   # Moves to bottom left and prints pressed number
   if selection:
      tGame.moveCursor('B', 1000)
      tGame.moveCursor('B', 1000)
      tGame.render("You pressed {}".format(selection[1])) # selection[1] gets the value only

   tGame.renderCopy() # Remember to call renderCopy to update everything
```

**OptionScreen**
- Composed of a `Keypad`
- Acts as an entire scene with its own loop

- Create `OptionScreen`

```py
from Menu import OptionScreen
import tGame
from myfunctionsfoobar import open_options_screen, say_hi, game_quit

start_menu = OptionScreen(
                  ["start", "options", "Say Hi", "quit"], # Options
                  # Corresponding function for each option
                  # If the function returns KEY.QUIT, the menu will close itself
                  [lambda: KEY.QUIT, open_options_screen, say_hi, game_quit]) 
```

- Open your `OptionScreen`
   - Pass in a `KeyboardInput` object
```py
Input = tGame.KeyboardInput()
start_menu.open_menu(Input)
```

- Close your `OptionScreen`
   - Putting in CONTROLS.ESCAPE will close the menu and return 0
   - Your function options should return KEY.QUIT if the `OptionScreen` should close upon return

### Entities and stuff
- It's been almost 2 years since I touched this code so I will leave this to you to decipher
- I recommend making your own classes for these
- Take a look at `examples/test.py` for usage
