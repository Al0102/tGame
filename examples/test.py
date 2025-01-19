import sys, os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
import tGame
import KEY, CONTROLS
from Entity import Player, Creature
from Menu import OptionScreen

def game_quit(menu="Game"):
    sys.exit("Game quit from " + menu)
if __name__ == "__main__":
  # collision
  # list1 = [Player(x=i) for i in range(5)]
  # foo = 1
  # checkCollide = lambda x: True if x.x_pos == foo else False
  # list2 = list(map(checkCollide, list1))
  # print([p.x_pos for p in list1])
  # print(list2)
  
    try:
        tGame.init()
        tGame.setTitle("tGame test dungeon")
        tGame.screenClear()
        tGame.renderCopy()
    
        key_input = tGame.KeyboardInput()
    
        enemy_group = []
    
        def mob_factory():
            return Creature(10,1, x=random.randint(1,60), y=random.randint(1,25), rect=(4,4), image=tGame.import_image("sprites/test.txt", height=4).split('\n'),  group=enemy_group)

        def respawn_mob():
            global mob
            mob = mob_factory()
            return KEY.QUIT

        entity = Player(enemy_group)
        mob = mob_factory()
    
        entity.enemies.append(mob)

        def update_screen():
            global options_menu
            window_size = os.get_terminal_size()
            display_centered = ((window_size[0]-len(max(options_menu.choices.keys(), key=len)))//2,
                            window_size[1]//len(options_menu.choices))
            options_menu.keypad.format(x=display_centered[0],y=display_centered[1])
            return KEY.QUIT

        options_menu = OptionScreen(["abc", "spawn", "update resolution", "quit"],
                                    [lambda: KEY.QUIT, respawn_mob, update_screen, game_quit])

    
        tGame.hideCursor()
        tGame.screenClear()
        tGame.renderCopy()

        # Intro menu
        if options_menu.open_menu(key_input) == 0:
            sys.exit("Game quit from choice menu")
        tGame.screenClear()
    
        # Main app
        can_press = True
        while True:
            if can_press:
                key_input.keyIn()
                can_press = False
            else:
                can_press = True
                continue
            if key_input.pressed == KEY.QUIT:
                sys.exit("Game quit from in-game")
            elif key_input.pressed == CONTROLS.ESCAPE:
                options_menu.open_menu(key_input)
                tGame.screenClear()

            for mo in enemy_group:
                mo.update()
            entity.update(key_input.pressed)
            tGame.render("\033[1;1H")
            tGame.moveCursor('B')
            tGame.moveCursor('D', 1000)
            tGame.render(str(key_input.pressed))
            tGame.render("\033[100;100H")
            tGame.renderCopy()
        tGame.showCursor()

    finally:
        if tGame.POSIX:
            import termios
            termios.tcsetattr(tGame.fd,termios.TCSADRAIN, tGame.old_settings)
        print("\033[10B")
