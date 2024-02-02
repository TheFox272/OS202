import numpy as np
from time import time
import sys
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

if rank == 0:
    global_start = time()

# Dimention du problème (mis en argument ou pas)
argv = sys.argv
if len(argv) > 1:
    dim = int(sys.argv[1])
    if dim > 10000:
        raise "dim trop grand (doit être < 1000)"
else:
    dim = 120

N_loc = dim // nbp
# Si dim N_loc'est pas divisible par nbp, erreur
if dim != N_loc * nbp:
    raise "dim doit être divisible par nbp"

if rank == 0:
    start = time()
# Initialisation de la matrice
A = np.array([[(i + (j + rank*N_loc)) % dim+1. for i in range(dim)] for j in range(N_loc)], dtype=np.int64)
if rank == 0:
    end = time()
    print(f"Temps de création de A : {end - start} sec")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)], dtype=np.int64)

start = time()
# Produit matrice-vecteur partiel
v = np.empty(dim, dtype=np.int64)
v_local = A.dot(u)
end = time()
print(f"Temps du calcul pour le processeur {rank} : {end - start} sec")

globCom.Allgather(v_local, v)

if rank == 0:
    # print(v)
    global_end = time()
    print(f"Temps d'exécution totale : {global_end - global_start} sec")
