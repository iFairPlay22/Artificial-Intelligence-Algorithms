import tkinter as tk
import random
import numpy as np
import copy 

#################################################################################
#
#   Données de partie
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

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


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

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )
   
    
    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI 

# renvoie les directions réalisables
def GetAllExectuableMove(Game):

    # ensemble des vecteurs directions 
    possibleMove = [(0,+1),(0,-1),(+1,0),(-1,0)]

    # liste des déplacements réalisables
    executableMove = []

    for tup in possibleMove :
        x,y = Game.PlayerX + tup[0], Game.PlayerY + tup[1]
        
        # si on peut se déplacer, on l'ajoute 
        if Game.Grille[x,y] == 0 : executableMove.append((x,y))
    
    return executableMove

# renvoie une direction réalisable aléatoirement
def MovePlayer(Game): 
    executableMove = GetAllExectuableMove(Game)
    if(len(executableMove)<1): return None, None
    return random.choice(executableMove)

# simiule une partie aléatoire
def SimulateGame(Game):
    
    while True :

        # positions du joueur en cours
        x,y = Game.PlayerX, Game.PlayerY

        # on laisse la trace de la moto
        Game.Grille[x,y] = 2  

        # prochaine position du joueur
        x,y = MovePlayer(Game)
        if x == None or y == None : break
        
        # on déplace le joueur
        Game.PlayerX = x 
        Game.PlayerY = y 

        # on incrémente le score
        Game.Score += 1

    # retourne le scode du jeu  
    return Game.Score

# réalise nbGame fois le jeu de manière aléatoire
def MonteCarlo(Game, nbGame):
    Total = 0

    for i in range(nbGame):
        # on fait une copie du jeu
        Game2 = Game.copy()

        # on incrémente les scores réalisés
        Total += SimulateGame(Game2)
        
    return Total

# deplace le joueur de manière intelligente
def MovePlayerWithIA(Game):

    # recupere les directions réalisables
    executableMove = GetAllExectuableMove(Game)
    result = (None, None)
    maxi = 0

    # si on a pas de résultats, on retourne (None, None)
    if(len(executableMove) == 0): return result

    for x,y in executableMove:

        # on déplace le joueur
        Game.PlayerX = x  
        Game.PlayerY = y

        # on recupere le score des simulations 
        total = MonteCarlo(Game, 10000)

        # on recupere les informations pour le meilleur score
        if(maxi < total):
            result = (x,y)
            maxi = total

    return result

def Play(Game):   

    # on laisse la trace de la moto
    Game.Grille[Game.PlayerX, Game.PlayerY] = 2  

    # on récupère la prochaine position la plus pertinente 
    x,y = MovePlayerWithIA(Game)

    # si une collision est détectée, la partie est terminée
    if x == None or y == None : return True 
    
    # on déplace le joueur
    Game.PlayerX = x 
    Game.PlayerY = y  

    # on incrémente le score
    Game.Score += 1

    # la partie continue
    return False   
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = Play(CurrentGame)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(100,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

