import tkinter as tk
import random
import numpy as np
import copy 
import time
# voici les 4 touches utilisées pour les déplacements  gauche/haut/droite/bas

Keys =  ['q','z','d','s']

#################################################################################
#
#   Données de partie
#
#################################################################################


Data = [   [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0,0],
           [0,0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,8] ]


GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17


#################################################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER
#
#################################################################################


L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = (HAUTEUR+1) * L
DEBUG =False

Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix+3))   # taille de la fenetre
Window.title("Frozen Lake")

# gestion du clavier

LastKey = '0'
 
    
def keydown(e):  
    global LastKey
    if hasattr(e,'char') and e.char in Keys:
        LastKey = e.char
        
    
# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.bind("<KeyPress>", keydown)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)
F.focus_set()

# gestion des pages

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
    H = canvas.winfo_height()-2
    
    def MSG(coul,txt):
       
        canvas.create_rectangle(0,0,largeurPix,20,fill="black")
        canvas.create_text(largeurPix//2, 10,  font='Helvetica 12 bold', fill=coul, text=txt )
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin du décors
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 0  : DrawCase(x,y,"cyan" )
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"blue" )
           if Game.Grille[x,y] == 8  : DrawCase(x,y,"pink" )
   
    DrawCase(Game.PlayerPos[0],Game.PlayerPos[1],"yellow" )
   
    MSG("yellow",str(Game.Score))     
  
################################################################################
#
#                          Gestionnaire de partie
#
################################################################################

 
class Game:
    
    def __init__(self):
        self.Grille = GInit
        self.Score = 0
        self.ResetPlayerPos()
        
        
    def ResetPlayerPos(self):
        self.PlayerPos = [0,HAUTEUR-1] 
        
        
    def Doo(self,action):
        global DEBUG
        if DEBUG : print('Start')
        #  annulation des déplacements vers un mur
        if self.PlayerPos[0] == 0          and action == 0:  return 0
        if self.PlayerPos[0] == LARGEUR-1  and action == 2:  return 0
        
        if self.PlayerPos[1] == 0          and action == 3:  return 0
        if self.PlayerPos[1] == HAUTEUR-1  and action == 1:  return 0
        
        if DEBUG :print('AfterWall')
        # 0 ; left, 2: up, 4: right, 6: down
        P = [ 0 ] * 8 
        v = 100
        P[(action * 2 - 1) % 8] = v
        P[ action * 2         ] = v
        P[(action * 2 + 1) % 8] = v
        
        
        # plus on se rapproche de l'objectif, plus ca glisse
        for i in range(8) : P[i] += LARGEUR-self.PlayerPos[0] + (HAUTEUR-self.PlayerPos[1])
        
        # gestion des murs
        if self.PlayerPos[0] == 0 :           P[7] = P[0] = P[1] = 0 # mur gauche
        if self.PlayerPos[0] == LARGEUR-1 :   P[3] = P[4] = P[5] = 0 # mur droit
        
        if self.PlayerPos[1] == 0 :           P[5] = P[6] = P[7] = 0 # mur bas
        if self.PlayerPos[1] == HAUTEUR-1 :   P[1] = P[2] = P[3] = 0 # mur haut
        
        # tirage aléa
        totProb = sum(P)
        rd = random.randrange(0,totProb)+1
        choix = 0
        while P[choix] < rd :
            rd -= P[choix]
            choix += 1
    
        # traduction 0-7 => déplacement
        if choix in [7,0,1] : self.PlayerPos[0] -= 1
        if choix in [3,4,5] : self.PlayerPos[0] += 1
        if choix in [1,2,3] : self.PlayerPos[1] += 1
        if choix in [5,6,7] : self.PlayerPos[1] -= 1
         
        # gestion des collisions
        
        xP,yP = self.PlayerPos
        if self.Grille[xP][yP] == 1 :   # DEAD
            self.ResetPlayerPos()
            return -100
            
        if self.Grille[xP][yP] == 8 :   # WIN
            self.ResetPlayerPos() 
            return 100
            
        return 0  
        

    def Do(self,action):
        reward = self.Doo(action)
        self.Score += reward
        return reward
    
    def GetNbCase(self):
        return (HAUTEUR-1-self.PlayerPos[1])*(LARGEUR)+self.PlayerPos[0]

        

