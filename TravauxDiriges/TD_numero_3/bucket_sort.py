import numpy as np
import sys
from time import time
from mpi4py import MPI
import random as rd

# On initialise MPI
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
    if dim > 4294967296:
        raise "dim trop grand (doit être < 2^32)"
else:
    dim = 40000000


# On arrange dim pour qu'elle soit un multiple de nbp
dim_local = dim // nbp
dim = dim_local * nbp


# On génère les données localement
start = time()
v_local = np.random.rand(dim_local)
end = time()
print(f"Temps de création des données pour P{rank} : {end - start} sec")


# On calcul le max & min global afin de pouvoir enuite faire les buckets
if rank == 0:
    start = time()
max_local = np.asarray([np.max(v_local)])
min_local = np.asarray([np.min(v_local)])
max_global = np.empty(1, dtype=np.double)
min_global = np.empty(1, dtype=np.double)
globCom.Allreduce([max_local, MPI.DOUBLE], [max_global, MPI.DOUBLE], op=MPI.MAX)
globCom.Allreduce([min_local, MPI.DOUBLE], [min_global, MPI.DOUBLE], op=MPI.MIN)
if rank == 0:
    end = time()
    print(f"Temps de calcul du max & min global : {end - start} sec")


# On constitue localement les buckets
start = time()

bucket_size = (max_global[0] - min_global[0]) / nbp
bucket_indices = ((v_local - min_global[0]) / bucket_size).astype(int)
bucket_indices[bucket_indices == nbp] -= 1  # Faire attention au cas de max_global

buckets = [v_local[bucket_indices == i] for i in range(nbp)]
bucket_lengths = np.array([np.array([np.sum(bucket_indices == i)]) for i in range(nbp)], dtype=np.uint32)
end = time()
print(f"Temps de constitution local des buckets pour P{rank} : {end - start} sec")


# On regroupe les buckets sur le processeurs appropriés
if rank == 0:
    start = time()

recvcounts = np.empty(nbp, dtype=np.uint32)
displacements = np.empty(nbp, dtype=np.uint32)
global_bucket_lengths = np.empty(nbp, dtype=np.uint32)
for i in range(nbp):
    globCom.Allgather([bucket_lengths[i], MPI.UINT32_T], [recvcounts, MPI.UINT32_T])
    global_bucket_lengths[i] = np.sum(recvcounts)
    if rank == i:
        local_bucket = np.empty(global_bucket_lengths[i], dtype=np.double)
        displacements = np.cumsum(recvcounts) - recvcounts
        globCom.Gatherv([buckets[i], MPI.DOUBLE], [local_bucket, recvcounts, displacements, MPI.DOUBLE], root=i)
        global_bucket_lengths[i]
    else:
        globCom.Gatherv([buckets[i], MPI.DOUBLE], None, root=i)

if rank == 0:
    end = time()
    print(f"Temps de réunion des buckets : {end - start} sec")


# On trie
start = time()
local_bucket.sort()
end = time()
print(f"Temps du sort pour le processeur {rank} : {end - start} sec")


# On regroupe sur P0 avec Gatherv
if rank == 0:
    v = np.empty(dim, dtype=np.double)
else:
    v = None

start = time()
global_displacements = np.cumsum(global_bucket_lengths) - global_bucket_lengths
globCom.Gatherv([local_bucket, MPI.DOUBLE], [v, global_bucket_lengths, global_displacements, MPI.DOUBLE], root=0)
end = time()

if rank == 0:
    print(f"Temps de regroupement des buckets sur P0 : {end - start} sec")
    global_end = time()
    print(f"Temps d'exécution totale : {global_end - global_start} sec")

# # On regroupe sur P0
# if rank == 0:
#     v = np.empty(dim, dtype=float)
#     n = len(local_bucket)
#     v[:n] = local_bucket
#     start = time()
#     for i in range(1, nbp):
#         # local_bucket.extend(globCom.recv(source=i))
#         n_local = globCom.recv(source=i)
#         globCom.Recv([v[n:n+n_local], MPI.FLOAT], source=i)
#         n += n_local
#     end = time()
#     print(f"Temps de regroupement des buckets sur P0 : {end - start} sec")
#     print(v)
#     global_end = time()
#     print(f"Temps d'exécution totale : {global_end - global_start} sec")
    
# else:
#     globCom.send(len(local_bucket), dest=0)
#     globCom.Send([local_bucket, MPI.FLOAT], dest=0)
#     # globCom.send(local_bucket, dest=0)


