import sys
from time import sleep
import KEY, CONTROLS
from events import Collide
import tGame


class Entity:
  TYPE = "Entity"
  def __init__(self, x=1, y=1, rect=(1,1), image=None, group=None):
    self.group = group
    if group != None:
      self.group.append(self)
    
    self.image = image
    self.rect = rect
    self.midpoint = [dim//2+1 for dim in self.rect]
    
    self.speed = 1
    self.can_move = False
    
# --- top left if image is larger than 1x1 unit
    self.prev_x_pos = self.x_pos = x
    self.prev_y_pos = self.y_pos = y
# ---
    self.direction = CONTROLS.RIGHT #default random direction

  def kill(self):
    self.clearImage()
    if self.group:
      self.group.pop(self.group.index(self))
      
  def move(self, direction:int, redraw=True):
    if self.can_move == False:
      return
    if direction in (CONTROLS.RIGHT, CONTROLS.LEFT, CONTROLS.UP, CONTROLS.DOWN):
      self.direction = direction
      self.prev_x_pos = self.x_pos
      self.prev_y_pos = self.y_pos
      speed = round(self.speed)
      if direction == CONTROLS.UP:
        self.y_pos -= speed
      elif direction == CONTROLS.DOWN:
        self.y_pos += speed
      elif direction == CONTROLS.RIGHT:
        self.x_pos += speed
      elif direction == CONTROLS.LEFT:
        self.x_pos -= speed
      if redraw:
        self.draw()

  def collide(self, entities:"Entity"):
    for entity in entities:
      if self.x_pos == entity.x_pos+entity.rect[0]-1:
        if any(
          [entity.y_pos <= i < entity.y_pos+entity.rect[1] for i in range(self.y_pos, self.y_pos+self.rect[1])]
        ):
          return Collide(entity, CONTROLS.LEFT)
      elif entity.x_pos == self.x_pos+self.rect[0]-1:
        if any(
          [entity.y_pos <= i < entity.y_pos+entity.rect[1] for i in range(self.y_pos, self.y_pos+self.rect[1])]
        ):
          return Collide(entity, CONTROLS.RIGHT)
      elif self.y_pos == entity.y_pos+entity.rect[1]-1:
        if any(
          [entity.x_pos <= i < entity.x_pos+entity.rect[0] for i in range(self.x_pos, self.x_pos+self.rect[0])]
        ):
          return Collide(entity, CONTROLS.UP)
      elif entity.y_pos == self.y_pos+self.rect[1]-1:
        if any(
          [entity.x_pos <= i < entity.x_pos+entity.rect[0] for i in range(self.x_pos, self.x_pos+self.rect[0])]
        ):
          return Collide(entity, CONTROLS.DOWN)
    return 0
    
  def draw(self):
    self.clearImage()
    for i in range(self.rect[1]):
      tGame.render("\033["+str(self.y_pos+i)+';'+str(self.x_pos)+'H'+self.image[i])
    tGame.renderCopy()

  def clearImage(self):
    for i in range(self.rect[1]):
      for j in range(self.rect[0]):
        tGame.render("\033["+str(self.prev_y_pos+i)+';'+str(self.prev_x_pos+j)+'H'+' ')
  
  def update(self):
    pass


class Creature(Entity):
  TYPE = "Creature"
  def __init__(self, hp, energy, bag_slots=9, x=0, y=0, rect=(1,1), image="%", group=None, enemies=[]):
    super().__init__(x=x, y=y, rect=rect, image=image, group=group)
    self.hp = self.max_hp = hp
    self.energy = self.max_energy = energy
    self.bag_slots = bag_slots
    self.enemies = enemies

    self.can_move = True

    self.punch = Attack(1, 1, self.enemies) # damage and range are arbitrary numbers for testing
  
  def attack(self, attack=None):
    if not attack:
        attack = self.punch
    if self.direction == CONTROLS.UP:
      y = self.y_pos-1
      x = self.x_pos+self.midpoint[0]-1
    elif self.direction == CONTROLS.DOWN:
      y = self.y_pos+self.rect[1]
      x = self.x_pos+self.midpoint[0]-1
    elif self.direction == CONTROLS.LEFT:
      y = self.y_pos+self.midpoint[1]-1
      x = self.x_pos-1
    elif self.direction == CONTROLS.RIGHT:
      y = self.y_pos+self.midpoint[1]-1
      x = self.x_pos+self.rect[0]
    else:
      tGame.render("\033[10;10H")
      tGame.render(str(x)+' '+ str(y))
    attack.update(x,y,self.direction)

  def collide(self):
    collision = super().collide(self.enemies)
    if collision == 0:
      return
    if collision.target_collide.TYPE == "Creature":
      self.x_pos = self.prev_x_pos
      self.y_pos = self.prev_y_pos
      self.draw()
      collision.target_collide.draw()
      
  def update(self):
    super().update()
    if self.hp <= 0:
      tGame.render("\033[1;1H")
      tGame.render(str("dead"))
      tGame.render("\033[100;100H")
      self.kill()
      return
    self.draw()


class Player(Creature):
  TYPE = "Player"
  def __init__(self, enemies, group=[], x=0, y=0):
    super().__init__(15, 10, x=x, y=y, rect=(3,3), image=(" o ","-|-","/ \\"), group=group, enemies=enemies)
    self.gun = Attack(10, 5, self.enemies, image='.')

  def attack(self, key_in):
    if key_in != CONTROLS.ACTION:
      return
    super().attack(self.gun)
  
  def update(self, key):
    super().update()
    self.move(key)
    super().collide()
    self.attack(key)


class Attack(Entity):
  def __init__(self, damage, range_, targets, obstacles=[], rect=(1,1), image=" "):
    super().__init__(rect=rect, image=image)
    self.can_move = True
    self.damage = damage
    self.range = range_
    self.targets = targets
    self.obstacles = obstacles

  def update(self, x, y, direction):
    self.x_pos = x
    self.y_pos = y
    self.direction = direction
    
    for _ in range(self.range):
      check_collide = self.collide(self.targets)
      if check_collide:
        check_collide.target_collide.hp -= self.damage
        tGame.render("\033["+str(check_collide.target_collide.y_pos)+';'+str(check_collide.target_collide.x_pos)+"H"+"\033[31m")
        tGame.renderCopy()
        check_collide.target_collide.draw()
        tGame.render("\033[0m")
        break
      sleep(0.2)
      self.draw()
      self.move(self.direction, redraw=False)
    self.clearImage()