###########################################################
#
#   découvrez le jeu en jouant au clavier
#
###########################################################
 
G = Game()

def JeuClavier():   
    F.focus_force()

    global LastKey
  
    r = 0 # reward
    if LastKey != '0' :
        if LastKey == Keys[0] : G.Do(0)
        if LastKey == Keys[1] : G.Do(1)
        if LastKey == Keys[2] : G.Do(2)
        if LastKey == Keys[3] : G.Do(3)

    Affiche(G)
    LastKey = '0'
    Window.after(500,JeuClavier)
     

###########################################################
#
#  simulateur de partie aléatoire
#
###########################################################
def Test(Q_table):
    global DEBUG
    DEBUG=True
    G = Game()
    reward=0;
    for t in range(100):
        s=G.GetNbCase()
        action = random.randrange(0,4)
        a = np.argmax(Q_table[s,:])
        reward += G.Do(a)
        
        
    return reward # over limitpy
    
def SimulGame():   # il n y a pas de notion de "fin de partie"
    Q_table = np.zeros((LARGEUR*HAUTEUR,len(Keys)))
    lr = .85
    y = .99
    liste=[]
    for i in range(1000): 
            
        G = Game()
        
        s=G.GetNbCase()
        for i in range(100):
            
            cumul_reward = 0
            a = random.randrange(0,4)
            reward = G.Do(a)
            s1=G.GetNbCase()
            Q_table[s, a] = Q_table[s, a] + lr*(reward + y * np.max(Q_table[s1,:]) - Q_table[s, a]) # Fonction de mise à jour de la Q-table
            s=s1
            cumul_reward += reward
            
        liste.append(cumul_reward)
       
    return str(sum(liste)/len(liste)), Q_table

# Q learning params
ALPHA = 0.1 # learning rate
GAMMA = 0.99 # reward discount
LEARNING_COUNT = 1000
TEST_COUNT = 1000

TURN_LIMIT = 100
IS_MONITOR = True

class Agent:
    def __init__(self, env):
        self.env = env
        self.episode_reward = 0.0
        self.q_val = np.zeros(LARGEUR*HAUTEUR * len(Keys)).reshape(LARGEUR*HAUTEUR , len(Keys)).astype(np.float32)

    def learn(self):
        # one episode learning
        self.env=Game()
        state = self.env.GetNbCase()
        
        #self.env.render()
        liste=[]
        for t in range(TURN_LIMIT):
            act = random.randrange(0,4) # random
            reward = self.env.Do(act)
            next_state =self.env.GetNbCase()
            q_next_max = np.max(self.q_val[next_state])
            # Q <- Q + a(Q' - Q)
            # <=> Q <- (1-a)Q + a(Q')
            self.q_val[state][act] = (1 - ALPHA) * self.q_val[state][act]\
                                 + ALPHA * (reward + GAMMA * q_next_max)
            
            #self.env.render()
            state = next_state
        return self.env.Score # over limit

    def test(self):
        self.env=Game()
        state = self.env.GetNbCase()
        for t in range(TURN_LIMIT):
            act = np.argmax(self.q_val[state])
            print(act)
            reward = self.env.Do(act)
            next_state =self.env.GetNbCase()
            state = next_state
        return self.env.Score # over limit

def main():
    env = Game()
    agent = Agent(env)

    print("###### LEARNING #####")
    reward_total = 0.0
    for i in range(LEARNING_COUNT):
        reward_total += agent.learn()
    print("episodes      : {}".format(LEARNING_COUNT))
    print("total reward  : {}".format(reward_total))
    print("average reward: {:.2f}".format(reward_total / LEARNING_COUNT))
    print("Q Value       :{}".format(agent.q_val))

    print("###### TEST #####")
    reward_total = 0.0
    for i in range(TEST_COUNT):
        reward_total += agent.test()
    print("episodes      : {}".format(TEST_COUNT))
    print("total reward  : {}".format(reward_total))
    print("average reward: {:.2f}".format(reward_total / TEST_COUNT))




#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

 
AfficherPage(0)
Window.after(500,main)
Window.mainloop()
      

    
        

      
 

