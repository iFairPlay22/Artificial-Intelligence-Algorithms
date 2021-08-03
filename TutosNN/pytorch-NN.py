import torch, numpy,matplotlib.pyplot as plt


''' Pytorch - Tensor
ListePython = [[1,2,3], [4,5,6]]
A = torch.FloatTensor(ListePython)
print(A)
ArrayNumpy = numpy.array(ListePython)
B = torch.FloatTensor(ArrayNumpy)
print(B)

A = torch.FloatTensor([[1,2,3],[4,5,6]])
print(A.tolist()) # => liste python
print(A.numpy()) # => numpy array

A = torch.FloatTensor([2])
print(A.item()) # => numérique python

A = torch.FloatTensor([[0,0,0],[10,10,10]])
print(A.shape)

'''

''' Pytorch Neurone 
layer = torch.nn.Linear(in_features = 4, out_features = 2)
print("Poids :", layer.weight, layer.weight.shape)
print("Biais :", layer.bias, layer.bias.shape)
Input = torch.FloatTensor([1,2,3,4])
Sortie = layer(Input)
print("Sortie :", Sortie, Sortie.shape)

layer = torch.nn.Linear(1,1)
input = torch.FloatTensor([4])
output = layer(input)
print(output)
layer = torch.nn.Linear(1,1) # creation de la couche Linear
activ = torch.nn.ReLU() # fonction d’activation Relu
Lx = numpy.linspace(-2,2,50) # échantillonnage de 50 valeurs dans [‐2,2]
Ly = []

for x in Lx:
    input = torch.FloatTensor([x]) # création d’un tenseur de taille 1
    v1 = layer(input) # utilisation du neurone
    v2 = activ(v1) # application de la fnt activation ReLU
    Ly.append(v2.item()) # on stocke le résultat dans la liste

plt.plot(Lx,Ly,'.') # dessine un ensemble de points(())
plt.axis('equal') # repère orthonormé
plt.show() # ouvre la fenetre d'affichage

layer = torch.nn.Linear(1,1)
relu = torch.nn.ReLU()
Lx = numpy.linspace(-2,2,50)
Lx = torch.FloatTensor(Lx) # crée un tenseur de taille 50
Lx = Lx.reshape(50,1) # change la taille du tenseur pour (50,1)
Ly = layer(Lx) # calcule pour chaque xi la sortie du neurone
Ly = relu(Ly) # applique la fonction d'activation
Ly = Ly.detach() # extrait le tenseur du réseau
Ly = Ly.numpy() # conversion vers un tableau numpy
plt.plot(Lx,Ly,'.') # dessine un ensemble de points(())
plt.axis('equal') # repère orthonormé
plt.show() # ouvre la fenetre d'affichage

layer1 = torch.nn.Linear(50, out_features = 3) # creation de la couche Linear
layer2 = torch.nn.Linear(in_features = 3, out_features = 1)
activ = torch.nn.ReLU() # fonction d’activation Relu
Lx = numpy.linspace(-2,2,50) # échantillonnage de 50 valeurs dans [‐2,2]
Lx = torch.FloatTensor(Lx)
Lx = Lx.reshape(50,1)
Ly = layer1(Lx)
Ly = activ(Ly)
Ly = layer2(Ly)
Ly = Ly.detach() # extrait le tenseur du réseau
Ly = Ly.numpy() # conversion vers un tableau numpy
plt.plot(Lx,Ly,'.') # dessine un ensemble de points(())
plt.axis('equal') # repère orthonormé
plt.show() # ouvre la fenetre d'affichage

layer = torch.nn.Linear(1,1)
relu = torch.nn.ReLU()
Lx = numpy.linspace(-2,2,50)
Lx = torch.FloatTensor(Lx) # crée un tenseur de taille 50
Lx = Lx.reshape(50,3) # change la taille du tenseur pour (50,1)
Ly = layer(Lx) # calcule pour chaque xi la sortie du neurone
Ly = relu(Ly) # applique la fonction d'activation
Ly = Ly.detach() # extrait le tenseur du réseau
Ly = Ly.numpy() # conversion vers un tableau numpy
plt.plot(Lx,Ly,'.') # dessine un ensemble de points(())
plt.axis('equal') # repère orthonormé
plt.show() # ouvre la fenetre d'affichage
''' 

layer = torch.nn.Linear(50,3)
relu = torch.nn.ReLU()
Lx = numpy.linspace(-2,2,50)
Lx = torch.FloatTensor(Lx) # crée un tenseur de taille 50
Lx = torch.reshape(Lx,(3,50)) # change la taille du tenseur pour (50,1)
Ly = layer(Lx) # calcule pour chaque xi la sortie du neurone
Ly = relu(Ly) # applique la fonction d'activation
Ly = Ly.detach() # extrait le tenseur du réseau
Ly = Ly.numpy() # conversion vers un tableau numpy
plt.plot(Lx,Ly,'.') # dessine un ensemble de points(())
plt.axis('equal') # repère orthonormé
plt.show() # ouvre la fenetre d'affichage