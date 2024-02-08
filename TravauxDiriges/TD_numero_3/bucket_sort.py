
import numpy as np
import sys
from time import time
from mpi4py import MPI
import random as rd

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
else:
    dim = 100

dim_local = dim // nbp

# On génère les données localement
start = time()
v_local = np.random.rand(dim_local)
end = time()
print(f"Temps de création des données pour P{rank} : {end - start} sec")

# On calcul le max / min global afin de pouvoir enuite faire les buckets
if rank == 0:
    start = time()
max_local = np.asarray([np.max(v_local)])
min_local = np.asarray([np.min(v_local)])
max_global = np.empty(1, dtype=float)
min_global = np.empty(1, dtype=float)
globCom.Allreduce([max_local, MPI.FLOAT], [max_global, MPI.FLOAT], op=MPI.MAX)
globCom.Allreduce([min_local, MPI.FLOAT], [min_global, MPI.FLOAT], op=MPI.MIN)
if rank == 0:
    end = time()
    print(f"Temps de calcul du max/min global : {end - start} sec")


# On constitue localement les buckets
start = time()
bucket_size = (max_global[0] - min_global[0]) / nbp
buckets = [[] for _ in range(nbp)]
for x in v_local:
    i_bucket = min(int((x - min_global[0]) / bucket_size), nbp-1)
    buckets[i_bucket].append(x)
end = time()
print(f"Temps de constitution local des buckets pour P{rank} : {end - start} sec")

# On regroupe les buckets sur le processeurs appropriés
if rank == 0:
    start = time()
local_bucket = buckets[rank]
for i in range(nbp):
    if rank == i:
        for j in range(nbp):
            if i != j:
                local_bucket.extend(globCom.recv(source=j))
    else:
        globCom.send(buckets[i], dest=i)
if rank == 0:
    end = time()
    print(f"Temps de réunion des buckets : {end - start} sec")

# On trie
start = time()
local_bucket.sort()
end = time()
print(f"Temps du sort pour le processeur {rank} : {end - start} sec")

# On regroupe sur P0
if rank == 0:
    start = time()
    for i in range(1, nbp):
        local_bucket.extend(globCom.recv(source=i))
    end = time()
    print(f"Temps de regroupement des buckets sur P0 : {end - start} sec")
    
    global_end = time()
    print(f"Temps d'exécution totale : {global_end - global_start} sec")
    
else:
    globCom.send(local_bucket, dest=0)


