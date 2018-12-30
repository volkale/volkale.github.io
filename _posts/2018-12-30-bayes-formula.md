## Bayes' Formula

Let $$ (\Omega,\mathcal A, P)$$ be a probability space, and
$$X: (\Omega, \mathcal A) \to (\mathbb R^n, \mathcal{B}^n)$$ and
$$Y: (\Omega, \mathcal A) \to (\mathbb R^k, \mathcal{B}^k)$$ random variables. 
We have the decomposition

$$
P(Y, X) (A \times B)
= \int_B P(Y \in A|X=x)\,dP_X(x)
= \int_A P(X \in B|Y=y)\,dP_Y(y)
$$

Choosing $$B=B_\varepsilon(x)$$ and letting $$\varepsilon \searrow 0$$ we get, using
Lebesgue's differentiation theorem

$$
P(Y \in A|X=x)
    = \lim_{\varepsilon \searrow 0} \int_A \frac{P(X \in B_\varepsilon(x)|Y=y)}{P(X \in B_\varepsilon(x))}\,dP_Y(y)
\quad\text{for a.e. $x$.}
$$

By Lebesgue's dominated convergence theorem we get

$$
P(Y \in A|X=x) = \int_A \frac{dP_{X|Y=y}}{dP_X}(x)\,dP_Y(y)
\quad\text{for a.e. $x$.}
$$

## The density case
Now let us assume that
$$ P_(Y, X) = f \mu \otimes \nu $$ with $$\sigma$$-finite measures
$$\mu$$ and $$\nu$$. Then
$$P_{X|Y=y} = f(\cdot|y) \nu$$
and
$$P_X = f_2 \nu$$
and
$$P_Y = f_1 \mu$$. Hence,

$$
\begin{align}
\frac{dP_{X|Y=y}}{dP_X}(x)
& = \frac{f(x|y)}{f_2(x)} \\
& = \frac{f(x, y)}{f_1(y)f_2(x)}
\end{align}
$$

$$
\begin{align}
P(Y \in A|X=x)
& = \int_A
 \frac{f(x|y)}{f_2(x)} f_1(y) \,d\mu(y) \\
 & = \int_A
\frac{f(x, y)}{f_1(y)f_2(x)} f_1(y) \,d\mu(y) \\
& = \int_A f(y|x) \,d\mu(y) \\
\end{align}
$$
