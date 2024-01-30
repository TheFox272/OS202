# OS202 : TD2

# Question de cours 1

1)  - P0 envoie un msg à P2
    - P2 reçoit le msg de P0
    - P2 envoie un msg à P0 & P1 envoie un msg à P2
    - P0 reçoit le msg de P2
    - P2 reçoit le msg de P1

2)  - P0 envoie un msg à P2 & P2 envoie un msg à P0
    - les deux processus sont en attente de la confimation de reception de l'autre, c'est un interblocage

La probabilité d'avoie un interblocage doit être assez faible, car cet éventualité est en général oubiée dans un premier temps. Disons 10% du temps.


# Question de cours 2

$$
\text{speedup} = \frac{1}{\frac{1}{10} + \frac{9}{10 \cdot n}} = \frac{10 \cdot n}{n + 9} \underset{n\to +\infty}{\longrightarrow} 10
$$



