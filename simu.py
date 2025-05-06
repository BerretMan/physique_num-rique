import pygame
import math
import numpy as np
import random as rd
from solve import *
import time

#nombre de Pieton
N=50
RAYON=20
tau=0.1

#Les couleurs
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (200, 200, 200)
TURQUOISE=(64, 224, 208)


class Pieton:
    def __init__(self,i):
        """

        Paramètres:
        vitesse (float) : la vitesse du Pieton
        direction (float) : la direction du Pieton en degrés
        """
        self.pos=pygame.Vector2((l_position_aleatoire[i][0], l_position_aleatoire[i][1]))
        self.vitesse = 0
        self.vect_vitesse=pygame.Vector2(0,0)
        self.vect_direction=pygame.Vector2(0,0)
        self.i=i

    def calcul_vect_direction(self):
        #valeur de base
        vitesse_moyenne=1.34
        ecart_type=0.26
        tau=1

        #vitesse de n piéton 
        self.vitesse=np.random.normal(vitesse_moyenne,ecart_type,1)*40
        self.vect_direction = pygame.Vector2(-self.pos.x+destination[0],-self.pos.y+destination[1])
        self.vect_direction.normalize_ip()
    
    def afficher_pieton(self):
        self.player=pygame.draw.circle(ecran, RED, (int(self.pos.x),int(self.pos.y)), RAYON)

    def deplacement(self):
        t=1
        v=0
        dt=0
        le_temps,self.vect_vitesse=RK4(self.f,T=0.001)
        self.pos.x+=self.vect_vitesse[0][0]
        self.pos.y+=self.vect_vitesse[0][1]
        self.vect_direction = pygame.Vector2(-self.pos.x+destination[0],-self.pos.y+destination[1])
        self.vect_direction.normalize_ip()
        return self.vect_direction
    
    def f(self,t,v):
        force_1= (self.vitesse * self.vect_direction - v) / tau
        force_2=pygame.math.Vector2(0,0)
        force_mur=pygame.math.Vector2(0,0)
        if(N==1):
            force_2=pygame.Vector2(0,0)
        else:
            B=50
            B_MUR=100
            for j in range(N):
                if self.i!=j:
                    direction=pygame.Vector2(matrice_direction[self.i][j])
                    force_2+=direction*math.exp(-matrice_distance[self.i][j]/B)
            force_mur=l_direction[self.i]*math.exp(-l_distance[self.i]/B_MUR)

        return 1/4*force_1 +150*force_2+100*force_mur
    def verif_collission(self,list_mur):
       # Vérification de la collision avec les mur

        self.pos.x = min(ecran.get_width() - RAYON+400, max(self.pos.x, RAYON))
        self.pos.y = min(ecran.get_height() - RAYON, max(self.pos.y, RAYON))

        for mur in list_mur:
            closest_x = max(mur.left, min(self.pos.x, mur.right))
            closest_y = max(mur.top, min(self.pos.y, mur.bottom))
            vect = pygame.Vector2(self.pos.x - closest_x, self.pos.y - closest_y)

            if vect.length() < RAYON:
                norme_v = math.sqrt(self.vect_vitesse[0][0]**2 + self.vect_vitesse[0][1]**2)
                if vect.length() >0:
                    vect.normalize_ip()
                self.pos += vect * norme_v
        
        if dest_rect.colliderect(self.player):
            return True
        
        return False

def poisson_disque_sampling(r):
    l=[]
    taille_disque=r/math.sqrt(2)
    l.append((rd.randint(50, 600), rd.randint(50, 600)))
    i=0
    while i<N:
        x,y=rd.randint(50, 600), rd.randint(50, 600)
        if all(math.sqrt((x - x_l)**2 + (y - y_l)**2) > r+10 for x_l, y_l in l):
            l.append((x,y))
            i+=1
    return l

l_position_aleatoire=poisson_disque_sampling(RAYON)

