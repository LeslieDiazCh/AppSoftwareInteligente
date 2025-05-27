import pandas as pd
import random

# Atributos posibles
atributos = {
    'sombrero': ['sí', 'no'],
    'gafas': ['sí', 'no'],
    'altura': ['alto', 'medio', 'bajo'],
    'ropa_negra': ['sí', 'no']
}

# Lista ampliada de sospechosos
culpables = [
    'Sr. X', 'Sra. Y', 'Srta. Z', 'Dr. A',
    'Cap. Nemo', 'Ing. Ruiz', 'Agente K', 'Ms. Noir'
]

# Reglas de perfil por sospechoso
def asignar_culpable(s, g, a, r):
    if s == 'sí' and r == 'sí':
        return 'Sr. X'
    elif g == 'sí' and a == 'bajo':
        return 'Sra. Y'
    elif g == 'sí' and s == 'sí':
        return 'Srta. Z'
    elif s == 'no' and g == 'no' and a == 'alto':
        return 'Dr. A'
    elif r == 'no' and a == 'medio':
        return 'Cap. Nemo'
    elif s == 'sí' and g == 'no' and a == 'medio':
        return 'Ing. Ruiz'
    elif g == 'sí' and r == 'sí' and a == 'alto':
        return 'Agente K'
    else:
        return 'Ms. Noir'

# Generar 100 filas con lógica razonable
datos = []
for _ in range(100):
    sombrero = random.choice(atributos['sombrero'])
    gafas = random.choice(atributos['gafas'])
    altura = random.choice(atributos['altura'])
    ropa_negra = random.choice(atributos['ropa_negra'])
    culpable = asignar_culpable(sombrero, gafas, altura, ropa_negra)
    datos.append([sombrero, gafas, altura, ropa_negra, culpable])

# Crear DataFrame y exportar CSV
df = pd.DataFrame(datos, columns=['sombrero', 'gafas', 'altura', 'ropa_negra', 'culpable'])
df.to_csv('sospechosos.csv', index=False)

print("✅ Archivo 'sospechosos.csv' generado con 100 filas y 8 sospechosos.")
