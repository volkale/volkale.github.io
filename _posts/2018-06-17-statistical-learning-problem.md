## The Statistical Learning Problem

Given a probability space $$ (\Omega,\mathcal A, P)$$ with unknown probability measure $$P$$.
Consider a function space $$\mathcal F$$ and a *loss function* $$\mathcal L:\Omega\times \mathcal F \to \mathbb R$$. 
We want to minimize the *risk functional* $$\mathcal R$$, given by

$$
\mathcal R(f):=\int \mathcal L(\omega,f)\,dP(\omega).
$$

The main difficulty arises from the fact that $$P$$ is unknown.


## Supervised Learning
A special case of the learning problem arises when we consider th following situation:


Here we are given two random variables:
the *input* $$X: (\Omega,\mathcal A) \to (\mathcal X, \mathcal A_{\mathcal X})$$
and the *output* $$Y: (\Omega,\mathcal A) \to (\mathcal Y,\mathcal A_{\mathcal Y})$$
($$\mathcal A_{\mathcal Y}$$ countably generated).
Then we can consider the space
$$\mathcal Z = \mathcal X\times \mathcal Y$$ with the push forward measure
$$(X,Y)(P)= P_{(X,Y)}=P_X\otimes K$$. Here $$K$$ denotes the regular conditional probability,
i.e. $$K(x,A)=P(Y\in A|X=x)$$.
Hence, we may write

$$
\mathcal R(f)=\int_{\mathcal X} \int_{\mathcal Y} \mathcal L(x,y,f)K(x,dy)\,dP_X(x).
$$

A measurable function $$f^*:\mathcal X \to \mathcal Y$$ such that

$$
\mathcal R(f^*) = \inf\{\mathcal R(f):f:(\mathcal X,\mathcal A_{\mathcal X})\to (\mathcal Y,\mathcal A_{\mathcal Y})\}
$$

is called *Bayes predictor*.


### Least Squares:
($$\mathcal Y$$ is an inner product space, e.g. $$\mathcal Y = \mathbb R^n$$)
$$\mathcal L(x,y,f)=|y-f(x)|^2$$, *$$L^2$$-loss*.
The function $$\eta(x):=E[Y|X=x]$$ is called *regression function*.
We have

$$
\mathcal R(f)
=E[ |Y-f(X)|^2]=E[ |Y-f(X)\pm E[Y|X]|^2 ] .
$$

Using that

\begin{align}
E\left[ (Y-E[Y|X])\cdot (f(X)-E[Y|X]) \right]
&=E\left[E[ (Y-E[Y|X])\cdot (f(X)-E[Y|X])|X]\right] \\\\
&=E\left[(f(X)-E[Y|X])\cdot E[ (Y-E[Y|X])|X]\right]\\\\
&=E\left[(f(X)-E[Y|X])\cdot 0\right] =0,
\end{align}

we obtain

$$
\mathcal R(f) = E[ |Y-\eta(X)|^2] + E[ |f(X)- \eta(X)|^2]
$$

Hence, the regression function $$\eta$$ is a Bayes predictor.
Also note here that we can always write

$$
Y = \eta(X) + \varepsilon
$$

where $$\varepsilon = Y-\eta(X)$$ is mean independent of $$X$$,
i.e. $$E[h(X)\varepsilon]=0$$ for any function $$h(X)$$.

With this decomposition we can rewrite the above equation as

$$
\mathcal R(f) = Var(\varepsilon) + \int_{\mathcal X} |f(x)- \eta(x)|^2\,dP_X(x)
$$

We see that the $$L^2$$-risk of an arbitrary estimator $$f$$ is close to optimal
if and only if the (squared) $$L^2$$-norm
$$E[ |f(X)- \eta(X)|^2]=\int_{\mathcal X} |f(x)- \eta(x)|^2\,dP_X(x)$$ is close to zero.


## Bias-Variance Tradeoff
We can decompose the squared $$L^2$$-distance $$E[ |f(X)- \eta(X)|^2]$$ into to components as follows:

\begin{align}
E[ |f(X)- \eta(X)|^2]
&=E[ |f(X)-E[f(X)]|^2] + E[ |E[f(X)]-\eta(X)|^2] \\\\
&\quad +2 \underbrace{E[ (f(X)-E[f(X)])}_{=0}\cdot (E[f(X)]-\eta(X))] \\\\
&=E[ |f(X)-E[f(X)]|^2] + E[ |E[f(X)]-\eta(X)|^2] \\\\
&=\text{Varianz} + \text{Bias}
\end{align}

regularization -> stability
