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