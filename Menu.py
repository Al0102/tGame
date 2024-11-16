import sys, os
import KEY, CONTROLS
import tGame

class OptionScreen:
  
  def __init__(self, choices):
    self.choices = choices
    self.index = 0
    self.num_choices = len(choices)

  def open_menu(self):
    tGame.render("\033[2J\033[;H")
    tGame.render("\033[0m")
    tGame.render("\033[1;1H") # tGame.moveCursor cursor to top
    for i in range(self.num_choices):
      tGame.moveCursor("D", 1000)
      tGame.moveCursor("B", 1)
      tGame.render(self.choices[i]) # print option
    # go to line 1, the number should be changed if there are lines prior to options
    tGame.moveCursor("D", 1000) # Move all the way left
    tGame.render("\033["+str(self.index+1)+"H") # tGame.moveCursor to self.index
    tGame.render("\033[1;32m" + self.choices[self.index]) # change selected to green
    tGame.render("\033["+str(self.num_choices+1)+"H")
    tGame.renderCopy()
    
  def run(self, key_input):
    if key_input == -1:
      return None
      
    tGame.render("\033["+str(self.index+1)+"H")
    tGame.moveCursor("D", 1000) # Move all the way left
    tGame.render("\033[0m" + self.choices[self.index]) # change previous to white
    sys.stdout.flush()

    if key_input == CONTROLS.ACTION:
      return self.choices[self.index]
    
    if key_input == CONTROLS.UP:
      if self.index > 0:
        self.index -= 1
      else:
        self.index = self.num_choices-1
    elif key_input == CONTROLS.DOWN:
      if self.index < self.num_choices-1:
        self.index += 1
      else:
        self.index = 0
  
    tGame.moveCursor("D", 1000) # Move all the way left
    tGame.render("\033["+str(self.index+1)+"H") # tGame.moveCursor to self.index
    tGame.render("\033[1;32m" + self.choices[self.index]) # change selected to green
    
    return None
