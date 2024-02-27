from lifegame import *
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

pg.init()
dico_patterns = { # Dimension et pattern dans un tuple
    'blinker' : ((5,5),[(2,1),(2,2),(2,3)]),
    'toad'    : ((6,6),[(2,2),(2,3),(2,4),(3,3),(3,4),(3,5)]),
    "acorn"   : ((100,100), [(51,52),(52,54),(53,51),(53,52),(53,55),(53,56),(53,57)]),
    "beacon"  : ((6,6), [(1,3),(1,4),(2,3),(2,4),(3,1),(3,2),(4,1),(4,2)]),
    "boat" : ((5,5),[(1,1),(1,2),(2,1),(2,3),(3,2)]),
    "glider": ((100,90),[(1,1),(2,2),(2,3),(3,1),(3,2)]),
    "glider_gun": ((200,100),[(51,76),(52,74),(52,76),(53,64),(53,65),(53,72),(53,73),(53,86),(53,87),(54,63),(54,67),(54,72),(54,73),(54,86),(54,87),(55,52),(55,53),(55,62),(55,68),(55,72),(55,73),(56,52),(56,53),(56,62),(56,66),(56,68),(56,69),(56,74),(56,76),(57,62),(57,68),(57,76),(58,63),(58,67),(59,64),(59,65)]),
    "space_ship": ((25,25),[(11,13),(11,14),(12,11),(12,12),(12,14),(12,15),(13,11),(13,12),(13,13),(13,14),(14,12),(14,13)]),
    "die_hard" : ((100,100), [(51,57),(52,51),(52,52),(53,52),(53,56),(53,57),(53,58)]),
    "pulsar": ((17,17),[(2,4),(2,5),(2,6),(7,4),(7,5),(7,6),(9,4),(9,5),(9,6),(14,4),(14,5),(14,6),(2,10),(2,11),(2,12),(7,10),(7,11),(7,12),(9,10),(9,11),(9,12),(14,10),(14,11),(14,12),(4,2),(5,2),(6,2),(4,7),(5,7),(6,7),(4,9),(5,9),(6,9),(4,14),(5,14),(6,14),(10,2),(11,2),(12,2),(10,7),(11,7),(12,7),(10,9),(11,9),(12,9),(10,14),(11,14),(12,14)]),
    "floraison" : ((40,40), [(19,18),(19,19),(19,20),(20,17),(20,19),(20,21),(21,18),(21,19),(21,20)]),
    "block_switch_engine" : ((400,400), [(201,202),(201,203),(202,202),(202,203),(211,203),(212,204),(212,202),(214,204),(214,201),(215,201),(215,202),(216,201)]),
    "u" : ((200,200), [(101,101),(102,102),(103,102),(103,101),(104,103),(105,103),(105,102),(105,101),(105,105),(103,105),(102,105),(101,105),(101,104)]),
    "flat" : ((200,400), [(80,200),(81,200),(82,200),(83,200),(84,200),(85,200),(86,200),(87,200), (89,200),(90,200),(91,200),(92,200),(93,200),(97,200),(98,200),(99,200),(106,200),(107,200),(108,200),(109,200),(110,200),(111,200),(112,200),(114,200),(115,200),(116,200),(117,200),(118,200)])
}

argv = sys.argv
if len(argv) > 1:
    choice = sys.argv[1]
else:
    choice = "flat"

resx = 800
resy = 800
print(f"Pattern initial choisi : {choice}")
print(f"resolution ecran : {resx,resy}")
try:
    init_pattern = dico_patterns[choice]
except KeyError:
    print("No such pattern. Available ones are:", dico_patterns.keys())
    exit(1)

size = list(init_pattern[0])
points = list(init_pattern[1])
x_step = size[0] // 2
ghost_step = 1
if rank == 0:   
    grid = Grille(*init_pattern)
    appli = App((resx, resy), grid)
    times = np.empty(2 + 2 * (nbp-1), dtype=np.double)
    recvcounts = np.empty(nbp, dtype=np.uint32)
    displacements = np.empty(nbp, dtype=np.uint32)
    globCom.Gather([np.array([0], dtype=np.uint32), MPI.UINT32_T], [recvcounts, MPI.UINT32_T], root=0)
    displacements = np.cumsum(recvcounts) - recvcounts
else:
    new_points = []
    if rank == 1:
        for p in points:
            if p[0] > x_step:
                if p[0] == size[0]-1:
                    new_points.append((0, p[1]))
            else:
                new_points.append((p[0]+1, p[1]))
    elif rank == 2:
        for p in points:
            if p[0] < x_step-1:
                if p[0] == 0:
                    new_points.append((x_step + 1, p[1]))
            else:
                new_points.append((p[0] - x_step + 1, p[1]))
    
    size[0] = x_step + 2 * ghost_step
    grid = Grille(tuple(size), new_points)
    times = np.empty(2, dtype=np.double)
    globCom.Gather([np.array([size[1]*(size[0]-2*ghost_step)], dtype=np.uint32), MPI.UINT32_T], None, root=0)


stop_at_cycle = 10
for cycle in range(stop_at_cycle):
    if rank in [1, 2]:
        times[0] = time()
        diff = grid.compute_next_iteration()
        times[1] = time()
        globCom.Gather([times, MPI.DOUBLE], None, root=0)

        globCom.Gatherv([np.ascontiguousarray(grid.cells[ghost_step:-ghost_step, :]), MPI.UINT8_T], None, root=0)
        
        recv_buffer = np.empty(size[1], dtype=np.uint8)

        globCom.Recv([recv_buffer, MPI.UINT8_T], source=0)
        grid.cells[0,:] = recv_buffer
        globCom.Recv([recv_buffer, MPI.UINT8_T], source=0)
        grid.cells[-1,:] = recv_buffer

    elif rank == 0:
        globCom.Gather([times[:2], MPI.DOUBLE], [times, MPI.DOUBLE], root=0)
        local = np.empty(0, dtype=np.uint8)
        globCom.Gatherv([local, MPI.UINT8_T], [grid.cells, recvcounts, displacements, MPI.UINT8_T], root=0)

        globCom.Send([np.ascontiguousarray(grid.cells[-ghost_step, :]), MPI.UINT8_T], dest=1)
        globCom.Send([np.ascontiguousarray(grid.cells[x_step, :]), MPI.UINT8_T], dest=1)
        
        globCom.Send([np.ascontiguousarray(grid.cells[x_step-ghost_step, :]), MPI.UINT8_T], dest=2)
        globCom.Send([np.ascontiguousarray(grid.cells[0, :]), MPI.UINT8_T], dest=2)

        times[0] = time()
        appli.draw()
        times[1] = time()
        print(f"Temps calcul prochaine generation P1: {times[3]-times[2]:2.2e} sec, Temps calcul prochaine generation P2: {times[5]-times[4]:2.2e} sec, temps affichage : {times[1]-times[0]:2.2e} sec, temps_total : {times[1]-times[2]:2.2e}\r", end='')

if rank == 0:
    print(f"Temps calcul prochaine generation P1: {times[3]-times[2]:2.2e} sec, Temps calcul prochaine generation P2: {times[5]-times[4]:2.2e} sec, temps affichage : {times[1]-times[0]:2.2e} sec, temps_total : {times[1]-times[2]:2.2e}")
pg.quit()

