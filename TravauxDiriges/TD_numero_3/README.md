# TD n°3 - parallélisation du Bucket Sort

*Ce TD peut être réalisé au choix, en C++ ou en Python*

Implémenter l'algorithme "bucket sort" tel que décrit sur les deux dernières planches du cours n°3 :

- le process 0 génère un tableau de nombres arbitraires,
- il les dispatch aux autres process,
- tous les process participent au tri en parallèle,
- le tableau trié est rassemblé sur le process 0.


Voici les résultats obtenus pour dim = 1 000 000 :

```
$ mpiexec -np 1 python3 normal_sort.py 1000000
Temps d'exécution totale : 0.32674336433410645 sec
```

Et pour la version parrallélisée :
```
$ mpiexec -np 4 python3 bucket_sort.py 1000000
Temps de création des données pour P1 : 0.00827336311340332 sec
Temps de création des données pour P0 : 0.008250236511230469 sec
Temps de création des données pour P2 : 0.008451461791992188 sec
Temps de création des données pour P3 : 0.008450984954833984 sec
Temps de calcul du max/min global : 0.0018761157989501953 sec
Temps de constitution local des buckets pour P0 : 0.32459235191345215 sec
Temps de constitution local des buckets pour P3 : 0.32845187187194824 sec
Temps de constitution local des buckets pour P1 : 0.3289196491241455 sec
Temps de constitution local des buckets pour P2 : 0.33954930305480957 sec
Temps de réunion des buckets : 0.6362795829772949 sec
Temps du sort pour le processeur 0 : 0.14658522605895996 sec
Temps du sort pour le processeur 1 : 0.1471419334411621 sec
Temps du sort pour le processeur 2 : 0.13745522499084473 sec
Temps du sort pour le processeur 3 : 0.13959813117980957 sec
Temps de regroupement des buckets sur P0 : 0.889728307723999 sec
Temps d'exécution totale : 2.0078186988830566 sec
```

On voit qu'on a bien gagné du temps sur le sort local (2 fois plus rapide), mais rien que le temps de constitution des buckets rend la parralélisation plus longue. Au final, le process a donc été beaucoup plus long.

