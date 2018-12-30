## Bayes' Formula

Let $$ (\Omega,\mathcal A, P)$$ be a probability space, and
$$X: (\Omega, \mathcal A) \to (\mathbb R^n, \mathcal{B}^n)$$ and
$$Y: (\Omega, \mathcal A) \to (\mathbb R^k, \mathcal{B}^k)$$ random variables. 
We have the decomposition

$$
P_{(Y, X)} (A \times B)
= \int_B P_{Y|X=x}(A)\,dP_X(x)
= \int_A P{X|Y=y}(B)\,dP_Y(y)
$$

Choosing $$B=B_\varepsilon(x)$$ and letting $$\varepsilon \searrow 0$$ we get, using
Lebesgue's differentiation theorem

$$
P_{Y |X=x}(A)
    = \lim_{\varepsilon \searrow 0} \int_A \frac{P{X|Y=y}(B_\varepsilon(x))
    }{P_X(B_\varepsilon(x)) }\,dP_Y(y)
\quad\text{for a.e. $x$.}
$$

By Lebesgue's dominated convergence theorem we get

$$
P_{Y|X=x}(A) = \int_A \frac{dP_{X|Y=y}}{dP_X}(x)\,dP_Y(y)
\quad\text{for a.e. $x$.}
$$

On the other hand,

$$
P_{Y|X=x}(A) = \int_A 1\,dP_{Y|X=x}
= \int_A \frac{dP_{Y|X=x}}{dP_Y}(y)dP_Y(y)
\quad\text{for a.e. $x$.}
$$

From which we get

$$
\frac{dP_{X|Y=y}}{dP_X}(x) = \frac{dP_{Y|X=x}}{dP_Y}(y)
\quad\text{for a.e. $x, y$.}
$$

## The density case
Now let us assume that
$$ P_{(Y, X)} = f \mu \otimes \nu $$ with $$\sigma$$-finite measures
$$\mu$$ and $$\nu$$. Then
$$P_{X|Y=y} = f(\cdot|y) \nu$$
and
$$P_X = f_2 \nu$$
and
$$P_Y = f_1 \mu$$. Hence,

$$
\frac{dP_{X|Y=y}}{dP_X}(x)
 = \frac{f(x|y)}{f_2(x)}
 = \frac{f(x, y)}{f_1(y)f_2(x)}
$$

So the above equation reduces to the well known Bayes formula for densities

$$
 f(y|x) = \frac{f(x|y) f_1(y)}{f_2(x)}.
$$
