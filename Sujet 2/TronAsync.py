import tkinter as tk
import random
import numpy as np
import copy 
import time

#################################################################################
#
#   Données de partie
NbSimulation = 10000
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
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
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
dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)
def GetAllExectuableMove(Game):
    possibleMove = [(0,+1),(0,-1),(+1,0),(-1,0)]
    executableMove = []
    for tup in possibleMove :
        x,y = Game.PlayerX + tup[0], Game.PlayerY + tup[1]
        v = Game.Grille[x,y]
        if v == 0 :
            executableMove.append((x,y))
    
    return executableMove

def Simulate(Game):

    nb = NbSimulation
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

    # on retourne la moyenne des scores
    return np.mean(S)


     
def MonteCarlo(Game):
    return Simulate(Game)

def MovePlayerWithIA(Game):
    executableMove = GetAllExectuableMove(Game)
    result = (None, None)
    maxi = 0
    if(len(executableMove)==0):
        return None, None

    for x,y in executableMove:
        Game.PlayerX = x  
        Game.PlayerY = y
        total = MonteCarlo(Game)
        if(total>maxi):
            result = (x,y)
            maxi = total
    return result

def Play(Game):   
    
    x,y = Game.PlayerX, Game.PlayerY

    Game.Grille[x,y] = 2  # laisse la trace de la moto

    x,y = MovePlayerWithIA(Game)
    if x == None or y == None :
        # collision détectée
        return True # partie terminée
    else :
       Game.PlayerX = x  # valide le déplacement
       Game.PlayerY = y  # valide le déplacement
       Game.Score += 1
       return False   # la partie continue
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():
    Tstart = time.time()
    PartieTermine = Play(CurrentGame)
    print(time.time() -  Tstart)
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(1,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

