import pygame, sys
from math import *

RED=(255,0,0)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hello World")


i=100
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
    pygame.draw.circle(screen,RED,(100,floor(i)),20)
    i+=0.01
    pygame.display.update() 