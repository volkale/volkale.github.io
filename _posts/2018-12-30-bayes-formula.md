## Bayes' Formula

Let $$ (\Omega,\mathcal A, P)$$ be a probability space, and
$X: (\Omega, \mathcal A) \to (\mathbb R^n, \mathcal{B}^n)$ and
$Y: (\Omega, \mathcal A) \to (\mathbb R^k, \mathcal{B}^k)$ random variables. 
We have the decomposition

$$
P(X, Y) (A \times B)
= \int_B P(X \in A|Y=y)\,dP_Y(y)
= \int_A P(Y \in B|X=x)\,dP_X(x)
$$

Choosing $B=B_\varepsilon(y)$ and letting $\varepsilon \searrow 0$ we get, using
Lebesgue's Differentiation Theorem

$$
P(X \in A|Y=y) = \lim_{\varepsilon \searrow 0} \int_A \frac{P(Y \in B_\varepsilon(y)|X=x)}{P(Y \in B_\varepsilon(y))}\,dP_X(x)
\quad\text{for a.e. $y$.}
$$

By Lebesgue's dominated convergence theorem we get

$$
P(X \in A|Y=y) = \int_A \frac{dP_{Y|X=x}}{dP_Y}(y)\,dP_X(x)
\quad\text{for a.e. $y$.}
$$