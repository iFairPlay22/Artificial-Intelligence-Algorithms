import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import tkinter.font as tkFont # ou «import TkFont» pour python 2

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

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
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
  

###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 
DebutDePartie = False
vainqueur = 0

def TestPartieFini():
    global Grille, vainqueur
    vainqueur = 0
    # Tests fin de partie
    for player in [1, 2]:
        # Check les colonnes
        for colonne in Grille:
            if all(cell == player for cell in colonne):
                vainqueur = player

        # Check les lignes
        for i in range(len(Grille)):
            if all(Grille[j][i] == player for j in range(len(Grille[0]))):
                vainqueur = player
        
        # Check les croix
        croix = [0, 1, 2]
        if all(Grille[i][i] == player for i in croix):
            vainqueur = player

        if all(Grille[i][len(Grille[i]) - 1 - i] == player for i in croix):
            vainqueur = player

    if vainqueur == 0 and all(Grille[i][j] != 0 for i in range(len(Grille)) for j in range(len(Grille[i]))):
        vainqueur = 3

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

    if Grille[x][y] != 0:
        return
    
    # Placement du joueur
    Grille[x][y] = 1

    TestPartieFini()
    if (vainqueur != 0): return
    print("Chargement du coup de l'IA ...")
    result, coup = JoueurSimulePlayerN(2)
    print("coups possibles = ", CoupsPossibles())
    print("coup choisi= ", result, coup)
    Grille[coup[0]][coup[1]] = 2
    TestPartieFini()
    if (vainqueur != 0): return


# Liste qui contient des tuples de coups, avec x et y
def CoupsPossibles():
    coupsPossibles = []

    for i in range(len(Grille)):
        for j in range(len(Grille[i])):
            if Grille[i][j] == 0:
                coupsPossibles.append((i, j))
    return coupsPossibles


# coup est un tuple comme ça (x, y)
# result est une liste comme ça [(result, coup), ...]
# les retours des fonctions sont comme ça (result, coup)

def JoueurSimulePlayerN(playerN):
    if vainqueur != 0:
        return (vainqueur, (-1, -1))
    
    result = []
    coups = CoupsPossibles()
    
    for coup in coups:
        Grille[coup[0]][coup[1]] = playerN
        TestPartieFini()

        #Change le joueur qui appelle la fonction
        nextPlayer = 1
        if playerN == 1: nextPlayer = 2
        
        r = JoueurSimulePlayerN(nextPlayer)
        TestPartieFini()

        result.append((r[0], coup))
        Grille[coup[0]][coup[1]] = 0


    if playerN == 1:
        pass
        #print("Calcul coups IA: ", result)
    # Cherche s'il existe un coup gagnant
    for result_coup in result:
        if result_coup[0] == playerN:
            return result_coup
    
    # Cherche s'il existe un coup nul
    for result_coup in result:
        if result_coup[0] == 3:
            return result_coup

    for result_coup in result:
        if result_coup[0] == 0:
            return result_coup

    # Coup perdant
    return result[0]

    
################################################################################
#    
# Dessine la grille de jeu

def Dessine():
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")

        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill="blue", width="4" )
            canvas.create_line(0,i*100,300,i*100,fill="blue", width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
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
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    
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


  


    
        

      
 

