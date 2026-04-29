# paint.py

import pygame
import math
import sys
from datetime import datetime

from tools import *

# главная функция
def main():
#* создаются кнопки
#* создаётся палитра цветов
#* задаются стартовые настройки
#* запускается бесконечный цикл программы
#* обрабатываются мышка и клавиатура
#* рисуется экран
    # кнопки инструментов
    buttons = [
        Button(10, 10, 55, 20, "Pen", PEN),
        Button(70, 10, 55, 20, "Line", LINE),
        Button(130, 10, 55, 20, "Rect", RECT),
        Button(190, 10, 60, 20, "Circle", CIRCLE),
        Button(255, 10, 60, 20, "Erase", ERASER),

        Button(10, 35, 55, 20, "Fill", FILL),
        Button(70, 35, 55, 20, "Text", TEXT),
        Button(130, 35, 60, 20, "Square", SQUARE),
        Button(195, 35, 60, 20, "RTri", RTRI),
        Button(260, 35, 60, 20, "ETri", ETRI),
        Button(325, 35, 70, 20, "Rhomb", RHOMB),
        Button(500, 10, 35, 20, "S", "small"),
        Button(540, 10, 35, 20, "M", "medium"),
        Button(580, 10, 35, 20, "L", "large"),
        Button(500, 35, 80, 20, "Clear", "clear"),
    ]

    # квадраты палитры
    # варианты цветов справа сверху
    palette_rects = []
    for i in range(len(PALETTE)):
        x = 720 + i * 24
        y = 18
        palette_rects.append(pygame.Rect(x, y, 20, 20))

    # стартовые значения
    # по дефолту при открытии инструмент и цвет и размер
    tool = PEN
    color = BLACK
    size = 5

    drawing = False # для мышки при зажатии рисуетc x
    start = None
    preview = None

    # для текста
    text_on = False
    text_pos = (0, 0)
    text = ""

    while True:

        clock.tick(60)

        for event in pygame.event.get():

            # закрытие окна
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # клавиши
            if event.type == pygame.KEYDOWN:

                # размеры
                if event.key == pygame.K_1:
                    size = 2
                if event.key == pygame.K_2:
                    size = 5
                if event.key == pygame.K_3:
                    size = 10

                # сохранить ctrl+s
                if event.key == pygame.K_s:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        name = datetime.now().strftime("%Y%m%d_%H%M%S")
                        pygame.image.save(canvas, "paint_" + name + ".png")

                # ввод текста
                if tool == TEXT and text_on:

                    if event.key == pygame.K_RETURN:# ентер вставляет 
                        img = font.render(text, True, color)
                        canvas.blit(img, text_pos)
                        text = ""
                        text_on = False

                    elif event.key == pygame.K_BACKSPACE: #удаляет послед элемент
                        text = text[:-1]

                    elif event.key == pygame.K_ESCAPE:# отменяет ввод
                        text = ""
                        text_on = False

                    else:
                        text += event.unicode

            # нажали мышку
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1: # нажата левая

                    x, y = event.pos

                    # если верхняя панель
                    if y < TOOLBAR_H:# т. е. ниже 64 это в панелях 

                        # инструменты
                        for b in buttons:
                            if b.click((x, y)):

                                if b.tool == "small":
                                    size = 2

                                elif b.tool == "medium":
                                    size = 5

                                elif b.tool == "large":
                                    size = 10

                                elif b.tool == "clear":
                                    canvas.fill(WHITE) # зливка на весь экран белым

                                else:
                                    tool = b.tool

                        # цвета
                        for i in range(len(palette_rects)):
                            if palette_rects[i].collidepoint(x, y):
                                color = PALETTE[i]

                    else:
                        # холст
                        cx, cy = to_canvas(x, y)

                        if tool == FILL: # если инструмент заливка то заливка
                            flood_fill(canvas, (cx, cy), color)

                        elif tool == TEXT:
                            text_on = True
                            text = ""
                            text_pos = (cx, cy)

                        else:
                            drawing = True
                            start = (cx, cy)

            # отпустили мышку
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1 and drawing:

                    end = to_canvas(*event.pos)

                    draw_shape(canvas, tool, color, size, start, end)

                    drawing = False
                    preview = None

            # движение мышки
            if event.type == pygame.MOUSEMOTION:

                if drawing:

                    cx, cy = to_canvas(*event.pos)

                    # карандаш
                    if tool == PEN:
                        pygame.draw.circle(canvas, color, (cx, cy), size)

                    # ластик
                    elif tool == ERASER:
                        pygame.draw.circle(canvas, WHITE, (cx, cy), size * 2)

                    # превью фигур # то есть дает предварительную фотку пока не отпустишь
                    else:
                        preview = canvas.copy()
                        draw_shape(preview, tool, color, size, start, (cx, cy))

        # экран
        screen.fill(DARK)

        # показать холст
        show = preview if preview else canvas
        screen.blit(show, (0, TOOLBAR_H))

        # временный текст # пока вводишь текст выходит |
        if text_on:
            img = font.render(text + "|", True, color)
            screen.blit(img, (text_pos[0], text_pos[1] + TOOLBAR_H))

        # панель
        draw_toolbar(screen, buttons, tool, color, size, palette_rects)

        pygame.display.flip()


# рисуем фигуры
def draw_shape(win, tool, color, size, sp, ep):

    x1, y1 = sp
    x2, y2 = ep

    # линия
    if tool == LINE:
        pygame.draw.line(win, color, sp, ep, size)

    # прямоугольник
    elif tool == RECT:
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(win, color, rect, size)

    # круг
    elif tool == CIRCLE:
        r = int(math.hypot(x2-x1, y2-y1))
        pygame.draw.circle(win, color, sp, r, size)

    # квадрат
    elif tool == SQUARE:
        side = min(abs(x2-x1), abs(y2-y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(win, color, rect, size)

    # прямоугольный треугольник
    elif tool == RTRI:
        pts = [(x1,y1), (x2,y1), (x2,y2)]
        pygame.draw.polygon(win, color, pts, size)

    # равносторонний
    elif tool == ETRI:
        pts = [(x1,y2), (x2,y2), ((x1+x2)//2, y1)]
        pygame.draw.polygon(win, color, pts, size)

    # ромб
    elif tool == RHOMB:
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
        pygame.draw.polygon(win, color, pts, size)


# запуск
main()