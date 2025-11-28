import math
import itertools
import time
import matplotlib.pyplot as plt

# ==========================================
# 1. DEFINICIÓN DE DATOS
# ==========================================
# Diccionario con las ciudades del sur de Chile y sus coordenadas (latitud, longitud)
ciudades = {
    "Temuco": (-38.73738453399292, -72.59448229578543),
    "Valdivia": (-39.81605763783872, -73.23991062486559),
    "Puerto Montt": (-41.46940994292862, -72.93960764483167),
    "Villarrica": (-39.28287779349695, -72.22836532447117),
    "Pucón": (-39.278366182989664, -71.96905107526196),
    "Angol": (-37.802326934844054, -72.70005960112702),
    "Victoria": (-38.232155732537336, -72.35245377471217),
    "Traiguén": (-38.25002474259598, -72.66635271990164),
}

# Extraer nombres y coordenadas en listas para acceso indexado
nombres = list(ciudades.keys())
coords = list(ciudades.values())
n = len(nombres)

# ==========================================
# 2. FUNCIONES DE CÁLCULO
# ==========================================
def calcular_distancia(p1, p2):
    """Calcula la distancia Euclidiana entre dos puntos"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Construir matriz de distancias: D[i][j] = distancia entre ciudad i y ciudad j
matriz_distancias = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        matriz_distancias[i][j] = calcular_distancia(coords[i], coords[j])

# ==========================================
# 3. ALGORITMOS
# ==========================================

def busqueda_exhaustiva(nombres, matriz):
    """
    Algoritmo de búsqueda exhaustiva (Fuerza Bruta)
    Prueba todas las permutaciones posibles y retorna la ruta óptima
    Complejidad: O((n-1)!)
    
    Retorna:
    - mejor_ruta: lista de índices con la ruta óptima
    - min_distancia: distancia total de la ruta óptima
    """
    mejor_ruta = None
    min_distancia = float('inf')
    
    # Fijamos inicio en ciudad 0 para evitar contar rutas equivalentes
    for perm in itertools.permutations(range(1, n)):
        ruta_actual = [0] + list(perm) + [0]  # Ciclo cerrado: 0 -> ... -> 0
        
        # Calcular distancia total de esta permutación
        distancia_actual = 0
        for k in range(len(ruta_actual) - 1):
            distancia_actual += matriz[ruta_actual[k]][ruta_actual[k+1]]
            
        # Actualizar mejor ruta si es más corta
        if distancia_actual < min_distancia:
            min_distancia = distancia_actual
            mejor_ruta = ruta_actual
            
    return mejor_ruta, min_distancia

def vecino_mas_cercano(nombres, matriz):
    """
    Algoritmo heurístico Greedy: Vecino Más Cercano
    Desde la ciudad actual, siempre visita la ciudad no visitada más cercana
    Complejidad: O(n²) - mucho más rápido que búsqueda exhaustiva
    
    Retorna:
    - ruta: lista de índices con la ruta construida
    - distancia_total: distancia total de la ruta
    """
    no_visitadas = set(range(1, n))  # Conjunto de ciudades sin visitar (excepto la 0)
    ruta = [0]  # Iniciamos en la ciudad 0
    actual = 0
    distancia_total = 0
    
    # Visitar todas las ciudades restantes
    while no_visitadas:
        mas_cercana = None
        min_dist_local = float('inf')
        
        # Buscar la ciudad más cercana entre las no visitadas
        for vecina in no_visitadas:
            d = matriz[actual][vecina]
            if d < min_dist_local:
                min_dist_local = d
                mas_cercana = vecina
        
        # Agregar la ciudad más cercana a la ruta
        ruta.append(mas_cercana)
        no_visitadas.remove(mas_cercana)
        distancia_total += min_dist_local
        actual = mas_cercana
        
    # Retornar a la ciudad de origen para completar el ciclo
    distancia_total += matriz[actual][0]
    ruta.append(0)
    
    return ruta, distancia_total

# ==========================================
# 4. EJECUCIÓN Y COMPARACIÓN
# ==========================================
print(f"Procesando {n} ciudades...\n")

# Ejecutar algoritmo de búsqueda exhaustiva y medir tiempo
start_time = time.perf_counter()
ruta_optima, dist_optima = busqueda_exhaustiva(nombres, matriz_distancias)
end_time = time.perf_counter()
tiempo_ex = end_time - start_time

# Ejecutar algoritmo heurístico y medir tiempo
start_time = time.perf_counter()
ruta_nn, dist_nn = vecino_mas_cercano(nombres, matriz_distancias)
end_time = time.perf_counter()
tiempo_nn = end_time - start_time

# Calcular porcentaje de desviación de la heurística respecto al óptimo
gap = ((dist_nn - dist_optima) / dist_optima) * 100

# Mostrar resultados en consola
print("-" * 50)
print(f"RESULTADOS PARA {n} CIUDADES")
print("-" * 50)
print("1. BÚSQUEDA EXHAUSTIVA (Solución Óptima)")
print(f"   Ruta: {[nombres[i] for i in ruta_optima]}")
print(f"   Distancia: {dist_optima:.4f}")
print(f"   Tiempo: {tiempo_ex:.6f} seg")
print("-" * 50)
print("2. VECINO MÁS CERCANO (Heurística Greedy)")
print(f"   Ruta: {[nombres[i] for i in ruta_nn]}")
print(f"   Distancia: {dist_nn:.4f}")
print(f"   Tiempo: {tiempo_nn:.6f} seg")
print("-" * 50)
print(f"COMPARACIÓN")
print(f"   Desviación respecto al óptimo: {gap:.2f}%")
# Calcular aceleración evitando división por cero
if tiempo_nn > 0:
    velocidad = tiempo_ex / tiempo_nn
    print(f"   La heurística fue {velocidad:.1f}x más rápida.")
else:
    print("   La heurística fue N/A (tiempo muy pequeño).")
print("-" * 50)

# ==========================================
# 5. VISUALIZACIÓN COMPARATIVA
# ==========================================
def plot_ruta(ax, ruta_indices, coords, nombres, titulo, color):
    """
    Dibuja una ruta en el mapa con puntos y líneas conectoras
    """
    # Separar coordenadas en x (longitud) e y (latitud)
    x = [coords[i][1] for i in ruta_indices]
    y = [coords[i][0] for i in ruta_indices]
    
    # Trazar la ruta
    ax.plot(x, y, marker='o', color=color, linestyle='-', linewidth=2, markersize=8, alpha=0.7)
    
    # Agregar flecha de cierre del ciclo
    ax.arrow(x[-2], y[-2], x[-1]-x[-2], y[-1]-y[-2], 
             head_width=0.05, length_includes_head=True, color=color)
    
    # Etiquetar cada ciudad en el mapa
    for i in range(len(nombres)):
        ax.text(coords[i][1] + 0.05, coords[i][0] + 0.05, nombres[i], fontsize=9)
        
    ax.set_title(titulo)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True, linestyle='--', alpha=0.5)

# Crear figura con dos gráficos lado a lado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Gráfico izquierdo: solución óptima
titulo_opt = f"Solución Óptima (Búsqueda Exhaustiva)\nDistancia: {dist_optima:.2f}"
plot_ruta(ax1, ruta_optima, coords, nombres, titulo_opt, 'green')

# Gráfico derecho: solución heurística
titulo_nn = f"Heurística Vecino Más Cercano\nDistancia: {dist_nn:.2f} (Desviación: {gap:.2f}%)"
plot_ruta(ax2, ruta_nn, coords, nombres, titulo_nn, 'red')

plt.tight_layout()
plt.show()

# ==========================================
# 6. ANIMACIÓN DEL PROCESO (Bonus)
# ==========================================
# Mostrar paso a paso cómo se construye la ruta heurística
input("\nPresiona ENTER para ver la animación del algoritmo Vecino Más Cercano...")

plt.figure(figsize=(8, 8))
x_todos = [c[1] for c in coords]
y_todos = [c[0] for c in coords]

# Dibujar todas las ciudades en el mapa base
plt.scatter(x_todos, y_todos, c='blue', s=100)
for i, txt in enumerate(nombres):
    plt.annotate(txt, (x_todos[i]+0.05, y_todos[i]))
plt.title("Construcción Heurística: Paso a Paso")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.grid(True)

# Animar la construcción de la ruta mostrando cada paso
for k in range(len(ruta_nn)-1):
    origen = ruta_nn[k]
    destino = ruta_nn[k+1]
    
    x_seg = [coords[origen][1], coords[destino][1]]
    y_seg = [coords[origen][0], coords[destino][0]]
    
    # Dibujar arista y actualizar título con el desplazamiento actual
    plt.plot(x_seg, y_seg, 'r-', linewidth=2)
    plt.title(f"Paso {k+1}: Viajando de {nombres[origen]} a {nombres[destino]}...")
    plt.pause(1.0)  # Pausa de 1 segundo entre pasos

plt.title(f"Ruta Completada. Distancia Total: {dist_nn:.2f}")
plt.show()
