import sys, os
import KEY, CONTROLS


def init():
    global render_buffer, POSIX, WINDOWS

    # Posix systems  - i.e mac/linux
    if os.name == "posix":
        global tty, termios
        import tty, termios

        global fd, old_settings

        fd = sys.stdin.fileno()
        old_settings =  termios.tcgetattr(fd)

        WINDOWS = False
        POSIX = True

    else:
        global msvcrt
        import msvcrt
        WINDOWS = True
        POSIX = False

    render_buffer = ""

    render("\033[7h")
    renderCopy()

def end():
    if POSIX:
        import termios
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)


def clearRenderBuffer():
    global render_buffer
    render_buffer = ""

def render(*commands):
    global render_buffer
    for command in commands:
        render_buffer += command

def renderCopy():
    global render_buffer
    sys.stdout.write(render_buffer)
    sys.stdout.flush()
    clearRenderBuffer()


def moveCursor(direction: str, amount=1):
    """
    direction:
      'A' - UP
      'B' - DOWN
      'C' - FORWARD
      'D' - BACK
    """
    if direction not in "ABCD" or len(direction)>1:
        raise Exception("Invalid Move Cursor Direction")
    render("\033["+str(amount)+direction)

def setCursor(x: int, y: int):
    render(f"\033[{y};{x}H")

def hideCursor():
    render("\033[?25l")

def showCursor():
    render("\033[?25h")


def screenClear():
    render("\033[2J")

def setTitle(title):
    render("\033]0;"+title+"\x07")


'''
import_image(file, height, start, do_colour)
    Imports the image from a text file
    
    return (string)
      - Returns "ascii image" from text file as a string
     
    Parameters:
        file (string)
          - File path of text file holding the ascii image
          - e.g. "foo.txt"
        height (int)
          - Height of ascii image (number of lines in file)
        start (int)
          - default: 1
          - The first line in file to start taking in input
        do_colour (bool)
          - default: False
          - If set to True, uses the next {height} lines
            after the ascii image in the file as the "bitmap"
            argument when it calls: merge_ascii_colourmap()
    
'''
def import_image(file, height, start=1, do_colour=False):
    start=start-1
    with open (file, 'r', encoding='utf-8') as f:
        file = f.readlines()
        img = ''.join(file[start:start+height])
        if do_colour:
            colourmap = ''.join(file[start+height:start+2*height])
            return merge_ascii_colourmap(img, colourmap)
        else:
            img = '\033[0m'+img
        return img

'''
merge_ascii_colourmap(image, bitmap)
    Combines an ASCII image with its corresponding colourmap
    
    return (string)
      - Returns a new ascii image
        with the corresponding ANSI escape codes inserted
      - newlines (\n) used to separate lines 

    Parameters:
        image (string or 2D list)
          - The ascii image
        bitmap (bitmap style string of digits 0-9 or spaces)
          - Map of colours corresponding to the ascii image
            0 - Black
            1 - Red
            2 - Green
            3 - Yellow
            4 - Blue
            5 - Magenta
            6 - Cyan
            7 - White
            8 - Grey (faint white)
            9 - Bold white
'''
def merge_ascii_colourmap(image, bitmap):
    if type(image) == str:
        new_image = list(map(list, image.split('\n')))
    else:
        new_image = image[:]
    if type(bitmap) == str:
        bitmap_f = bitmap.split('\n')

    for line in range(len(bitmap_f)):
        temp_line = bitmap_f[line]

        while len(temp_line) > 0:
            temp_char = chr(temp_line[-1])
            if temp_char == '8':
                colour_value = '2'
            elif temp_char == '9':
                colour_value = '1'
            else:
                colour_value = '3'+temp_char

            temp_line = temp_line.rstrip(temp_char)
            new_image[line].insert(
                    len(temp_line),
                        f"\033[0m\033[{colour_value}m")
        new_image[line].append("\033[0m")

    new_image = '\n'.join(map(lambda x: ''.join(x), new_image))
    return new_image


