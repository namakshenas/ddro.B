# Adjustable Robust Counterpart (ARC) with Affine Recourse

## Variable roles

| Variable | Type | Role |
|---|---|---|
| $x_1^{(1)}, x_2^{(1)}$ | **here-and-now** | fixed before $\xi$ is revealed; the objective and ratio constraint act on these |
| $x_1^{(2)}, x_2^{(2)}$ | **wait-and-see** | react to the realized uncertainty $\xi$ |
| $u_1, u_2$ | rule coefficients | constant part of the affine rule for $x^{(2)}$ |
| $v_1, v_2$ | rule coefficients | recourse slope — how $x^{(2)}$ adjusts per unit of $\xi$ |

**Affine decision rule (linear decision rule):**

$$
\begin{aligned}
x_1^{(2)} &= u_1 + v_1\,\xi_1 \\
x_2^{(2)} &= u_2 + v_2\,\xi_2
\end{aligned}
$$

## Where the absolute values come from

Before substituting the rule, the budget constraint carries the wait-and-see variables and an uncertainty term in $\xi \in [-1, 1]^2$:

$$
3x_1^{(1)} + 5x_2^{(1)} + 2x_1^{(2)} + 7x_2^{(2)}
     + x_1^{(1)}\,\xi_1 + x_2^{(1)}\,\xi_2 \le 15
\qquad \forall\, \xi \in [-1,1]^2
$$

Substituting $x_1^{(2)} = u_1 + v_1\xi_1$ and $x_2^{(2)} = u_2 + v_2\xi_2$, then grouping the constant part and the $\xi$-dependent part:

$$
\underbrace{\big(3x_1^{(1)} + 5x_2^{(1)} + 2u_1 + 7u_2\big)}_{\text{constant in }\xi}
     + (x_1^{(1)} + 2v_1)\,\xi_1 + (x_2^{(1)} + 7v_2)\,\xi_2 \le 15
$$

Enforcing this for the **worst-case** $\xi$ (each $\xi_i \in [-1,1]$, where $\max_{\zeta \in [-1,1]} \zeta\,e = |e|$) turns each linear $\xi$-term into its absolute value:

$$
3x_1^{(1)} + 5x_2^{(1)} + 2u_1 + 7u_2
     + \lvert x_1^{(1)} + 2v_1\rvert + \lvert x_2^{(1)} + 7v_2\rvert \le 15
$$

That is exactly the original constraint — confirming it is the **adjustable robust counterpart** under box uncertainty, with $x^{(2)}$ handled by an affine rule.

## Full formulation (ARC with affine recourse)

```math
\begin{aligned}
\max_{x_1^{(1)},\,x_2^{(1)},\,u_1,\,u_2,\,v_1,\,v_2} \quad & z = x_1^{(1)} + x_2^{(1)} \\[4pt]
\text{s.t.} \quad
& 3x_1^{(1)} + 5x_2^{(1)} + 2u_1 + 7u_2
   + \lvert x_1^{(1)} + 2v_1\rvert + \lvert x_2^{(1)} + 7v_2\rvert \le 15 \\[4pt]
& x_1^{(1)} - 2x_2^{(1)} \le 0 \qquad (\,x_1^{(1)} \le 2x_2^{(1)}\,) \\[4pt]
& x_1^{(1)},\, x_2^{(1)},\, u_1,\, u_2,\, v_1,\, v_2 \ge 0
\end{aligned}
```

where the wait-and-see variable follows the affine rule

$$
x_1^{(2)} = u_1 + v_1\,\xi_1, \qquad
x_2^{(2)} = u_2 + v_2\,\xi_2, \qquad
\xi_1, \xi_2 \in [-1, 1].
$$

> **Reading the solution.** Solving for the here-and-now variables gives $x_1^{(1)} = \tfrac{15}{7} \approx 2.143$ and $x_2^{(1)} = \tfrac{15}{14} \approx 1.071$. The optimization over $u_i, v_i$ defines the *policy* $x^{(2)}(\xi)$ that hedges the worst-case budget; the objective and the ratio constraint $x_1^{(1)} \le 2x_2^{(1)}$ act only on the here-and-now block, keeping both $x_1^{(1)}, x_2^{(1)}$ strictly positive without forcing them equal.

## Solver code

Since all variables are $\ge 0$, the arguments of the $\lvert\cdot\rvert$ terms are nonnegative and the model is fully linear; the version below keeps the `abs` literal so it stays valid if the nonnegativity bounds are later relaxed.

### Gurobi

```python
import gurobipy as gp
from gurobipy import GRB

m = gp.Model()
x11 = m.addVar(name="x_1_1")
x12 = m.addVar(name="x_1_2")
u1, u2 = m.addVar(name="u_1"), m.addVar(name="u_2")
v1, v2 = m.addVar(name="v_1"), m.addVar(name="v_2")

# free helpers for the abs arguments; t1,t2 hold the absolute values
a1 = m.addVar(lb=-GRB.INFINITY, name="a1")
a2 = m.addVar(lb=-GRB.INFINITY, name="a2")
t1, t2 = m.addVar(name="t1"), m.addVar(name="t2")
m.addConstr(a1 == x11 + 2*v1)
m.addConstr(a2 == x12 + 7*v2)
m.addGenConstrAbs(t1, a1)
m.addGenConstrAbs(t2, a2)

m.setObjective(x11 + x12, GRB.MAXIMIZE)
m.addConstr(3*x11 + 5*x12 + 2*u1 + 7*u2 + t1 + t2 <= 15)
m.addConstr(x11 <= 2*x12)

m.optimize()
print(x11.X, x12.X)
```

### CPLEX (docplex)

```python
from docplex.mp.model import Model

m = Model()
x11 = m.continuous_var(name="x_1_1")
x12 = m.continuous_var(name="x_1_2")
u1, u2 = m.continuous_var(name="u_1"), m.continuous_var(name="u_2")
v1, v2 = m.continuous_var(name="v_1"), m.continuous_var(name="v_2")

m.maximize(x11 + x12)
m.add(3*x11 + 5*x12 + 2*u1 + 7*u2 + m.abs(x11 + 2*v1) + m.abs(x12 + 7*v2) <= 15)
m.add(x11 <= 2*x12)

m.solve()
print(x11.solution_value, x12.solution_value)
```

Both return $x_1^{(1)} = \tfrac{15}{7} \approx 2.143$ and $x_2^{(1)} = \tfrac{15}{14} \approx 1.071$.

## Before running the codes

- Install `cplex`, `docplex`, and `gurobipy`
