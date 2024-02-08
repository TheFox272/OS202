# TD n°3 - parallélisation du Bucket Sort

*Ce TD peut être réalisé au choix, en C++ ou en Python*

Implémenter l'algorithme "bucket sort" tel que décrit sur les deux dernières planches du cours n°3 :

- le process 0 génère un tableau de nombres arbitraires,
- il les dispatch aux autres process,
- tous les process participent au tri en parallèle,
- le tableau trié est rassemblé sur le process 0.


Voici les résultats obtenus pour dim = 10 000 000 :

```
$ mpiexec -np 1 python3 normal_sort.py 10000000
Temps d'exécution totale : 3.9714250564575195 sec
```

Et pour la version parrallélisée :
```
$ mpiexec -np 4 python3 bucket_sort.py 10000000
Temps de création des données pour P1 : 0.05756568908691406 sec
Temps de création des données pour P2 : 0.05965852737426758 sec
Temps de création des données pour P0 : 0.059648990631103516 sec
Temps de création des données pour P3 : 0.05979156494140625 sec
Temps de calcul du max/min global : 0.011668920516967773 sec
Temps de constitution local des buckets pour P0 : 1.773460865020752 sec
Temps de constitution local des buckets pour P1 : 1.7751903533935547 sec
Temps de constitution local des buckets pour P3 : 1.7759759426116943 sec
Temps de constitution local des buckets pour P2 : 1.8115863800048828 sec
Temps de réunion des buckets : 6.782710075378418 sec
Temps du sort pour le processeur 0 : 2.136425495147705 sec
Temps du sort pour le processeur 1 : 2.082073450088501 sec
Temps du sort pour le processeur 2 : 2.067537307739258 sec
Temps du sort pour le processeur 3 : 2.1634538173675537 sec
Temps de regroupement des buckets sur P0 : 8.780912637710571 sec
Temps d'exécution totale : 19.545241355895996 sec
```

On voit qu'on a bien gagné du temps sur le sort local (2 fois plus rapide), mais le problème réside dans l'envoi et la réception des listes qui sont gigantesque. 