pygame.init()
simu_en_cours = True


clock = pygame.time.Clock()

width=1280
height=720

ecran = pygame.display.set_mode((width, height))
middle_x = int(ecran.get_width() / 2)
middle_y = int(ecran.get_height() / 2)
destination = (middle_x+650, middle_y+300)


#mur 


mur_haut= pygame.Rect(0, 0, width, 20)
mur_bas= pygame.Rect(0, height-20, width, 20)
mur_gauche= pygame.Rect(0, 0, 20, height)
mur_droit = pygame.Rect(width-20, 0, 20, height-200)
list_mur=[mur_haut,mur_bas,mur_droit,mur_gauche]

#Créer les piétons
list_pietons=[]
for i in range(0,N):
    list_pietons.append(Pieton(i))


#initialisation des tableaux et matrices
matrice_distance=[[0]*N for _ in range(N)]
matrice_direction=[[0,0]*N for _ in range(N)]
l_direction=[0]*N
l_distance=[0]*N

for Pieton in list_pietons:
    Pieton.calcul_vect_direction()

debut_boucle=time.perf_counter() # asocie l'heure initiale
police=pygame.font.SysFont("Font/Robotto.ttf", 30, "bold=True") #police=monospace de taille 10


while simu_en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simu_en_cours = False
    ecran.fill(BLUE)

    for mur in list_mur:
        pygame.draw.rect(ecran, TURQUOISE, mur)
    dest_rect = pygame.draw.circle(ecran, GREEN, destination, 20)


    l_Pieton_supprimer=[]
    for Pieton in list_pietons:
        Pieton.afficher_pieton()
        Pieton.deplacement()
        if Pieton.verif_collission(list_mur):
            l_Pieton_supprimer.append(Pieton)

    for Pieton in l_Pieton_supprimer:
        list_pietons.remove(Pieton)
        N=N-1

    for index, Pieton in enumerate(list_pietons):
        Pieton.i = index

        

    for i in range(N):
        for j in range(i, N):
            dist = list_pietons[i].pos.distance_to(list_pietons[j].pos)-RAYON
            matrice_distance[i][j] = dist
            matrice_distance[j][i] = dist  

            vect=pygame.Vector2(+list_pietons[i].pos.x-list_pietons[j].pos.x,+list_pietons[i].pos.y-list_pietons[j].pos.y)
            if (vect.length())**2 >0:
                vect.normalize_ip()
            matrice_direction[i][j]=vect

    for Pieton in list_pietons:
        
        closest_x,closest_y=0,0
        dist=float("inf")

        for mur in list_mur:
            candidat_closest_x = max(mur.left, min(Pieton.pos.x, mur.right))
            candidat_closest_y = max(mur.top, min(Pieton.pos.y, mur.bottom))

            new_dist=math.sqrt((candidat_closest_x-Pieton.pos.x)**2+(candidat_closest_y-Pieton.pos.y)**2)
            if new_dist<=dist:
                dist=new_dist
                closest_x,closest_y=candidat_closest_x,candidat_closest_y


        l_distance[Pieton.i]=math.sqrt((closest_x-Pieton.pos.x)**2+(closest_y-Pieton.pos.y)**2)-RAYON

        direction_mur=-pygame.Vector2(closest_x-Pieton.pos.x,closest_y-Pieton.pos.y)
        if (direction_mur.length())**2>0:
            direction_mur.normalize_ip()
        l_direction[Pieton.i]=direction_mur



#affichage du compteur de pions et du chronomètre

    chrono=time.perf_counter()-debut_boucle #met à jour le temps en calculant la durée en cet instant et le temps de début
    affichage_temps=police.render(f"tmp={chrono:.2f}", 1, BLACK)
    compteur_pions=police.render(f"nb de pions restants={N}", 1, BLACK)
    ecran.blit(compteur_pions, (200, 0))
    ecran.blit(affichage_temps, (0, 0))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()