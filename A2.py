import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w, h = 500, 800
flag = True
freeze = False
game_over = False
cheat_mode = False
flag = True
count = 0
dictionary = {}
class Diamond:
    def __init__(self):
        self.x = random.randint(-200, 200)
        self.y = 350
        self.size = 10
        self.speed = 100
        self.iteration = 0
        self.color = [random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5]
    
    def reset(self):
        self.x = random.randint(-200, 200)
        self.y = 350
        self.color = [random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5]

class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]
        self.speed = 300  

#---------------------------------------------- Mid-Point Line Drawing Algorithm
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # Determine the zone
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    # Convert to zone 0
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    # calculate initial decision parameter
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy )-2*( dx)

    # plot initial point
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)

    # iterate over x coordinates
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        # Convert back from zone 0
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)
#---------------------------------------------- End of Mid-Point Line Drawing Algorithm
diamond = Diamond()
catcher = Catcher()

def draw_diamond():
    global diamond
    glPointSize(2)

    glColor3f(diamond.color[0], diamond.color[1], diamond.color[2])
    midpoint_line(int(diamond.x + 5), int(diamond.y), int(diamond.x), int(diamond.y + 10))
    midpoint_line(int(diamond.x + 5), int(diamond.y), int(diamond.x), int(diamond.y - 10))
    midpoint_line(int(diamond.x - 5), int(diamond.y), int(diamond.x), int(diamond.y + 10))
    midpoint_line(int(diamond.x - 5), int(diamond.y), int(diamond.x), int(diamond.y - 10))

def draw_ui():
    global catcher

    # Catcher
    glPointSize(2)
    glColor3f(catcher.color[0], catcher.color[1], catcher.color[2])
    midpoint_line(int(catcher.x + 70), -365, int(catcher.x - 70), -365)
    midpoint_line(int(catcher.x + 60), -385, int(catcher.x + 70), -365)
    midpoint_line(int(catcher.x + 60), -385, int(catcher.x - 60), -385)
    midpoint_line(int(catcher.x - 60), -385, int(catcher.x - 70), -365)

    # Left restart button (bright teal)
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    # Right Cross Button (red)
    glPointSize(3)
    glColor3f(0.9, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    # Middle Pause/Play Button (amber)
    glPointSize(4)
    glColor3f(1, 0.5, 0)
    if freeze:
        # Play icon (triangle)
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        # Pause icon (two bars)
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

def convert_coordinate(x, y):
    global w, h
    a = x - (w / 2)
    b = (h / 2) - y
    return a, b

def keyboardListener(key, x, y):
    global freeze, cheat_mode
    if key == b' ':
        freeze = not freeze
    elif key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        print(f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global catcher, freeze, game_over, cheat_mode
    if not cheat_mode and not freeze and not game_over:
        if key == GLUT_KEY_RIGHT:
            if catcher.x < 180:
                catcher.x += 10
        if key == GLUT_KEY_LEFT:
            if catcher.x > -180:
                catcher.x -= 10
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global freeze, diamond, game_over, catcher, cheat_mode
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        
        # Left restart button
        if -209 < c_x < -170 and 325 < c_y < 375:
            print('Starting Over')
            catcher.color = (1, 1, 1)
            diamond.reset()
            game_over = False
            freeze = False
            cheat_mode = False
            diamond.iteration = 0
        
        # Right close button
        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', diamond.iteration)
            glutLeaveMainLoop()
        
        # Middle pause/play button
        if -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze
            print("Game Paused" if freeze else "Game Resumed")
    
    glutPostRedisplay()

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)  # Color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    

    glMatrixMode(GL_MODELVIEW)
    
    # Initialize the matrix
    glLoadIdentity()
    
    gluLookAt(0, 0, 314, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    
    draw_ui()
    if not game_over:
        draw_diamond()
    
    glutSwapBuffers()

def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global freeze, diamond, catcher, game_over, cheat_mode
    
    if not freeze and not game_over:
        # Update diamond position
        diamond.y -= (100 + diamond.iteration * 10) * delta_time
        
        # Cheat mode: automatically move catcher towards diamond
        if cheat_mode:
            if catcher.x < diamond.x:
                catcher.x += catcher.speed * delta_time
                if catcher.x > diamond.x:
                    catcher.x = diamond.x
            elif catcher.x > diamond.x:
                catcher.x -= catcher.speed * delta_time
                if catcher.x < diamond.x:
                    catcher.x = diamond.x
            
            # Keep catcher in bounds
            if catcher.x < -180:
                catcher.x = -180
            elif catcher.x > 180:
                catcher.x = 180
        
        # Check collision (diamond caught)
        if diamond.y <= -365 and catcher.x - 75 <= diamond.x <= catcher.x + 75:
            diamond.reset()
            diamond.iteration += 1
            print("Score:", diamond.iteration)
        
        # Check if diamond missed (game over)
        if diamond.y < -400:
            catcher.color = (1, 0, 0)
            print("Game Over! Score:", diamond.iteration)
            game_over = True
            freeze = True
    
    time.sleep(1 / 60)
    glutPostRedisplay()

def init():
    # Clear the screen
    glClearColor(0, 0, 0, 0)
    
    # Load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    
    # Initialize the matrix
    glLoadIdentity()
    
    # Give PERSPECTIVE parameters
    gluPerspective(104, (500 / 800), 1, 1000.0)
    # Aspect ratio that determines the field of view in the X direction (horizontally)
    # Near distance
    # Far distance

glutInit()
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Depth, Double buffer, RGB color

wind = glutCreateWindow(b"Catch the Diamonds!")
init()

glutDisplayFunc(display)  # display callback function
glutIdleFunc(animate)  # what you want to do in the idle time (when no drawing is occurring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

print("=== Catch the Diamonds Game ===")
print("Controls:")
print("  Left/Right Arrow Keys - Move catcher")
print("  C - Toggle cheat mode")
print("  Left Button (Teal Arrow) - Restart game")
print("  Middle Button (Amber) - Play/Pause")
print("  Right Button (Red X) - Exit game")
print("\nStarting game...")

glutMainLoop()  # The main loop of OpenGL