import pandas as pd

df=pd.read_csv('data/reservaciones.csv')
resenas=pd.read_csv('data/resenas.csv')

#Consultas

#1. Horas picos
print(1)
print(df['hora_inicio'].value_counts().head(10))

#2. Reservaciones por dia
print(2)
print(df.groupby('fecha').size())

# 3. Total por estado
print(3)
print(df['estado'].value_counts())

# 4. Clientes con más reservaciones
print(4)
print(df['nombre_cliente'].value_counts())

# 5. Mesas más utilizadas
print(5)
print(df['numero_mesa'].value_counts())

# 6. Tiempo promedio de estancia
print(6)
df['hora_inicio'] = pd.to_datetime(df['hora_inicio'], format='%H:%M')
df['hora_fin'] = pd.to_datetime(df['hora_fin'], format='%H:%M')
df['duracion'] = df['hora_fin'] - df['hora_inicio']
print(df['duracion'].mean())

# 7. Promedio de personas

print(df['numero_personas'].mean())

# 8. Reservaciones por número de personas
print(df.groupby('numero_personas').size())

# 9. No-shows
print(df[df['estado'] == 'no_show'].shape[0])

# 10. Por día y estado
print(df.groupby(['fecha', 'estado']).size())

# 11. Promedio calificación
print(resenas['calificacion'].mean())