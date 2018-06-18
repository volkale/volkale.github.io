# The Statistical Learning Problem

Given a probability space $$ (\Omega,\mathcal A, P)$$ with unknown probability measure $$P$$.
Consider a function space $$\mathcal F$$ and a *loss function* $$\mathcal L:\Omega\times \mathcal F \to \mathbb R$$. 
We want to minimize the
*risk functional* $$\mathcal R$$, given by

$$
\mathcal R(f):=\int \mathcal L(\omega,f)\,dP(\omega).
$$

The main difficulty arises from the fact that $$P$$ is unknown.
