import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import math
 

#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

# TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#         [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
#         [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
#         [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
#         [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
#         [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
#         [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
#         [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
#         [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
#         [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
#         [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
#         [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
#         [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
#         [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
#         [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
#         [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
#         [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
#         [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
#         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        
TBL = np.array(TBL,dtype=np.int8) # on transforme en tableau de int8 avec numpy
TBL = TBL.transpose()              ## ainsi, on peut écrire TBL[x][y]

WIN   = False # Pacman a gagné
LOOSE = False # Pacman a perdu

LIFE  = 3     # nombre de vie de Pacman
SCORE = 0     # nombre de points de Pacman

NB_CASES_INVINCIBLE = 0      # Le Pacman attaque les ghosts si 0 < NB_CASES_INVINCIBLE
MAX_NB_CASES_INVINCIBLE = 15 # NB_CASES_INVINCIBLE = MAX_NB_CASES_INVINCIBLE quand Pacman mange une super pacgom

ZOOM   = 40 # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

HAUTEUR = TBL.shape [1] # hauteur du tableau TBL
LARGEUR = TBL.shape [0] # largeur du tableau TBL

screeenWidth = (LARGEUR+1) * ZOOM # largeur de l'ecran
screenHeight = (HAUTEUR+2) * ZOOM # hauteur de l'ecran
 


###########################################################################################

# création de la fenetre principale  -- NE PAS TOUCHER

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# création de la frame principale stockant plusieurs pages

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
    
    
def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
################################################################################
#
# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape)
   TOTAL_GUMS = 0
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
            TOTAL_GUMS += 1

   for x, y in [ (1,1) , (LARGEUR-2,1), (1,HAUTEUR-2), (LARGEUR-2,HAUTEUR-2) ]:
      if ( GUM[x][y] == 1 ):
         GUM[x][y] = 2

   return (GUM, TOTAL_GUMS)
            
