import pygame as py
import random as rd
import math

class Disque:
    def __init__(self, vitesse, direction, d_confort, t_carac):
        """
        Initialise un disque avec les coordonnées aléatoires, la vitesse, la direction, la distance de confort et le temps caractéristique
        Paramètres:
        vitesse (float) : la vitesse du disque
        direction (float) : la direction du disque en degrés
        d_confort (float) : la distance de confort
        t_carac (float) : le temps caractéristique
        """
        self.x = rd.randint(0, 229)
        self.y = rd.randint(0, 489)
        self.vitesse = vitesse
        self.direction = direction
        self.d_confort = d_confort
        self.t_carac = t_carac
    

    def deplacer(self):
        direction_radians = math.radians(self.direction + rd.randint(160,200))
        self.x += self.vitesse * math.cos(direction_radians)
        self.y += self.vitesse * math.sin(direction_radians)
        self.direction += rd.uniform(-5,5)
        if self.direction < 0:
            self.direction += 360
        elif self.direction >= 360:
            self.direction -= 360

def gererCollision(disque, liste):
    for disk in liste:
        if disk != disque:
            distance = math.sqrt((disque.x - disk.x)**2 + (disque.y - disk.y)**2)
            if distance < 20:
                disque.vitesse = -disque.vitesse
                disk.vitesse = -disk.vitesse
    if disque.x - 10 <= 0 or disque.x + 10 >= 480 or (disque.x+10 >= 239 and disque.x-10 <= 261 and (disque.y-10 <= 221 or disque.y+10 >= 279)):
        disque.vitesse = -disque.vitesse
    if disque.y - 10 <= 0 or disque.y + 10 >= 480:
        disque.vitesse = -disque.vitesse

def afficherDisque(disque):
    print("Coordonnées : ", [disque.x, disque.y])
    print("Vitesse : ", disque.vitesse)
    print("Direction : ", disque.direction)
    print("Distance de confort : ", disque.d_confort)
    print("Temps caracteristique : ", disque.t_carac)

def listeDisque(n):
    list = []
    for i in range(0,n):
        list.append(Disque(3, rd.randint(0,360), rd.uniform(0.2, 2), 10))
    return list

disque1 = Disque(vitesse=5, direction=45, d_confort=2, t_carac=10)
afficherDisque(disque1)

py.init()
fenetre = py.display.set_mode((500, 500))
liste = listeDisque(10)
while True:
    fenetre.fill((0,0,0))
    py.time.Clock().tick(60)
    py.draw.rect(fenetre,(0,0,255),(240,0,20,220))
    py.draw.rect(fenetre,(0,0,255),(240,280,20,240))
    for disk in liste:
        gererCollision(disk, liste)
        py.draw.circle(fenetre, (255,0,0), (int(disk.x), int(disk.y)), 10)
        disk.deplacer()
        if (disk.x > 280):
            liste.remove(disk)
            print("-1 disque")
        py.display.update()

