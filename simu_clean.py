import pygame
import math
import numpy as np
import random as rd
from solve import *
import time

#nombre de disque
N = 50
RAYON = 20
TAU = 0.1


#Les couleurs
BLACK = (0, 0, 0)
RED = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (200, 200, 200)


class Pieton:
    def __init__(self, i):
        self.i = i
        self.rect_pieton = None
        self.rayon = RAYON
        self.vitesse = 0
        self.vect_position = pygame.Vector2((rd.randint(50, 250), rd.randint(50, 600)))
        self.vect_vitesse = pygame.Vector2(0, 0)
        self.vect_direction = pygame.Vector2(0, 0)

    def calcul_vect_direction(self):
        vitesse_moyenne = 1.34
        ecart_type = 0.26

        self.vitesse = np.random.normal(vitesse_moyenne, ecart_type, 1) * 40
        
        # chemin le plus court
        self.vect_direction = pygame.Vector2(destination[0] - self.vect_position.x, destination[1] - self.vect_position.y)
        self.vect_direction.normalize_ip()
    
    def afficher_pieton(self):
        self.rect_pieton = pygame.draw.circle(ecran, RED, (int(self.vect_position.x), int(self.vect_position.y)), self.rayon)
    
    def force(self, t, v, matrice_direction, matrice_distance):
        force_1 = (self.vitesse * self.vect_direction - v) / TAU
        
        if N == 1:
            force_2 = pygame.Vector2(0, 0)
        else:
            force_2 = matrice_direction[self.i][j] * sum(math.exp(-matrice_distance[self.i][j] / 100) for j in range(N))
        
        return force_1 + force_2

    def deplacement(self, destination, matrice_direction, matrice_distance):
        def f(t, v):
            return self.force(t, v, matrice_direction, matrice_distance)

        temps, vitesse = Euler(f, T=0.001)

        vect_vitesse = pygame.Vector2(vitesse[0][0], vitesse[0][1])
        
        self.vect_position.x += vect_vitesse.x
        self.vect_position.y += vect_vitesse.y

        self.vitesse = vect_vitesse.length()
        
        self.vect_direction = pygame.Vector2(-self.vect_position.x + destination[0], -self.vect_position.y + destination[1])
        self.vect_direction.normalize_ip()
        
        return self.vect_direction

    def verif_collission(self, mur_haut, mur_bas, disques):
        # collision avec les autres disques
        # for disque in disques:
        #     vect = pygame.Vector2(self.pos.x - disque.pos.x, self.pos.y - disque.pos.y)
        #     norme = vect.length()
        #     if norme != 0 and norme < self.rayon + disque.rayon:
        #         self.pos.rotate_ip(180)
        #         disque.pos.rotate_ip(180)

        # collision avec les murs
        for wall in [mur_haut, mur_bas]:
            mur_x = max(wall.left, min(self.vect_position.x, wall.right))
            mur_y = max(wall.top, min(self.vect_position.y, wall.bottom))
            vect = pygame.Vector2(self.vect_position.x - mur_x, self.vect_position.y - mur_y)
            norme = vect.length() 
            if norme != 0 and norme < self.rayon:
                vect.normalize_ip()
                self.vect_position += vect * self.vitesse

        # collision avec le bord de l'ecran
        self.vect_position.x = min(ecran.get_width() - self.rayon, max(self.vect_position.x, self.rayon))
        self.vect_position.y = min(ecran.get_height() - self.rayon, max(self.vect_position.y, self.rayon))



list_pietons = []

for i in range(0, N):
    list_pietons.append(Pieton(i))


pygame.init()
simu_en_cours = True
image = 0

clock = pygame.time.Clock()
ecran = pygame.display.set_mode((1280, 720))

milieu_x = int(ecran.get_width() / 2)
milieu_y = int(ecran.get_height() / 2)

destination = (milieu_x + 600, milieu_y)
mur_haut = pygame.Rect(milieu_x - 50, 0, 100, milieu_y - 50)
mur_bas = pygame.Rect(milieu_x - 50, milieu_y + 50, 100, milieu_y - 50)

debut_boucle = time.perf_counter() # associe l'heure initiale
police = pygame.font.SysFont("Font/Robotto.ttf", 30, "bold=True") # police monospace de taille 10



matrice_direction = [[pygame.Vector2(0, 0)] * N] * N
matrice_distance = [[0] * N] * N



while simu_en_cours:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simu_en_cours = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        simu_en_cours = False

    ecran.fill(BLUE)

    pygame.draw.rect(ecran, GREEN, mur_haut)
    pygame.draw.rect(ecran, GREEN, mur_bas)
    rect_destination = pygame.draw.circle(ecran, GREEN, destination, 10)

    for i in range(N):
        for j in range(i+1, N):
            pieton_i = list_pietons[i]
            pieton_j = list_pietons[j]

            distance = pieton_i.vect_position.distance_to(pieton_j.vect_position)
            matrice_distance[i][j] = distance

            vect = pygame.Vector2(
                pieton_i.vect_position.x - pieton_j.vect_position.x,
                pieton_i.vect_position.y - pieton_j.vect_position.y,
            )

            if vect.length() != 0:
                vect.normalize_ip()

            matrice_direction[i][j] = vect
    
    for i, pieton in enumerate(list_pietons):
        pieton.calcul_vect_direction()
        pieton.deplacement(destination, matrice_direction, matrice_distance)
        pieton.verif_collission(mur_haut, mur_bas, list_pietons[i:])
        
        if pieton.rect_pieton != None and rect_destination.colliderect(pieton.rect_pieton):
            list_pietons.remove(pieton)
            N -= 1

        pieton.afficher_pieton()

    # affichage du compteur de pions et du chronomètre
    chrono = time.perf_counter() - debut_boucle # met à jour le temps en calculant la durée en cet instant et le temps de début
    
    affichage_temps = police.render(f"Temps: {chrono:.2f}", 1, BLACK)
    compteur_pions = police.render(f"Nb de pietons restants: {N}", 1, BLACK)
    
    ecran.blit(compteur_pions, (200, 0))
    ecran.blit(affichage_temps, (0, 0))

    
    clock.tick(60) / 1000
    pygame.display.flip()
    image += 1

pygame.quit()
