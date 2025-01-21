
# tGame

Python game engine for terminals  

This is very crude, mostly for personal learning, but feel free to test it out.  

## Features

### Input

- tty, termios, stdin for linux/mac  
- msvcrt for windows  

**Create KeyboardInput object**
```py
import tGame

tGame.init()
input_ = tGame.KeyboardInput()
```

**KeyboardInput.keyIn(self)**  
- returns symbol from `KEY` (or `CONTROLS` for arrow keys)
- sets `KeyboardInput.pressed` to the symbol or 0 if input was unrecognised
- if unbound control code is mashed more than `KeyboardInput.max_control_code_mash` (default: 5) times returns `KEY.QUIT`  

### ASCII Images with Colour

- import text files with "images" and a colour map to go along with it
- colour corresponds to the second digit of the 3-bit colour ANSI escape sequence (found here: [Wikipedia: Ansi Escape Sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit))

**import_image(file, height, start=1, do_colour=False)**  
- returns printable string ASCII image + ANSI colour sequences from file
- lines separated with `\n`  

Parameters:
- `file`: name of file to import from - `str` 
- `height`: height or lines taken up by image - `int` > 0 
- `start`: first line to search for image; starts at 1 - `int` > 0 
- `do_colour`: imports the next `height` lines after `height+start-1`; then calls `merge_ascii_colourmap`- `bool`  

**merge_ascii_colourmap(image, bitmap)**
- returns printable string ASCII image + ANSI colour sequences
- lines separated with `\n`  

- `image`: ASCII image - `\n` separated **string** or **2D list** of characters
- `bitmap`: matching colour bitmap - `\n` separated **string**, **list** of strings, or **2D list** of characters/integers
    - colour's corresponding integer must be from 0-7  

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
```py
import tGame

print(tGame.import_image(file="images.txt", height=7, start=1, do_colour=True))
```
*output\**
&nbsp; &nbsp;<span style='color:black;'>|||</span>
<span style='color:black;'>\\\\\\|||///</span>
<span style='color:yellow;'>┌──┐</span>
<span style='color:yellow;'>│</span> 0 0<span style='color:yellow;'>│</span>
<span style='color:yellow;'>│</span>&nbsp; 0 &nbsp;<span style='color:yellow;'>│</span>
<span style='color:yellow;'>│</span><span style='color:red;'>\\__/</span><span style='color:yellow;'>│</span>
<span style='color:yellow;'>└──┘</span>  

*\*probably won't show up properly on github*

### App title

