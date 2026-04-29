# tools.py

import pygame
import collections #используется для fill 

# запуск pygame
pygame.init() # все модули пайгейм

# размеры окна
SCREEN_W = 950
SCREEN_H = 680
TOOLBAR_H = 64   # верхняя панель

# основные цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
DARK = (30, 30, 40)
BLUE = (70, 130, 220)
GREEN = (60, 180, 100)

# палитра цветов
PALETTE = [
    (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),
    (255,255,0),(255,0,255),(0,255,255),(128,128,128)
]

# названия инструментов
PEN = "pen"
LINE = "line"
RECT = "rect"
CIRCLE = "circle"
ERASER = "eraser"
FILL = "fill"
TEXT = "text"
SQUARE = "square"
RTRI = "rtri"
ETRI = "etri"
RHOMB = "rhomb"

# создаем окно
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H)) #окно программы 950 на 680
pygame.display.set_caption("Paint") # кнопка сверху пэинт

# fps
clock = pygame.time.Clock() # для контроля фпс т. е. скок кадров в сек

# шрифт
font = pygame.font.SysFont("Arial", 16)  # используется для кнопок пен лайн и т. п. (их шрифт)

# холст
canvas = pygame.Surface((SCREEN_W, SCREEN_H - TOOLBAR_H)) # размер поверхности ниже панели
canvas.fill(WHITE) # фулл закрашивает в белый ниже панели


# класс кнопки
class Button:
    def __init__(self, x, y, w, h, text, tool): # создает кнопку и записывает ее свойства
        self.rect = pygame.Rect(x, y, w, h) # создает кнопку а рест хранит размеры и позицию кнопку
        self.text = text
        self.tool = tool 

    # рисуем кнопку
    def draw(self, win, active): # рисует кнопку на панели
        color = BLUE if active == self.tool else DARK # выбранная кнопка горит синей
        pygame.draw.rect(win, color, self.rect) # рисует тело кнопки
        pygame.draw.rect(win, GRAY, self.rect, 1) #рамка. серая

        txt = font.render(self.text, True, WHITE) # текст кнопки
        win.blit(txt, (self.rect.x + 5, self.rect.y + 3)) #blit() = вставить изображение на экран.

    # нажали или нет
    def click(self, pos):
        return self.rect.collidepoint(pos)


# перевод координат вниз панели
def to_canvas(x, y): # дает реальные координаты холста убирая панель
    return x, y - TOOLBAR_H


# заливка области
def flood_fill(surface, pos, new_color):

    x, y = pos
    w, h = surface.get_size() # размеры холста

    if not (0 <= x < w and 0 <= y < h): # если кликнули вне холста выйти
        return

    old = surface.get_at((x, y))[:3] # старый цвет :3 чтобы брал только rgb

    if old == new_color: # при заливке если там уже красный цвет то не нужно ниче делать
        return

    q = collections.deque() # Очередь точек и список посещённых пикселей
    q.append((x, y))
    used = set()

    while q:
        cx, cy = q.popleft() # пока есть точки для проверки

        if (cx, cy) in used: # если тут была проверка скип
            continue

        used.add((cx, cy)) # пометим что она уже проверенная

        if surface.get_at((cx, cy))[:3] == old:
            surface.set_at((cx, cy), new_color) # krasit

            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]: # sosedi sverhu snizy i t. d. 
                nx = cx + dx
                ny = cy + dy

                if 0 <= nx < w and 0 <= ny < h:
                    q.append((nx, ny))


# рисуем верхнюю панель
def draw_toolbar(win, buttons, tool, color, size, palette_rects):

    pygame.draw.rect(win, DARK, (0, 0, SCREEN_W, TOOLBAR_H)) # Рисует тёмную полоску сверху

    # кнопки инструментов
    for b in buttons:
        b.draw(win, tool) # рисует кнопки

    # текущий цвет
    pygame.draw.rect(win, color, (670, 18, 25, 25)) # маленький квадрат показывающий текущ цвет

    # размер кисти
    txt = font.render("Size: " + str(size), True, WHITE)
    win.blit(txt, (420, 20)) # кнопка показывающая размер

    # палитра
    for i in range(len(palette_rects)):
        pygame.draw.rect(win, PALETTE[i], palette_rects[i])
        pygame.draw.rect(win, BLACK, palette_rects[i], 1) # рамка за цвтеами черная