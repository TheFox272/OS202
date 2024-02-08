# TD n°3 - parallélisation du Bucket Sort

*Ce TD peut être réalisé au choix, en C++ ou en Python*

Implémenter l'algorithme "bucket sort" tel que décrit sur les deux dernières planches du cours n°3 :

- le process 0 génère un tableau de nombres arbitraires,
- il les dispatch aux autres process,
- tous les process participent au tri en parallèle,
- le tableau trié est rassemblé sur le process 0.


Voici les résultats obtenus pour dim = 40 000 000 :

```
$ mpiexec -np 1 python3 normal_sort.py 40000000
Temps du sort : 4.363286256790161 sec
Temps d'exécution totale : 4.6629157066345215 sec
```

Et pour la version parrallélisée :
```
$ mpiexec -np 4 python3 bucket_sort.py 40000000
Temps de création des données pour P0 : 0.21884560585021973 sec
Temps de création des données pour P1 : 0.22470331192016602 sec
Temps de création des données pour P2 : 0.22818875312805176 sec
Temps de création des données pour P3 : 0.22928857803344727 sec
Temps de calcul du max & min global : 0.051528215408325195 sec
Temps de constitution local des buckets pour P1 : 0.6919729709625244 sec
Temps de constitution local des buckets pour P3 : 0.6936190128326416 sec
Temps de constitution local des buckets pour P2 : 0.6960113048553467 sec
Temps de constitution local des buckets pour P0 : 0.703218936920166 sec
Temps de réunion des buckets : 0.06903791427612305 sec
Temps du sort pour le processeur 1 : 1.0459797382354736 sec
Temps du sort pour le processeur 0 : 1.0647923946380615 sec
Temps du sort pour le processeur 3 : 1.0567286014556885 sec
Temps du sort pour le processeur 2 : 1.0854144096374512 sec
Temps de regroupement des buckets sur P0 : 0.10318899154663086 sec
Temps d'exécution totale : 2.2109642028808594 sec
```

On a donc un speedup de $2.1$. On voit qu'on a gagné beaucoup de temps au niveau du sort (local), sur lequel on a un speedup de $6.2$ ! Cependant, on perd beaucoup de cet avantage lors de la constitution des buckets, qui est du même ordre de grandeur. Le regroupement des buckets sur P0 prend lui aussi un peu de temps. Mais globalement c'est satisfaisant. Et surtout, ça semble bien passer à l'échelle.


