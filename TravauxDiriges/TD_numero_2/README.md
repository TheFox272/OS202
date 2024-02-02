# OS202 : TD2

## Question de cours 1

### Question 1

1. P0 envoie un msg à P2
2. P2 reçoit le msg de P0
3. P2 envoie un msg à P0 & P1 envoie un msg à P2
4. P0 reçoit le msg de P2
5. P2 reçoit le msg de P1

### Question 2

1. P0 envoie un msg à P2 & P2 envoie un msg à P0
2. $\infty$ : les deux processus sont en attente de la confimation de reception de l'autre, c'est un interblocage

La probabilité d'avoie un interblocage doit être assez faible, car cet éventualité est en général oubiée dans un premier temps. Disons 10% du temps.


## Question de cours 2

### Loi d'Amdhal

La loi d'Amdhal donne :
$$
S = \frac{1}{\frac{1}{10} + \frac{9}{10 \cdot n}} = \frac{10 \cdot n}{n + 9} \underset{n\to +\infty}{\longrightarrow} 10
$$

Calculons les premiers éléments de la suite $S(n)$ :  
$S(1) = 1$  
$S(2) \approx 1.8$  
$S(3) = 2.5$  
$S(4) \approx 3.1$  
$S(5) \approx 3.6$  
$S(6) \approx 4$  
$...$  

Pour ce jeu de données, il semble raisonnable d'utiliser 4 noeuds de calcul, pour aller déjà 3 fois plus vite. Mais il faudrait faire des tests empirirques pour voir ce qui convient le mieux, sans trop perturber le CPU.


### Loi de Gustavson

On a maintenant $S(n, t_p) = 4$

La loi de Gustavson donne :
$$
S(n) = n + (1 − n) \cdot t_s \qquad \text{où} \quad t_s = 1 - t_p
$$

