import pyomo.environ as pyo

# Conjuntos
r = ['r1', 'r2', 'r3']  # Cursos
y = ['y1', 'y2']        # Requisitos
c = ['c1', 'c2']        # Casillas

# Parámetros
B = {
    ('r1', 'y1'): 1,
    ('r1', 'y2'): 1,
    ('r2', 'y1'): 0,
    ('r2', 'y2'): 1,
    ('r3', 'y1'): 1,
    ('r3', 'y2'): 0
}
C = {
    ('c1', 'y1'): 1,
    ('c1', 'y2'): 0,
    ('c2', 'y1'): 0,
    ('c2', 'y2'): 1
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
