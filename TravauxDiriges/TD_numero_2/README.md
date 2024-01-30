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
$$
\begin{align\*}
S(1) &= 1\\
S(2) &\approx 1.8\\
S(3) &= 2.5\\
S(4) &\approx 3.1\\
S(5) &\approx 3.6\\
S(6) &\approx 4\\
...
\end{align\*}
$$

Pour ce jeu de données, il semble raisonnable d'utiliser 4 noeuds de calcul, pour aller déjà 3 fois plus vite. Mais il faudrait faire des tests empirirques pour voir ce qui convient le mieux, sans trop perturber le CPU.


### Loi de Gustavson

On a maintenant $S(n, t_p) = 4$

La loi de Gustavson donne :
$$
S(n) = n + (1 − n) \cdot t_s \qquad \text{où} \quad t_s = 1 - t_p
$$

On nous dis que $t_p$ est alors doublé : $t_p' = 2 \cdot t_p$.\
D'où :
$$
\begin{align}
S'(n, t_p') &= n + (1 − n) \cdot (1 - t_p')\\
S'(n, t_p) &= n + (1 − n) \cdot (1 - 2t_p)\\
&= 2n + 2(1 − n) \cdot (1 - t_p) - n - (1 - n)\\
&= 2 \cdot S(n, t_p) - 1\\
&= 2 \cdot 4 - 1\\
&= 7
\end{align}
$$

On peut donc espérer une accélération maximale de 7.