On nous dis que $t_p$ est alors doublé : $t_p' = 2 \cdot t_p$.\
D'où :  
$S'(n, t_p') = n + (1 − n) \cdot (1 - t_p')$  
$S'(n, t_p) = n + (1 − n) \cdot (1 - 2t_p)$  
$S'(n, t_p) = 2n + 2(1 − n) \cdot (1 - t_p) - n - (1 - n)$  
$S'(n, t_p) = 2 \cdot S(n, t_p) - 1$  
$S'(n, t_p) = 2 \cdot 4 - 1$  
$S'(n, t_p) = 7$  

On peut donc espérer une accélération maximale de 7.


## Ensemble de mandelbrot

### Question 1

Attention, on a ici partitionné par colonne plutôt que par lignes. C'est plus pratique pour utiliser la fonction Gather de MPI.

Voir `mandelbrot_partition.py`.

Pour nbp = 1 :
```
$ mpiexec -np 1 python3 mandelbrot_partition.py 
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 0: 3.57043194770813 sec
Temps pris par la fonction Gather : 0.002248525619506836 sec
Temps de constitution de l'image : 0.04791688919067383 sec
Temps d'exécution totale : 3.7215442657470703 sec
```

Pour nbp = 2 :
```
$ mpiexec -np 2 python3 mandelbrot_partition.py 
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 0: 1.9553425312042236 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 1: 1.9894976615905762 sec
Temps pris par la fonction Gather : 0.03931856155395508 sec
Temps de constitution de l'image : 0.055301666259765625 sec
Temps d'exécution totale : 2.156292200088501 sec
```
$S(2) \approx 1.7$

Pour nbp = 3 :
```
$ mpiexec -np 3 python3 mandelbrot_partition.py 
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 0: 1.3124971389770508 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 2: 1.361816167831421 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 1: 1.4645228385925293 sec
Temps pris par la fonction Gather : 0.1551220417022705 sec
Temps de constitution de l'image : 0.06777524948120117 sec
Temps d'exécution totale : 1.6421256065368652 sec
```
$S(3) \approx 2.3$

Pour nbp = 4 :
```
$ mpiexec -np 4 python3 mandelbrot_partition.py 
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 0: 1.0471241474151611 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 3: 1.0965375900268555 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 1: 1.1195943355560303 sec
Temps du calcul de l'ensemble de Mandelbrot pour le processeur 2: 1.1230363845825195 sec
Temps pris par la fonction Gather : 0.08043742179870605 sec
Temps de constitution de l'image : 0.07645988464355469 sec
Temps d'exécution totale : 1.311894178390503 sec
```
$S(4) \approx 2.8$

On observe que multiplier le nombre de processeurs par 4 nous donne un speedup inférieur à 3. On peut expliquer ce phénomène par deux facteurs:
- D'une part, le temps de rassemblement des données par la fonction Gather, qui est en fait négligeable (voir second facteur)
- D'autre part, le fait que le partitionnement ainsi produit n'est pas équitable. En effet, certaine bande contiennent de nombreux points qui divergents très rapidement, ou qui convergent dans une zone connue, et qui nécéssiteront donc beaucoup moins de calcul. Ainsi, pour la cas à 3 processeurs, on observe une différence de 0.15 sec entre les processeurs 0 et 1. On remarque que cela correspond quasiment au temps indiqué dans l'exécution de la fonction Gather par le processeur 0. Cela est dû au fait que cette fonction attend de recevoir l'ensemble des paquets avant de continuer, elle est blocante. On voit donc bien que son temps d'exécution est négligeable devant l'attente qu'entraine la différence de charge de travail entre les processeurs.


### Question 2

Voir `mandelbrot_maitre.py`  

Partage en 4 zones :
```
$ mpiexec -np 4 python3 mandelbrot_maitre.py 4
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 2: 1.1826765537261963 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 3: 1.238067388534546 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 1: 2.0785982608795166 sec
Temps de constitution de l'image : 0.05576181411743164 sec
Temps d'exécution totale : 2.2445831298828125 sec
```

Partage en 8 zones :
```
$ mpiexec -np 4 python3 mandelbrot_maitre.py 8
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 2: 1.099367380142212 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 1: 1.487701416015625 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 3: 1.6146109104156494 sec
Temps de constitution de l'image : 0.05350613594055176 sec
Temps d'exécution totale : 1.7801728248596191 sec
```

Partage en 16 zones :
```
$ mpiexec -np 4 python3 mandelbrot_maitre.py 16
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 2: 1.3399591445922852 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 3: 1.3951382637023926 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 1: 1.5331127643585205 sec
Temps de constitution de l'image : 0.0519709587097168 sec
Temps d'exécution totale : 1.694117784500122 sec
```

Partage en 32 zones :
```
$ mpiexec -np 4 python3 mandelbrot_maitre.py 32
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 3: 1.2726099491119385 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 1: 1.2927470207214355 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 2: 1.4022440910339355 sec
Temps de constitution de l'image : 0.057065486907958984 sec
Temps d'exécution totale : 1.5901401042938232 sec
```

Partage en 64 zones :
```
$ mpiexec -np 4 python3 mandelbrot_maitre.py 64
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 2: 1.4275059700012207 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 1: 1.4347436428070068 sec
Temps du calcul total de l'ensemble de Mandelbrot pour le processeur 3: 1.4790091514587402 sec
Temps de constitution de l'image : 0.05488085746765137 sec
Temps d'exécution totale : 1.6422412395477295 sec
```

Le meilleur speedup est donc atteint pour : $S(nbp=4, n=32) = 2.34$  

Ainsi, on observe bien une réduction de l'écart entre le temps de travail effectués par les différents processeurs, au fur et à mesure que l'on augmente la précision du partage. Cependant, cela semble être compensé par les temps de transferts des messages qui sont bien plus nombreux...  


## Produit matrice-vecteur

On prendra dim=4800 pour les test, afin d'avoir un différence significative :
```
$ mpiexec -np 1 python3 matvec.py 4800
Temps de création de A : 4.713960647583008 sec
Temps du calcul : 0.01736760139465332 sec
Temps d'exécution totale : 4.732148170471191 sec
```

On remarque que le temps de calcul en lui-même reste extrêmement faible, mais c'est le temps de création de la matrice A qui est important. Or, c'est la parrallélisation des tâches va justement permettre de réduire sa dimension en la séparant dnas chaque processeur.

### Question 1

Voir `matvec_colonne.py`  

Pour 2 processeurs :
```
$ mpiexec -np 2 python3 matvec_colonne.py 4800
Temps de création de A : 3.1115329265594482 sec
Temps du calcul pour le processeur 0 : 0.05671429634094238 sec
Temps du calcul pour le processeur 1 : 0.04431462287902832 sec
Temps d'exécution totale : 3.2458560466766357 sec
```

Pour 4 processeurs :
```
$ mpiexec -np 4 python3 matvec_colonne.py 4800
Temps de création de A : 1.6828110218048096 sec
Temps du calcul pour le processeur 0 : 0.05681753158569336 sec
Temps du calcul pour le processeur 3 : 0.03263521194458008 sec
Temps du calcul pour le processeur 1 : 0.02636408805847168 sec
Temps du calcul pour le processeur 2 : 0.03358793258666992 sec
Temps d'exécution totale : 1.8638427257537842 sec
```

Cette méthode nous donne permet donc d'atteindre un speedup de 2.5, ce qui n'est pas négligeable. On pourrait s'attendre à mieux, comme 4, mais il faut garder en tête qu'une partie des tâches reste non parrallélisable et doit être effectué par chaque processeur. De plus, la transmission des fragment de matrice prend elle aussi un peu de temps. Et enfin, on remarque que notre temps de calcul est horriblement long. Cela est dû au fait que l'on a pas utilisé de fonction numpy très optimisée comme dot.

### Question 2

Voir `matvec_ligne.py`  

Pour 2 processeurs :
```
$ mpiexec -np 2 python3 matvec_ligne.py 4800
Temps de création de A : 3.190264940261841 sec
Temps du calcul pour le processeur 0 : 0.014615535736083984 sec
Temps du calcul pour le processeur 1 : 0.010293960571289062 sec
Temps d'exécution totale : 3.3315634727478027 sec
```

Pour 4 processeurs :
```
$ mpiexec -np 4 python3 matvec_ligne.py 4800
Temps de création de A : 1.7314302921295166 sec
Temps du calcul pour le processeur 0 : 0.005921840667724609 sec
Temps du calcul pour le processeur 2 : 0.009278535842895508 sec
Temps du calcul pour le processeur 3 : 0.007510185241699219 sec
Temps du calcul pour le processeur 1 : 0.006373167037963867 sec
Temps d'exécution totale : 1.9064362049102783 sec
```

Cette méthode est un peu plus lente que la précédente, malgrès des temps de calcul significativement plus court ! Cela est dû au fait que la création de chaque portion de la matrice A prend plus de temps, comme si créer une nouvelle colonne était plus lourd que créer une nouvelle colonne. C'est sûrement dû à la manière dont est gérée la mémoire.
