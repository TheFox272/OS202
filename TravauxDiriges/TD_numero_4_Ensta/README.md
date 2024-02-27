# TP4

```
$ mpiexec -np 1 python3 lifegame.py flat
Temps calcul prochaine generation : 1.12e+00 sec, temps affichage : 1.73e-01 sec, temps_total : 1.30e+00
```

J'ai modifié le programme afin qu'il s'arrête au bout de la 10e itération, afin de pouvoir comparer les temps de manière rigoureuse.


## Q1 : séparer affichage et calcul

```
$ mpiexec -np 2 python3 q1.py flat
Temps calcul prochaine generation : 1.09e+00 sec, temps affichage : 1.93e-01 sec, temps_total : 1.28e+00
```

Ce n'est pas vraiment plus rapide, et c'est justifié par le fait que le temps d'affichage est négligeable par rapport au temps du calcul. On pourrait presque utiliser P0 pour faire aussi du calcul.


## Q2 : partage du calcul entre P1 et P2

```
Temps calcul prochaine generation P1: 7.52e-01 sec, Temps calcul prochaine generation P2: 7.26e-01 sec, temps affichage : 2.37e-01 sec, temps_total : 9.90e-01
```

C'est bien deux fois plus rapide, comme on pouvait s'y attendre ! On a $S \approx 1.3$. 


## Q3: partage du calcul 

On peut s'attendre à un speedup de 4. Il faudra juste faire attention au partage qui sera plus délicat, avec plus de ghost cells.
