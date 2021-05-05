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
def GetAllExectuableMove(Game):
    possibleMove = [(0,+1),(0,-1),(+1,0),(-1,0)]
    executableMove = []
    for tup in possibleMove :
        x,y = Game.PlayerX + tup[0],Game.PlayerY + tup[1]
        v = Game.Grille[x,y]
        if v == 0 :
            executableMove.append((x,y))
    
    return executableMove

def MovePlayer(Game): 
    executableMove = GetAllExectuableMove(Game)
    if(len(executableMove)<1):
        return None, None
    return random.choice(executableMove)


dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

def Simulate(Game):

    nb = NbSimulation
    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True

    # VOTRE CODE ICI

    while(boucle) :

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
        S[I] += ds[Position]
        nb0 =  np.count_nonzero(Position == 0 )
        if(nb0==nb):
            boucle = False
        DX = dx[Position]
        DY = dy[Position]
        X += DX
        Y += DY


    return np.mean(S)



def SimulateGame(Game):
   
    while True :
        x,y = Game.PlayerX, Game.PlayerY

        Game.Grille[x,y] = 2  # laisse la trace de la moto

        x,y = MovePlayer(Game)
        if x == None or y == None :
            break
        else :
            Game.PlayerX = x  # valide le déplacement
            Game.PlayerY = y  # valide le déplacement
            Game.Score += 1

    return Game.Score
     
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
        Window.after(1000,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