GUM, TOTAL_GUMS = PlacementsGUM()   

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  , (0, -1) ]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", (0, -1) ]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  , (0, -1) ]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   , (0, -1) ]  )     

 
#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche():
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")


   # chiffres
   moves1 = PacmanMovesTabForGums()
   moves2 = PacmanMovesTabForGhosts() 
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) + 10

         m1 = "∞" if moves1[x][y] == math.inf else str(int(moves1[x][y]))
         m2 = "∞" if moves2[x][y] == math.inf else str(int(moves2[x][y]))
         txt = m1 + " " + m2
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8))
      
      
   # murs
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (GUM[x][y] in [1,2]):
            xx = To(x) 
            yy = To(y)
            e = 5 if GUM[x][y] == 1 else 10
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = "yellow")
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
     
   # scores et vie de Pacman
   color = "red" if 0 < NB_CASES_INVINCIBLE else "yellow"
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "Score : " + str(SCORE) + ", Life : " + str(LIFE), fill = color, font = PoliceTexte)

   # message de victoire ou defaite
   if (WIN or LOOSE):
      canvas.create_text(screeenWidth // 2, screenHeight // 2, text = "Victory !" if WIN else "Defeat", fill ="yellow", font = (PoliceTexte, 75))

            
#################################################################
##
##  IA RANDOM


# renvoie un tableau des distances
def MovesTab(getVal):

   moves = np.array([ [ getVal(y, x) for y in range(LARGEUR) ] for x in range(HAUTEUR) ]) # on genere un tableau numpy a partir de tab
   moves = moves.transpose()   ## ainsi, on peut écrire moves[x][y]

   auMoinsUneModif  = True # on a modifie une valeur dans la boucle for x, for y (1*)
   
   # si on a plus de modifs, on arrete le traitement
   while auMoinsUneModif:
      auMoinsUneModif = False

      # boucle for x, for y (1*)
      for x in range(LARGEUR):
         for y in range(HAUTEUR):

            # on ne prends pas en compte les murs dans les calculs
            if (moves[x][y] == math.inf):  continue

            # valeurs des cellules disposees en carre autour de x, y
            valeursEnvironnantes = [] 
            if (x+1 < LARGEUR) : valeursEnvironnantes.append(moves[x+1][y  ])
            if (0 <= x-1     ) : valeursEnvironnantes.append(moves[x-1][y  ])
            if (y+1 < HAUTEUR) : valeursEnvironnantes.append(moves[x  ][y+1])
            if (0 <= y-1     ) : valeursEnvironnantes.append(moves[x  ][y-1])

            # si on a des valeurs environnantes
            if len(valeursEnvironnantes) != 0:

               # on prend la valeur minimale + 1
               nouvelleValeur = min(valeursEnvironnantes) + 1

               # si la longueur du chemin est plus courte que celle actuellement stockée dans x, y
               if (nouvelleValeur < moves[x][y]):

                  # on mets à jour la valeur
                  moves[x][y] = nouvelleValeur

                  # on indique qu'on a fait une modification
                  auMoinsUneModif = True
   
   # on retourne le tableau des distances généré
   return moves

# renvoie le tableau des distances pour les gums
def PacmanMovesTabForGums():
   def getVal(x, y): 
      if (GUM[x][y] in [1,2])   : return 0
      elif (TBL[x][y] == 0)     : return 100
      else                      : return math.inf

   return MovesTab(getVal)

# renvoie le tableau des distances pour les ghosts
def PacmanMovesTabForGhosts():
   def getVal(x, y): 
      for ghost in Ghosts:
         if (ghost[0] == x and ghost[1] == y): return 0
      
      if (TBL[x][y] == 0) : return 100
      else                : return math.inf

   return MovesTab(getVal)

def PacManPossibleMove():
   L = []
   x,y = PacManPos

   if ( TBL[x  ][y-1] == 0 ): L.append(( 0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append(( 0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1, 0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1, 0))
            
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] in [0, 2] ): L.append(( 0,-1))
   if ( TBL[x  ][y+1] in [0, 2] ): L.append(( 0, 1))
   if ( TBL[x+1][y  ] in [0, 2] ): L.append(( 1, 0))
   if ( TBL[x-1][y  ] in [0, 2] ): L.append((-1, 0))
   return L

def IA():
   global PacManPos, Ghosts, SCORE, LIFE, WIN, LOOSE, TOTAL_GUMS, NB_CASES_INVINCIBLE, MAX_NB_CASES_INVINCIBLE

   # fin de jeu
   if (LIFE <= 0)       : LOOSE = True
   if (TOTAL_GUMS == 0) : WIN   = True
   if (WIN or LOOSE)    : return 


   # deplacement Pacman
   pacmanGumsMoves              = PacmanMovesTabForGums()
   pacmanPhantomMoves           = PacmanMovesTabForGhosts()
   pacmanPossibleMoveDirections = PacManPossibleMove()

   if 0 < NB_CASES_INVINCIBLE:
      # Pacman est invincible : sa priorité est de manger les fantomes (1)
      
      # { longueur_chemin_next_ghost : direction_a_emprunter }
      pacmanBestMoveDirections = { 
         pacmanPhantomMoves[PacManPos[0] + pacmanNextX][PacManPos[1] + pacmanNextY] 
            : 
         (pacmanNextX, pacmanNextY) 
         for pacmanNextX, pacmanNextY in pacmanPossibleMoveDirections 
      }

      # on prend le meilleur choix pour se diriger vers le fantome le plus proche (1)
      pacmanMoveCoords = pacmanBestMoveDirections[min(pacmanBestMoveDirections.keys())]

      NB_CASES_INVINCIBLE -= 1

   else:
      # Pacman n'est plus invincible : sa priorité est de manger les pacgoms (2) et de survivre (3)

      # { longueur_chemin_next_gum : direction_a_emprunter si 3 < longueur_chemin_next_ghost }
      pacmanBestMoveDirections = { 
         pacmanGumsMoves[PacManPos[0] + pacmanNextX][PacManPos[1] + pacmanNextY] 
            : 
         (pacmanNextX, pacmanNextY) 
         for pacmanNextX, pacmanNextY in pacmanPossibleMoveDirections 
         if 3 < pacmanPhantomMoves[PacManPos[0] + pacmanNextX][PacManPos[1] + pacmanNextY]
      }

      if (len(pacmanBestMoveDirections) != 0):
         # on prend le meilleur choix pour aller vers le gum le plus proche, tout en evitant les fantomes les plus proches (2)
         pacmanMoveCoords = pacmanBestMoveDirections[min(pacmanBestMoveDirections.keys())]
      else:
         # { longueur_chemin_next_ghost : direction_a_emprunter }
         pacmanBestMoveDirections = { 
            pacmanPhantomMoves[PacManPos[0] + pacmanNextX][PacManPos[1] + pacmanNextY] 
               : 
            (pacmanNextX, pacmanNextY) 
            for pacmanNextX, pacmanNextY in pacmanPossibleMoveDirections 
         }
         # on prend le meilleur choix pour survivre au fantomes qui sont trop proches (3)
         pacmanMoveCoords = pacmanBestMoveDirections[max(pacmanBestMoveDirections.keys())]
   
   # on mets à jour les coordonnees du Pacman
   PacManPos[0] += pacmanMoveCoords[0]
   PacManPos[1] += pacmanMoveCoords[1]
   
   # deplacement Fantome
   for F in Ghosts:

      # on recupere les directions possibles
      ghostPossibleMoves = GhostsPossibleMove(F[0], F[1])

      if (len(ghostPossibleMoves) == 1):
         # si on est dans une impasse, on va dans la seule direction possible
         ghostCoords = ghostPossibleMoves[0]
      elif (len(ghostPossibleMoves) == 2 and F[3] in ghostPossibleMoves):
         # on est dans un couloir, on continuer dans la meme direction
         ghostCoords = F[3]
      else :
         # on est dans un carrefour, on change de direction aleatoirement
         ghostPossibleMoves = list(filter(lambda p: F[3][0] == p[1] == 0 or F[3][1] == p[0] == 0, ghostPossibleMoves))
         randomIndex = random.randrange(len(ghostPossibleMoves))
         ghostCoords = ghostPossibleMoves[randomIndex]
   
      F[0] += ghostCoords[0]
      F[1] += ghostCoords[1]
      F[3]  = ghostCoords

   # Pacman recupere le gum 
   x, y = PacManPos
   if (GUM[x][y] == 1):
      GUM[x][y] = 0
      SCORE += 10
      TOTAL_GUMS -= 1

   # Pacman recupere le supergum
   if (GUM[x][y] == 2): 
      GUM[x][y] = 0
      SCORE += 50
      NB_CASES_INVINCIBLE = MAX_NB_CASES_INVINCIBLE
      TOTAL_GUMS -= 1

   # les fantomes attaquent Pacman 
   pacmanX, pacmanY = PacManPos
   for ghost in Ghosts:
      ghostX, ghostY = ghost[0], ghost[1]

      # si il y a une collision
      if ((ghostX - pacmanX, ghostY - pacmanY) in [ (0,0), (0,1), (0,-1), (1,0), (-1,0) ]):

         if (0 < NB_CASES_INVINCIBLE):
            # Pacman est invincible, il mange donc les fantomes
            ghost[0] = LARGEUR // 2
            ghost[1] = HAUTEUR // 2
            SCORE += 100
         else:
            # on baisse la vie de Pacman
            LIFE = max(0, LIFE - 1)

#################################################################
##
##   GAME LOOP

def MainLoop():
  IA()
  Affiche()  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

AfficherPage(0)
Window.mainloop()
   
   
    
   
   