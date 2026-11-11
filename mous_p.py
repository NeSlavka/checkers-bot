import pyautogui
from pynput import keyboard
import time
from PIL import ImageGrab
from test import is_color_similar
import random

interval = 50

x_ = (680, 730, 780, 830, 880, 930, 980, 1030)
y_ = (705, 655, 605, 555, 505, 455, 405, 355)

where_can = []
can = []
where_byts_can = []
byts_can = []

white = 232, 230, 217
dark = 95, 95, 94

# white = 95, 95, 94
# dark = 232, 230, 217

moves = 0
last_m = 0, 0

number = 0

ate = False

# def wd(a, b, c=dark):
#     global x_, y_, dark, white
    
#     # Проверка, чтобы не вылететь за пределы доски
#     if a < 0 or a > 7 or b < 0 or b > 7:
#         return False 

#     if c == 'all':
#         return not is_color_similar(get_pixel_color(x_[a], y_[b]), dark, tolerance_percent=5) and not is_color_similar(get_pixel_color(x_[a], y_[b]), white, tolerance_percent=5)
        
#     return is_color_similar(get_pixel_color(x_[a], y_[b]), c, tolerance_percent=5)

def wd(a, b, c=dark):
    if a < 0 or a > 7 or b < 0 or b > 7:
        return False
    
    if c == 'all':
        return is_color_similar(get_pixel_color(x_[a], y_[b]), dark) or is_color_similar(get_pixel_color(x_[a], y_[b]), white)
    return is_color_similar(get_pixel_color(x_[a], y_[b]), c)

def get_pixel_color(x, y):
    bbox = (x, y, x + 1, y + 1)
    img = ImageGrab.grab(bbox=bbox)
    return img.getpixel((0, 0))

def pc(X, Y, X2, Y2):
    pyautogui.click(x=x_[X], y=y_[Y])
    pyautogui.click(x=x_[X2], y=y_[Y2])

def pc_start(X, Y):
    global last_m, moves
    if random.randint(0, 1) == 1:
        pc(X, Y, X+1, Y-1)
        last_m = X+1, Y-1
        return True
    else:
        pc(X, Y, X-1, Y-1)
        last_m = X-1, Y-1
        return True
    
def start():
    global number
    number = random.randint(1, 4)
    

    if number ==  1:
        pc_start(1, 5)
    elif number == 2:
        pc_start(3, 5)
    elif number == 3:
        pc_start(5, 5)
    elif number == 4:
        pc(7, 5, 6, 4)
        last_m = 6, 4

def eat():
    global ate

    ate = False
    for Y in range(8):
        for X in range(8):
            if wd(X, Y, dark):

                if X - 2 >= 0 and Y - 2 >= 0: # не вылетим за край
                    if wd(X-1, Y-1, white) and not wd(X-2, Y-2, "all"):
                        pc(X, Y, X-2, Y-2)
                        print(f'Кушаю на {X-2}, {Y-2}')
                        ate = True
                        break
                    elif wd(X+1, Y+1, white) and not wd(X+2, Y+2, 'all'):
                        pc(X, Y, X-2, Y+2)
                        ate = True
                        break

                elif X + 2 != 9 and Y - 2 != -1: # не вылетим за край
                    if wd(X+1, Y-1, white) and not wd(X+2, Y-2, "all"):
                        pc(X, Y, X+2, Y-2)
                        ate = True
                        print(f'Кушаю на {X+2}, {Y-2}')
                        break
                    elif wd(X+1, Y+1, white) and not wd(X+2, Y+2, "all"):
                        pc(X, Y, X+2, Y+2)
                        ate = True
                        break


def d_can():
    global can, where_can, byts_can, where_byts_can

    can.clear()
    where_can.clear()
    byts_can.clear()
    where_byts_can.clear()

    for Y in range(8):
        for X in range(8):
            if wd(X, Y, dark):
                if X - 1 >= 0 and Y - 1 >= 0:
                    if wd(X-1, Y-1, "all"):
                        pass
                    else:
                        where_can.append((X, Y))
                        can.append((X-1, Y-1))

                        if not wd(X-2, Y-2, white) or wd(X+2, Y, dark):
                            where_byts_can.append((X, Y))
                            byts_can.append((X-1, Y-1))
                        

                if X + 1 <= 7 and Y - 1 >= 0:
                    if wd(X+1, Y-1, "all"):
                        pass
                    else:
                        where_can.append((X, Y))
                        can.append((X+1, Y-1))
                        if not wd(X+2, Y-2, white) or wd(X-2, Y, dark):
                            where_byts_can.append((X, Y))
                            byts_can.append((X+1, Y-1))
def carefully():
    global last_m
    global number
    global ate
    global can, where_can, byts_can, where_byts_can

    eat()

    if ate == False:
        d_can()
        
        # Защита от пустого списка
        if len(can) == 0:
            print("Ходов нет!")
            return
            
        if byts_can:
            idx = random.randrange(len(byts_can))
            end_pos = byts_can[idx]
            start_pos = where_byts_can[idx]
        else:
            idx = random.randrange(len(can)) 
            end_pos = can[idx]
            start_pos = where_can[idx]
        
        print(f"Ход: {start_pos} -> {end_pos}")

        print(where_can)
        print(can)
        print()
        print(where_byts_can)
        print(byts_can)
        
        pc(start_pos[0], start_pos[1], end_pos[0], end_pos[1])  

def move():
    global moves


    if moves == 0:
        start()
    elif moves <= 100:
        carefully()
    else:
        print("я хз братан")

    moves += 1 

def on_press(key):
    try:
        # Проверяем, что нажата именно клавиша "Пробел"
        if key == keyboard.Key.space:
            move()
    except AttributeError: 
        pass
# Запускаем прослушивание клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()