# TP4

```
$ mpiexec -np 1 python3 lifegame.py flat
Temps calcul prochaine generation : 1.15e+00 sec, temps affichage : 1.93e-01 sec, temps_total : 1.35e+00
Temps total d'exécution : 13.95801854133606
```

J'ai modifié le programme afin qu'il s'arrête au bout de la 10e itération, afin de pouvoir comparer les temps de manière rigoureuse.


## Q1 : séparer affichage et calcul

Ici, on va utiliser deux processeurs. P0 se chargera de l'affichage, et P1 du calcul. En observant les chiffres ci-dessus, on peut déjà avancer que cela n'aura pas beaucoup d'effet, car le temps d'affichage semble négligeable par rapport au temps du calcul.

```
$ mpiexec -np 2 python3 q1.py flat
Temps calcul prochaine generation : 1.13e+00 sec, temps affichage : 1.87e-01 sec, temps_total : 1.31e+00
Temps total d'exécution : 12.25254487991333 sec
```

Ce n'est pas vraiment plus rapide ($S \approx 1.14$), comme on s'y attendait. On pourrait presque utiliser P0 pour faire aussi du calcul.


## Q2 : partage du calcul entre P1 et P2

On va cette fois ci aussi séparer le calcul en 2, entre P1 et P2. La séparation sera verticale, à $x=width/2$.

```
Temps calcul prochaine generation P1: 6.14e-01 sec, Temps calcul prochaine generation P2: 6.19e-01 sec, temps affichage : 2.09e-01 sec, temps_total : 8.29e-01
Temps total d'exécution : 6.933628559112549 sec
```

C'est bien deux fois plus rapide, comme on pouvait s'y attendre ! On a $S \approx 2.01$.


## Q3: partage du calcul en 4

On peut s'attendre à un speedup de 4. Il faudra juste faire attention au partage qui sera plus délicat, avec plus de ghost cells.
