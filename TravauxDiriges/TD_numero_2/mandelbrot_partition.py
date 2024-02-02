from mandelbrot import MandelbrotSet
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI


globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

if rank == 0:
    global_start = time()

# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

# On va partitionner par colonne, c'est plus pratique pour le Gather
local_width = width // nbp
width = local_width * nbp  # necessary if width is not a multiple of nbp

# On définit les échelles
scaleX = 3./width
scaleY = 2.25/height

# On initialise la convergence locale
local_convergence = np.empty((local_width, height), dtype=np.double)

# Seul P0 aura le mandelbrot complet
if rank == 0:
    global_convergence = np.empty((width, height), dtype=np.double)
else:
    global_convergence = None

# Calcul de la fraction (correspondante au rank) de l'ensemble de mandelbrot
start = time()
for y in range(height):
    for x in range(local_width):
        c = complex(-2. + scaleX*(x + rank * local_width), -1.125 + scaleY * y)
        local_convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
end = time()
print(f"Temps du calcul de l'ensemble de Mandelbrot pour le processeur {globCom.rank}: {end - start} sec")

# On réunit tout dans P0
if rank == 0:
    start = time()
globCom.Gather(local_convergence, global_convergence, root=0)
if rank == 0:
    end = time()
    print(f"Temps pris par la fonction Gather : {end - start} sec")

if rank == 0:
    # Constitution de l'image résultante
    start = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(global_convergence.T)*255))
    end = time()
    print(f"Temps de constitution de l'image : {end - start} sec")
    image.show()

    global_end = time()
    print(f"Temps d'exécution totale : {global_end - global_start} sec")
