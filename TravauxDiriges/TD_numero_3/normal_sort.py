
import numpy as np
import sys
from time import time
import random as rd


global_start = time()

# Dimention du problème (mis en argument ou pas)
argv = sys.argv
if len(argv) > 1:
    dim = int(sys.argv[1])
else:
    dim = 40000000

v = np.random.rand(dim)

# On trie
start = time()
v.sort()
end = time()
print(f"Temps du sort : {end - start} sec")

global_end = time()
print(f"Temps d'exécution totale : {global_end - global_start} sec")
