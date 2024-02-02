# Produit matrice-vecteur v = A.u
import numpy as np
from time import time
import sys

global_start = time()

# Dimention du problème (mis en argument ou pas)
argv = sys.argv
if len(argv) > 1:
    dim = int(sys.argv[1])
    if dim > 10000:
        raise "dim trop grand (doit être < 1000)"
else:
    dim = 120

start = time()
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
# print(f"A = {A}")
end = time()
print(f"Temps de création de A : {end - start} sec")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
# print(f"u = {u}")

start = time()
# Produit matrice-vecteur
v = A.dot(u)
# print(f"v = {v}")
end = time()
print(f"Temps du calcul : {end - start} sec")

global_end = time()
print(f"Temps d'exécution totale : {global_end - global_start} sec")