class KeyboardInput:
    def __init__(self):
        self.pressed = 0
        self.key_mash_counter = 0
        self.max_control_code_mash = 5

        if POSIX:
            tty.setraw(fd)

        # Control codes for POSIX/WINDOWS
        # UP DOWN RIGHT LEFT
            CONTROL_CODES = tuple(range(65,69), 3)
        else:
            CONTROL_CODES = (72, 80, 77, 75, b'\x03')
        self.CONTROL_MAP = dict(zip(
            CONTROL_CODES, (
                CONTROLS.UP,
                CONTROLS.DOWN,
                CONTROLS.RIGHT,
                CONTROLS.LEFT,
                KEY.QUIT)))

    def _scan_in_control_codes(self, char):
        if char in self.CONTROL_MAP:
            return self.CONTROL_MAP[char]
        self.key_mash_counter += 1
        return KEY.QUIT if self.key_mash_counter > self.max_control_code_mash else 0
        # Uncomment if you want to raise error for control codes that are not coded in yet
        # raise ValueError(f'Invalid control code: {char}')
        
    def keyIn(self):
        if POSIX:
            # Reads one chracter from input stream 
            char = ord(sys.stdin.read(1))
        else:
            # Gets keyboard input as UNICODE character
            # ord() converts to ascii
            key = msvcrt.getwch()
            char = ord(key)
# Test -             render('\033[1;1H')
# Test -             render(str(key))
# Test -         render('\033[2;1H' + str(char))

        # ASCII (a - ~)
        if 32 <= char <= 126:
            self.pressed = char
            self.key_mash_counter = 0

        # Backspace
        elif char == 8:
# Test -             render("\033[3;5H Backspace")
            self.pressed = KEY.BACKSPACE
            self.key_mash_counter = 0
        # Tab
        elif char == 9:
# Test -             render("\033[3;5H TAB")
            self.pressed = KEY.TAB
            self.key_mash_counter = 0
        # ENTER
        elif char in {10, 13}:
# Test -             render("\033[3;5H ENTER")
            self.pressed = KEY.ENTER
            self.key_mash_counter = 0
        # CTRL-C
        if char == 3:
            self.pressed = KEY.QUIT
            self.key_mash_counter = 0

        if POSIX:
            if char == 27:
                # Control codes
                next1 = ord(sys.stdin.read(1))
                if next1 == 91:
                    next2 = ord(sys.stdin.read(1))
# Test -                     render("\033[1;5H CONTROL")
                    self.pressed = self._scan_in_control_codes(next2)
                    if self.pressed != 0: self.key_mash_counter = 0
# Test -                     match self.pressed:
# Test -                         case CONTROLS.UP: 
# Test -                             render("^")
# Test -                         case CONTROLS.DOWN: 
# Test -                             render("v")
# Test -                         case CONTROLS.RIGHT: 
# Test -                             render(">")
# Test -                         case CONTROLS.LEFT: 
# Test -                             render("<")
# Test -                         case _:
# Test -                             render(str(char))
                else:
                    # ESCAPE - If no control codes are inputted,
                    #          ESC is being pressed
                    self.pressed = CONTROLS.ESCAPE
            return self.pressed

        # WINDOWS
        else:
            # Control codes
            if char == 0x00 or char == 0xE0:
                next_ = ord(msvcrt.getwch())
# Test -                 render("\033[2;5H CONTROL")
                self.pressed = self._scan_in_control_codes(next_)
                if self.pressed != 0: self.key_mash_counter = 0
# Test -                 match self.pressed:
# Test -                     case CONTROLS.UP: 
# Test -                         render("^")
# Test -                     case CONTROLS.DOWN: 
# Test -                         render("v")
# Test -                     case CONTROLS.RIGHT: 
# Test -                         render(">")
# Test -                     case CONTROLS.LEFT: 
# Test -                         render("<")
# Test -                     case _:
# Test -                         render(str(char))

            elif char == 27: #ESC
# Test -                 render("\033[3;5H ESCAPE")
                self.pressed = CONTROLS.ESCAPE
            return self.pressed

        self.pressed = KEY.QUIT

if __name__ == "__main__":
    try:
        init()
        
        keyboard = KeyboardInput()
        
        screenClear()
        for i in range(10000000):
            keyboard.keyIn()
            if keyboard.pressed == KEY.QUIT:
                break
            elif keyboard.pressed == CONTROLS.ESCAPE:
                 screenClear()
            render("\033[;H")
 
            renderCopy()

    finally:
        if POSIX:
            termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
    





