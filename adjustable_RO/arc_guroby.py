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