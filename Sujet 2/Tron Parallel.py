import tkinter as tk
import random
import time
import numpy as np
import copy 


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

#############################################################
#
#  affichage en mode texte


def AffGrilles(G,X,Y):
    nbG, larg , haut = G.shape
    for y in range(haut-1,-1,-1) :
        for i in range(nbG) :
            for x in range(larg) :
               g = G[i]
               c = ' '
               if G[i,x,y] == 1 : c = 'M'  # mur
               if G[i,x,y] == 2 : c = 'O'  # trace
               if (X[i],Y[i]) == (x,y) : c ='X'  # joueur
               print(c,sep='', end = '')
            print(" ",sep='', end = '') # espace entre les grilles
        print("") # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas
dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

# nb de parties
nb = 5 

def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties
    G      = np.tile(Game.Grille,(nb,1,1))      # grille  (x,y) pour chaque partie
    X      = np.tile(Game.PlayerX,nb)           # playerX (x)   pour chaque partie
    Y      = np.tile(Game.PlayerY,nb)           # playerY (y)   pour chaque partie
    S      = np.tile(Game.Score,nb)             # score   (s)   pour chaque partie
    I      = np.arange(nb)                      # 0,1,2,3,...,nb-1

    # VOTRE CODE ICI
    continuer = True

    while(continuer) :

        # pour chaque partie, on fait une affectation à 2 le passage de la moto
        G[I, X, Y] = 2


        ### pour chaque partie, on gère tous les index de déplacements possibles
        # pour chaque partie, on associe une liste de taille 4 initialisée à 0 
        LPossibles = np.zeros((nb, 4),dtype=np.int8)

        # pour chaque partie, on associe la liste de taille 4 à i si le joueur peut bouger dans cette direction, 0 sinon
        for i in range(4): 
            LPossibles[I,i] = np.where(G[I, X+dx[i+1], Y+dy[i+1]] == 0,i+1,0)

        # pour chaque partie, on trie la liste des directions de manière décroissante
        LPossibles.sort(axis=1)
        LPossibles = np.fliplr(LPossibles)


        ### pour chaque partie, on compte le nombre de déplacements possibles
        # pour chaque partie, on compte le nombre d'éléments de LPossibles non nuls
        Indices = np.count_nonzero(LPossibles, axis=1)
        
        # pour chaque partie, on remplace les index de 0 par 1 pour pas planter sur le modulo
        Indices[Indices == 0] = 1

        # pour chaque partie, on génère un index de direction aléatoire
        R = np.random.randint(12,size=nb,dtype=np.int8)

        # pour chaque partie, on réucupère un vecteur position
        Position = LPossibles[I, R % Indices[I]]
        

        ### on gère les déplacement et le code
        # on arrete le traitement si, on est statique sur l'ensemble des parties
        if(nb == np.count_nonzero(Position == 0)): continuer = False

        # pour chaque partie, on incrémente le score
        S[I] += ds[Position]

        # pour chaque partie, on déplace le joueur
        X += dx[Position]
        Y += dy[Position]

    # on affiche la moyenne des scores
    print("Moyennes des scores : ", np.mean(S))

Simulate(GameInit)

