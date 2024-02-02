from mandelbrot import MandelbrotSet
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI
import sys


globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

if rank == 0:
    global_start = time()
    
# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

# On va partitionner par en n colonnes
argv = sys.argv
if len(argv) > 1:
    n = int(sys.argv[1])
else:
    n = 32  # il faut une puissance de 2, afin de diviser 1024
local_width = width // n
width = local_width * n  # necessary if width is not a multiple of n

# On définit les échelles
scaleX = 3./width
scaleY = 2.25/height

# On initialise la convergence locale pour les processeurs esclaves, et aussi pour le maître (ça lui servira de buffer de réception)
local_convergence = np.empty((local_width, height), dtype=np.double)

# Seul le maître à besoin du mandelbrot complet
if rank == 0:
    global_convergence = np.empty((width, height), dtype=np.double)

if rank == 0:
    # On créer une liste contenant la partie sur laquelle travaille chaque esclave
    slave_works = np.empty(nbp-1, dtype=np.uint8)
    work_achieved = 0
    work_in_progress = 0

    for i in range(nbp-1):
        # globCom.send(i, dest=i+1)  # they will already know what they have to begin with
        slave_works[i] = i
        work_in_progress += 1
    
    stat : MPI.Status = MPI.Status()
    while work_in_progress != 0:
        globCom.Recv([local_convergence, MPI.DOUBLE], status=stat)
        slave = stat.source
        i_work = slave_works[slave-1]
        work_achieved += 1
        work_in_progress -= 1

        if work_achieved + work_in_progress < n:
            globCom.isend(work_achieved + work_in_progress, dest=slave)
            slave_works[slave-1] = work_achieved + work_in_progress
            work_in_progress += 1
        else:
            globCom.isend(-1, dest=slave)
        
        global_convergence[i_work * local_width:(i_work+1)*local_width,:] = local_convergence
    
    # Constitution de l'image résultante
    start = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(global_convergence.T)*255))
    end = time()
    print(f"Temps de constitution de l'image : {end - start} sec")
    image.show()

    global_end = time()
    print(f"Temps d'exécution totale : {global_end - global_start} sec")

else:
    start = time()
    work = rank - 1

    while work != -1:
        # Calcul d'une fraction de l'ensemble de mandelbrot
        for y in range(height):
            for x in range(local_width):
                c = complex(-2. + scaleX*(x + work * local_width), -1.125 + scaleY * y)
                local_convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
        
        globCom.Send([local_convergence, MPI.DOUBLE], dest=0)
        work = globCom.recv(source=0)

    end = time()
    print(f"Temps du calcul total de l'ensemble de Mandelbrot pour le processeur {globCom.rank}: {end - start} sec")
