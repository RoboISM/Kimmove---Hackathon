import pygame
import os
import sys
import shutil
import subprocess
import pyautogui
import serial
import time

is_navMode , is_gameMode = False, False


pygame.init()

display_width = 400
display_height = 200

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Mode Select")

smallfont = pygame.font.SysFont("tahoma", 25)
medfont = pygame.font.SysFont("tahoma", 50)
largefont = pygame.font.SysFont("tahoma", 85)


def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def close_action():
    os.system('TASKKILL /F /IM OpenCV.exe')
    os.system('TASKKILL /F /IM OpenCV2.exe')

def Gaming():
    global is_gameMode, is_navMode
    if is_navMode:
        os.system('TASKKILL /F /IM OpenCV2.exe')
        is_navMode = False
                
    pid = subprocess.Popen('"OpenCV.exe"')
    is_gameMode = True

def Navigation():
    global is_gameMode, is_navMode
    if is_gameMode:     
        os.system('TASKKILL /F /IM OpenCV.exe')
        is_gameMode = False
                
    pid1 = subprocess.Popen('"OpenCV2.exe"')
    is_navMode = True
    
def Toggle():
    print ("Toggle Begin!")
    global is_gameMode, is_navMode
    if is_gameMode:     
        os.system('TASKKILL /F /IM OpenCV.exe')
        is_gameMode = False
        time.sleep(1)        
        pid1 = subprocess.Popen('"OpenCV2.exe"')    
        is_navMode = True
        
    elif is_navMode:
        os.system('TASKKILL /F /IM OpenCV2.exe')
        is_navMode = False
        time.sleep(1)
       # print("Task Killed")
        pid1 = subprocess.Popen('"OpenCV.exe"')    
        is_gameMode = True
     #   print ("Opened New")
        

def button(text, x, y, width, height, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay,(255,255,255), (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "Close":
                print ("closing call")
                close_action()

            if action == "Gaming":
                print ("gaming call")
                Gaming()

            if action == "Navigation":
                print ("Navigation call")
                Navigation()

            if action == "Toggle":
                Toggle()
    else:
        pygame.draw.rect(gameDisplay,(127,127,127), (x,y,width,height))

    black = (0,0,0)        
    text_to_button(text,black,x,y,width,height)

def comm(inp, ser):
    print inp

    if "RELOAD" in inp:
        pyautogui.press('R')
        inp =  ser.readline()
        while "RELOAD" in inp:
           inp =  ser.readline()
           pyautogui.press('R')
        print "R"

    elif "LR" in inp:
        pyautogui.mouseDown(button='left')
        pyautogui.mouseDown(button='right')
        inp =  ser.readline()
        while "LR" in inp:
            inp =  ser.readline()

        pyautogui.mouseUp(button='left')
        pyautogui.mouseUp(button='right')
        
    elif "LEFT" in inp:
        pyautogui.mouseDown(button='left')

        inp =  ser.readline()
        while "LEFT" in inp:
            inp =  ser.readline()
        pyautogui.mouseUp(button='left')

    elif "RIGHT" in inp:
        pyautogui.mouseDown(button='right')

        inp =  ser.readline()
        while "RIGHT" in inp:
            inp =  ser.readline()

        pyautogui.mouseUp(button='right')

    elif "TOGGLE" in inp:
           inp =  ser.readline()
           #close_action()
           Toggle()
           
    elif "CLOSE" in inp:
           inp =  ser.readline()
           close_action()
           #Toggle()
            
    else:
        inp =  ser.readline()
    
    return inp

def getPort(lower=1):
    
    ports = ["COM"]*(101-lower)
    for i in xrange(lower,100):
        ports[i-lower]+=str(i)
        
    print ("Ports to be tested:",ports)

    for port in ports:
        print ("checking PORT:",port)
        try:
            ser = serial.Serial(port,9600,timeout=2)
            inp = ser.readline()
            print (inp)
            
            if not len(inp):
                ser.close()
                pass
            else:
                return ser
                
        except:
            pass

        
    print "No port found"
    return ser

def loop():
    try:
        print "Trying to connect..."
        ser = getPort(1)
        print "Connection Established!"
    except:
        print "Connection Refused!"
        
    #ser = serial.Serial('COM86', 9600)
    inp = ser.readline()
     
    while 1:
        inp = comm(inp, ser)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        white = (168,168,168)
        gameDisplay.fill(white)
        button("Gaming", 35,25,130,35, action="Gaming")
        button("Navigation", 35,85,130,35, action="Navigation")
        button("Toggle", 35,145,130,35, action="Toggle")
        button("Close", 300,45,75,35, action="Close")

        pygame.display.update()

if __name__ == '__main__':
    loop()
