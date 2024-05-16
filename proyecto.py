import pyomo.environ as pyo


r = [f'r{i}' for i in range(1, 11)]  # 10 cursos
y = [f'y{i}' for i in range(1, 6)]   # 5 requisitos
c = [f'c{i}' for i in range(1, 6)]   # 5 casillas

B = {
    ('r1', 'y1'): 1, ('r1', 'y2'): 0, ('r1', 'y3'): 1, ('r1', 'y4'): 0, ('r1', 'y5'): 1,
    ('r2', 'y1'): 0, ('r2', 'y2'): 1, ('r2', 'y3'): 1, ('r2', 'y4'): 0, ('r2', 'y5'): 1,
    ('r3', 'y1'): 1, ('r3', 'y2'): 1, ('r3', 'y3'): 0, ('r3', 'y4'): 1, ('r3', 'y5'): 0,
    ('r4', 'y1'): 0, ('r4', 'y2'): 1, ('r4', 'y3'): 1, ('r4', 'y4'): 1, ('r4', 'y5'): 0,
    ('r5', 'y1'): 1, ('r5', 'y2'): 1, ('r5', 'y3'): 1, ('r5', 'y4'): 0, ('r5', 'y5'): 0,
    ('r6', 'y1'): 0, ('r6', 'y2'): 1, ('r6', 'y3'): 0, ('r6', 'y4'): 1, ('r6', 'y5'): 1,
    ('r7', 'y1'): 1, ('r7', 'y2'): 0, ('r7', 'y3'): 1, ('r7', 'y4'): 1, ('r7', 'y5'): 0,
    ('r8', 'y1'): 0, ('r8', 'y2'): 1, ('r8', 'y3'): 1, ('r8', 'y4'): 0, ('r8', 'y5'): 1,
    ('r9', 'y1'): 1, ('r9', 'y2'): 1, ('r9', 'y3'): 0, ('r9', 'y4'): 1, ('r9', 'y5'): 1,
    ('r10', 'y1'): 0, ('r10', 'y2'): 1, ('r10', 'y3'): 1, ('r10', 'y4'): 0, ('r10', 'y5'): 0
}

C = {
    ('c1', 'y1'): 1, ('c1', 'y2'): 0, ('c1', 'y3'): 1, ('c1', 'y4'): 0, ('c1', 'y5'): 0,
    ('c2', 'y1'): 0, ('c2', 'y2'): 1, ('c2', 'y3'): 0, ('c2', 'y4'): 1, ('c2', 'y5'): 0,
    ('c3', 'y1'): 1, ('c3', 'y2'): 1, ('c3', 'y3'): 0, ('c3', 'y4'): 0, ('c3', 'y5'): 1,
    ('c4', 'y1'): 0, ('c4', 'y2'): 0, ('c4', 'y3'): 1, ('c4', 'y4'): 1, ('c4', 'y5'): 1,
    ('c5', 'y1'): 1, ('c5', 'y2'): 1, ('c5', 'y3'): 1, ('c5', 'y4'): 0, ('c5', 'y5'): 0
}

# Modelo
model = pyo.ConcreteModel()

# Variables
model.a = pyo.Var(r, c, within=pyo.Binary)

# Función Objetivo
def objective_function(model):
    return sum(model.a[i, j] for i in r for j in c)
model.obj = pyo.Objective(rule=objective_function, sense=pyo.maximize)

# Restricciones

# Cada curso se asigna a lo sumo a una casilla
def course_assignment_rule(model, i):
    return sum(model.a[i, j] for j in c) <= 1
model.course_assignment = pyo.Constraint(r, rule=course_assignment_rule)

# Cada casilla contiene a lo sumo un curso
def slot_assignment_rule(model, j):
    return sum(model.a[i, j] for i in r) <= 1
model.slot_assignment = pyo.Constraint(c, rule=slot_assignment_rule)

# Un curso puede ser asignado a una casilla solo si cumple con los requisitos
def requirement_satisfaction_rule(model, i, j):
    return model.a[i, j] * (1 - sum(B[i, l] * C[j, l] for l in y)) == 0
model.requirement_satisfaction = pyo.Constraint(r, c, rule=requirement_satisfaction_rule)

# Resolver el modelo
solver = pyo.SolverFactory('glpk')
results = solver.solve(model, tee=True)

# Resultados
print("Resultados de la asignación:")
for i in r:
    for j in c:
        if pyo.value(model.a[i, j]) == 1:
            print(f"Curso {i} asignado a casilla {j}")
