import numpy as np
import cv2 as cv
import win32gui
import time
import ctypes
from PIL import ImageGrab, Image

nome_janela = 'mumu'
desenhar_imagem = True
jogar_jogo = False
ver_imagem_tons_cinza = False
ver_imagem_kernel = False

## Posições onde serão feitos os recortes na janela ( estou utilizando a resolução de
x0 = 183 # Posição x inicial referente a janela 1
x1 = 797 # Posição x final referente a janela 1
x2 = 802 # Posicao x inicial referente a janela 2
x3 = 1416 # Posicao x final referente a janela 2
y0 = 135 # Posicao y inicial referente a janela 1,2
y1 = 630 # Posicao y inicial referente a janela 1,2



def click(x,y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

toplist, winlist = [], []

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

window = [(hwnd, title) for hwnd, title in winlist if nome_janela in title.lower()]


try:
    window = window[0]
    hwnd = window[0]
except:
    print ("Janela Não Encontrada")
    exit(0)


while True:
    time.sleep(1)
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    screenshot_game = ImageGrab.grab(bbox)
    screenshot_game = np.array(screenshot_game)
    screenshot_game = screenshot_game[:, :, ::-1].copy()

    img1 = screenshot_game[y0:y1, x0:x1]
    img2 = screenshot_game[y0:y1, x2:x3]

    imagem_subtraida = cv.absdiff(img1,img2)
    imagem_subtraida_em_cinza = cv.cvtColor(imagem_subtraida,cv.COLOR_BGR2GRAY)
    if (ver_imagem_tons_cinza):
        cv.imshow('Imagem subtraida em cinza',imagem_subtraida_em_cinza)
        cv.waitKey(10000)
    kernel = np.ones((4, 4), np.uint8)

    imagem_com_kernel = cv.erode(imagem_subtraida_em_cinza,kernel)
    if (ver_imagem_kernel):
        cv.imshow('Imagem com kernel aplicado',imagem_com_kernel)
        cv.waitKey(10000)
    imagem_com_threshold,mask = cv.threshold(imagem_com_kernel,10,255,cv.THRESH_BINARY)
    contornos, hierarquia = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for contorno in contornos:
        if (cv.contourArea(contorno) > 5 ):
            x, y, w, h = cv.boundingRect(contorno)
            middle_x = int(x + w / 2) + 183
            middle_y = int(y + h / 2) + 135
            if desenhar_imagem:
                cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if jogar_jogo:
                click(middle_x,middle_y)
                time.sleep(0.15)
    if desenhar_imagem:
        cv.imshow('Imagem com Erros Destacados',img2)
    cv.waitKey(0)
    click(557,351)




