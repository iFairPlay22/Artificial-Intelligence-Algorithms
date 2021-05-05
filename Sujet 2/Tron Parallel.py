import tkinter as tk
import random
import time
import numpy as np


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

Debug = False
nb = 15 # nb de parties

def push_zeros_back(array):
    valid_mask = array != 0
    flipped_mask = valid_mask.sum(1, keepdims=1) > np.arange(array.shape[1] - 1, -1, -1)
    print( np.arange(array.shape[1] -1))
    #print(flipped_mask)
    flipped_mask = flipped_mask[:, ::-1]
    #print(flipped_mask)
    array[flipped_mask] = array[valid_mask]
    #print(array)
    array[~flipped_mask] = 0
    return array

def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI

    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2
        # Direction : 2 = vers le haut
        R = np.random.randint(4,size=nb)

        #DEPLACEMENT
        LPossibles = np.zeros((nb,4),dtype=np.int8)
        LPossibles[I,0] = np.where(G[I, X+dx[1], Y+dy[1]] == 0,1,0)
        LPossibles[I,1] = np.where(G[I, X+dx[2], Y+dy[2]]==0,2,0)
        LPossibles[I,2] = np.where(G[I, X+dx[3], Y+dy[3]]==0,3,0)        
        LPossibles[I,3] = np.where(G[I, X+dx[4], Y+dy[4]]==0,4,0)
        LPossibles.sort(axis=1)#sort
        LPossibles = np.fliplr(LPossibles)#flip the sort by descending order

        Indices = np.zeros(nb,dtype=np.int8)
        Indices = np.count_nonzero(LPossibles, axis=1)
      
        Indices[Indices == 0]=1
        Position = LPossibles[I,R%Indices[I]]
        if Debug :print("Position : ",Position)
        S[I] += Position[I]!=0
        nb0 =  np.count_nonzero(Position == 0 )
        if(nb0==nb):
            boucle = False
        DX = dx[Position]
        DY = dy[Position]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY


        #debug
        if Debug : AffGrilles(G,X,Y)
        #if Debug : time.sleep(2)
    AffGrilles(G,X,Y)
    print(S)
    print("Scores : ",np.mean(S))



Simulate(GameInit)

