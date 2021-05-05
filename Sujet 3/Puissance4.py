import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import tkinter.font as tkFont # ou «import TkFont» pour python 2

###############################################################################
# création de la fenetre principale  - ne pas toucher

# définie le nombre de cases et la taille
# 300 300 pour un morpion
LARG = 700
HAUT = 600

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
Grille = [ [0,0,0,0,0,0,0], 
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0], 
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
cellSizeX = LARG / len(Grille)
cellSizeY = HAUT / len(Grille[0])


###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 
DebutDePartie = False
vainqueur = 0

# Pose un jeton avec un numéro de colonne
# Position Y du nouevau jeton, sinon -1
def JetonPose(x, player):
    jetonPose = False
    for i in range(len(Grille[x]) - 1, -1, -1):
        if Grille[x][i] == 0:
            Grille[x][i] = player
            jetonPose = True
            break

    if not jetonPose: return -1
    return i


directions = [ 
    # Gauche-droite Haut-bas
    [1, 0],  #droite
    [-1, 0], #gauche
    [0, -1], #bas
    [0, 1],  #haut
    [1, 1],  #diagonale haut droite
    [-1, 1],  #diagonale haut gauche
    [-1, -1],  #diagonale bas gauche
    [1, -1],  #diagonale bas droite
]


def TestPartieFini():
    global Grille, vainqueur
    vainqueur = 0

    # Tests fin de partie
    for player in [1, 2]:

        cells = []
        for i in range(len(Grille)):
            for j in range(len(Grille[i])):
                if Grille[i][j] == player:
                    cells.append((i, j))

        for i, j in cells:
            for direction in directions:
                aligned = 0
                while i < len(Grille) and j < len(Grille[i]) and i > 0 and j > 0:
                    
                    if Grille[i][j] != player: 
                        break
                    
                    aligned += 1
                    if aligned >= 4:
                        vainqueur = player
                        break
                    
                    i += direction[0]
                    j += direction[1]
                

    if vainqueur == 0 and all(Grille[i][j] != 0 for i in range(len(Grille)) for j in range(len(Grille[i]))):
        vainqueur = 3

# Compte le nombre de jetons alignés autour d'une case x y
def compteAlignement(x, y, player):

    maxAligned = 0
    for direction in directions:
        aligned = 0
        for n in range(-4, 4):

            cellX = (direction[0] * n) + x
            cellY = (direction[1] * n) + y

            if cellX > len(Grille) - 1 or cellY > len(Grille[cellX]) - 1 or cellX < 0 or cellY < 0:
                continue
            
            if Grille[cellX][cellY] != player: 
                continue
            
            aligned += 1
            maxAligned = max(aligned, maxAligned)

    return maxAligned


def Play(x,y):
    global DebutDePartie, Grille, vainqueur

    if DebutDePartie or vainqueur != 0:
        for i in range(len(Grille)):
            for j in range(len(Grille[i])):
                Grille[i][j] = 0
        vainqueur = 0
        DebutDePartie = False
        Dessine()
        return
    
    # Placement du joueur
    if JetonPose(x, 1) < 0: return

    TestPartieFini()
    if (vainqueur != 0): return
    print("Chargement du coup de l'IA ...")
    result, coup = Minimax(2)
    
    print("coups possibles = ", CoupsPossibles())
    #print("coup choisi= ", result, coup)
    JetonPose(coup, 2)
    TestPartieFini()
    if (vainqueur != 0): return


# Liste qui contient des tuples de coups, avec x et y
def CoupsPossibles():
    coupsPossibles = []

    for i in range(len(Grille)):
        if any(Grille[i][j] == 0 for j in range(len(Grille[i]))):
            coupsPossibles.append(i)
    
    return coupsPossibles
            

# coup est le numéro de la colonne (x)
# result est une liste comme ça [(result, coup), ...]
# les retours des fonctions sont comme ça (nombre de point, coup)
rec = 0
def Minimax(playerN):
    global rec

    if rec > 3:
        rec = 0
        return (vainqueur, -1)
    rec += 1

    if vainqueur != 0:
        return (vainqueur, -1)
    
    result = []
    coups = CoupsPossibles()
    
    print("here")
    for coup in coups:
        y = JetonPose(coup, playerN)
        TestPartieFini()

        #Change le joueur qui appelle la fonction
        nextPlayer = 1
        if playerN == 1: nextPlayer = 2
        
        r = Minimax(nextPlayer)
        TestPartieFini()

        result.append((r[0], coup))
        Grille[coup][y] = 0


    maxCoup = 0
    maxResult = 0
    # Cherche s'il existe un coup gagnant
    for result_coup in result:
        if result_coup[0] > maxCoup:
            maxCoup = result_coup[0]
            maxResult = result_coup[1]
    
    # Coup perdant
    return (maxCoup, maxResult)

    
################################################################################
#    
# Dessine la grille de jeu
def DessineRond(x, y, color):
    xc = x * cellSizeX 
    yc = y * cellSizeY

    offsetX = 10 / 100 * cellSizeX # 10% d'offset
    offsetY = 10 / 100 * cellSizeY

    drawX = 90 / 100 * cellSizeX # le dessin représente 90% de la cellule (10% d'offset)
    drawY = 90 / 100 * cellSizeY

    canvas.create_line(xc + offsetX, yc + offsetY, xc + drawX, yc + drawY, fill=color, width="4" )
    canvas.create_line(xc + drawX, yc + offsetY, xc + offsetX, yc + drawY, fill=color, width="4" )


def Dessine():
    ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")

    #Dessin des lignes de grille
    for i in range(8):
        canvas.create_line(i*cellSizeX,0,i*cellSizeX,max(LARG, HAUT),fill="blue", width="4" )
        canvas.create_line(0,i*cellSizeY,max(LARG, HAUT),i*cellSizeY,fill="blue", width="4" )
        
    for x in range(len(Grille)):
        for y in range(len(Grille[0])):

            if ( Grille[x][y] == 1):
                DessineRond(x, y, "red")
            if ( Grille[x][y] == 2):
                DessineRond(x, y, "yellow")
    
    if vainqueur != 0:
        font = tkFont.Font(size=50)
        textVainqueur = "Gagné"
        if vainqueur == 2: textVainqueur = "Perdu"
        if vainqueur == 3: textVainqueur = "Match nul"
        canvas.create_text(LARG / 2, HAUT / 4, text=textVainqueur, fill="white", font=font)
        

        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
   
    Window.focus_set()
    x = int(event.x // cellSizeX)  # convertit une coordonée pixel écran en coord grille de jeu
    y = int(event.y // cellSizeY)
    if ( (x<0) or (x> len(Grille)) or (y<0) or (y>len(Grille[0])) ) : return
     
    
    print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    
    Dessine()
    


canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()


  


    
        

      
 

