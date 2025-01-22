'''
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
 '''
import tGame
import KEY, CONTROLS

tGame.init()
key = tGame.KeyboardInput()
while key.keyIn() != KEY.K_A:
    if key.pressed == CONTROLS.DOWN:
        tGame.setCursor(2, 2)
        tGame.renderCopy()
    if key.pressed == CONTROLS.UP:
        tGame.moveCursor('B', 2)

tGame.end()
