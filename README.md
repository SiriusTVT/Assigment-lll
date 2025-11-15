# Disk Scheduling Algorithms Implementation

## 📋 Descripción del Proyecto

Este proyecto implementa tres algoritmos de planificación de disco (disk scheduling) en Python:
- **FCFS** (First Come First Served)
- **SCAN**
- **C-SCAN** (Circular SCAN)

El programa genera 1000 solicitudes aleatorias en un disco de 5000 cilindros y compara el rendimiento de los tres algoritmos mostrando el movimiento total del cabezal y visualizaciones gráficas.

---

## 📝 1. Revisión Conceptual (20%)

### Pregunta 1: Cálculo de Seek Time

**Solicitudes:** 10, 22, 20, 2, 40, 6, 38  
**Posición inicial:** 20  
**Costo por movimiento:** 6 ms por cilindro

#### a) FCFS (First Come First Served)
```
Secuencia: 20 → 10 → 22 → 20 → 2 → 40 → 6 → 38

Movimientos:
- 20 → 10: |20-10| = 10 cilindros
- 10 → 22: |10-22| = 12 cilindros
- 22 → 20: |22-20| = 2 cilindros
- 20 → 2: |20-2| = 18 cilindros
- 2 → 40: |2-40| = 38 cilindros
- 40 → 6: |40-6| = 34 cilindros
- 6 → 38: |6-38| = 32 cilindros

Total: 146 cilindros × 6 ms = 876 ms
```

#### b) SSTF (Shortest Seek Time First)
```
Secuencia: 20 → 20 → 22 → 10 → 6 → 2 → 38 → 40

Movimientos:
- 20 → 20: |20-20| = 0 cilindros
- 20 → 22: |20-22| = 2 cilindros
- 22 → 10: |22-10| = 12 cilindros
- 10 → 6: |10-6| = 4 cilindros
- 6 → 2: |6-2| = 4 cilindros
- 2 → 38: |2-38| = 36 cilindros
- 38 → 40: |38-40| = 2 cilindros

Total: 60 cilindros × 6 ms = 360 ms
```

#### c) SCAN (Elevator - inicialmente hacia arriba)
```
Solicitudes ordenadas: 2, 6, 10, 20, 22, 38, 40
Posición inicial: 20, dirección: ↑ (arriba)

Secuencia: 20 → 20 → 22 → 38 → 40 → 10 → 6 → 2

Movimientos:
- 20 → 20: |20-20| = 0 cilindros
- 20 → 22: |20-22| = 2 cilindros
- 22 → 38: |22-38| = 16 cilindros
- 38 → 40: |38-40| = 2 cilindros
- 40 → 10: |40-10| = 30 cilindros
- 10 → 6: |10-6| = 4 cilindros
- 6 → 2: |6-2| = 4 cilindros

Total: 58 cilindros × 6 ms = 348 ms
```

**Resultado:** SCAN es el más eficiente con 348 ms, seguido de SSTF (360 ms) y FCFS (876 ms).

---

### Pregunta 2: Distancia Total en Cilindros

**Disco:** 0 a 4999  
**Posición inicial:** 2150  
**Cola FIFO:** 2069, 1212, 2296, 2800, 544, 1618, 356, 1523, 4965, 3681

#### a) FCFS
```
Secuencia: 2150 → 2069 → 1212 → 2296 → 2800 → 544 → 1618 → 356 → 1523 → 4965 → 3681

Movimientos:
- 2150 → 2069: |2150-2069| = 81
- 2069 → 1212: |2069-1212| = 857
- 1212 → 2296: |1212-2296| = 1084
- 2296 → 2800: |2296-2800| = 504
- 2800 → 544: |2800-544| = 2256
- 544 → 1618: |544-1618| = 1074
- 1618 → 356: |1618-356| = 1262
- 356 → 1523: |356-1523| = 1167
- 1523 → 4965: |1523-4965| = 3442
- 4965 → 3681: |4965-3681| = 1284

Total: 13,011 cilindros
```

#### b) SCAN (asumiendo dirección inicial hacia arriba)
```
Solicitudes ordenadas: 356, 544, 1212, 1523, 1618, 2069, 2296, 2800, 3681, 4965
Posición inicial: 2150, dirección: ↑

Hacia arriba: 2150 → 2296 → 2800 → 3681 → 4965 → 4999 (final)
Hacia abajo: 4999 → 2069 → 1618 → 1523 → 1212 → 544 → 356

Movimientos:
- 2150 → 2296: 146
- 2296 → 2800: 504
- 2800 → 3681: 881
- 3681 → 4965: 1284
- 4965 → 4999: 34 (hasta el final)
- 4999 → 2069: 2930
- 2069 → 1618: 451
- 1618 → 1523: 95
- 1523 → 1212: 311
- 1212 → 544: 668
- 544 → 356: 188

Total: 7,492 cilindros
```

#### c) C-SCAN (asumiendo dirección inicial hacia arriba)
```
Hacia arriba: 2150 → 2296 → 2800 → 3681 → 4965 → 4999
Salto circular: 4999 → 0
Desde el inicio: 0 → 356 → 544 → 1212 → 1523 → 1618 → 2069

Movimientos:
- 2150 → 2296: 146
- 2296 → 2800: 504
- 2800 → 3681: 881
- 3681 → 4965: 1284
- 4965 → 4999: 34
- 4999 → 0: 4999 (salto circular)
- 0 → 356: 356
- 356 → 544: 188
- 544 → 1212: 668
- 1212 → 1523: 311
- 1523 → 1618: 95
- 1618 → 2069: 451

Total: 9,917 cilindros
```

**Resultado:** SCAN es el más eficiente con 7,492 cilindros, seguido de C-SCAN (9,917) y FCFS (13,011).

---

### Pregunta 3: ¿Por qué C-SCAN es mejor que el Elevator tradicional?

**Respuesta:**

C-SCAN es mejor que el Elevator tradicional (SCAN) porque ofrece **tiempos de espera más uniformes y justos** para todas las solicitudes.

**Razones principales:**

1. **Equidad en el servicio:** En SCAN, las solicitudes ubicadas en el centro del disco tienen ventaja porque el cabezal pasa por ellas dos veces (ida y vuelta), mientras que las de los extremos solo son atendidas una vez. C-SCAN elimina este sesgo al moverse siempre en una sola dirección.

2. **Predecibilidad:** Con C-SCAN, todas las solicitudes saben que serán atendidas en la próxima "vuelta" del cabezal, lo que hace más predecible el tiempo de espera máximo.

3. **Evita la inanición del centro:** En sistemas con alta carga, SCAN puede favorecer continuamente las solicitudes del centro del disco. C-SCAN garantiza que todas las posiciones del disco reciban atención uniforme.

4. **Mejor para cargas asimétricas:** Si las solicitudes no están distribuidas uniformemente, C-SCAN maneja mejor esta situación al no hacer "ida y vuelta".

**Analogía:** Es como una línea de autobús circular que siempre va en la misma dirección vs. un autobús que va y viene - el circular es más justo porque todos saben exactamente cuándo pasará de nuevo.

---

## 🎯 Características Principales

### 1. **Algoritmos Implementados**

#### FCFS (First Come First Served)
- Procesa las solicitudes en el orden exacto que llegan
- **Ventaja**: Simple de implementar
- **Desventaja**: Puede causar mucho movimiento del cabezal
- **Fórmula**: Movimiento total = Σ|posición_actual - siguiente_solicitud|

#### SCAN
- Mueve el cabezal en una dirección hasta alcanzar el final del disco
- Luego se invierte la dirección y atiende las solicitudes pendientes
- **Ventaja**: Reduce el tiempo de espera máximo
- **Funcionamiento**:
  1. Ordena todas las solicitudes
  2. Mueve hacia la derecha (cilindros mayores)
  3. Luego mueve hacia la izquierda (cilindros menores)

#### C-SCAN (Circular SCAN)
- Similar a SCAN pero después de llegar al final, va al inicio (0) y vuelve a comenzar
- **Ventaja**: Proporciona mejor distribución de tiempo de espera
- **Funcionamiento**:
  1. Ordena todas las solicitudes
  2. Mueve hacia el final del disco (4999)
  3. Salta al inicio (0) como un movimiento circular
  4. Atiende las solicitudes restantes

---

## 🛠️ Instalación y Requisitos

### Requisitos
- Python 3.7 o superior
- matplotlib (para visualizaciones)
- numpy (para cálculos numéricos)

### Instalación

```bash
# Clonar o descargar el repositorio
cd Assigment-lll

# Instalar las dependencias necesarias
pip install matplotlib numpy

# O instalar desde requirements.txt
pip install -r requirements.txt
```

---

## 🚀 Uso

### Opción 1: Ejecución con visualizaciones

```bash
python visualizations.py
```

Esto:
1. Genera 1000 solicitudes aleatorias
2. Ejecuta los 3 algoritmos
3. Imprime los resultados en consola
4. Crea 5 gráficas de comparación
5. Guarda todas las gráficas en la carpeta `results/`
6. Muestra las visualizaciones

### Opción 2: Ejecutar solo el programa principal

```bash
python disk_scheduling.py
```

Esto solo imprime los resultados sin crear gráficas.

### Opción 3: Uso desde otro script Python

```python
from disk_scheduling import DiskScheduler

# Crear instancia del planificador
scheduler = DiskScheduler(num_cylinders=5000, num_requests=1000, initial_position=2500)

# Ejecutar todos los algoritmos
results = scheduler.run_all_algorithms()

# Acceder a los resultados
for algorithm, (total_movement, positions) in results.items():
    print(f"{algorithm}: {total_movement} cylinders")
```

---

## 📊 Visualizaciones Generadas

El programa genera 5 gráficas:

### 1. **Comparación de Barras** (`1_comparison_bar.png`)
- Muestra el movimiento total del cabezal para cada algoritmo
- Ideal para comparar rápidamente los algoritmos

### 2. **Movimientos del Cabezal** (`2_head_movements.png`)
- 3 gráficos de líneas mostrando la posición del cabezal a lo largo del tiempo
- Cada uno representa un algoritmo diferente
- Útil para visualizar el patrón de movimiento

### 3. **Métricas de Rendimiento** (`3_performance_metrics.png`)
- Movimiento total vs. Movimiento promedio por solicitud
- Proporciona perspectiva adicional sobre la eficiencia

### 4. **Comparación de Eficiencia** (`4_efficiency_comparison.png`)
- Muestra la eficiencia relativa de cada algoritmo
- El mejor algoritmo = 100%
- Porcentaje de cada uno relativo al mejor

### 5. **Reporte Resumen** (`5_summary_report.png`)
- Combinación de todas las métricas
- Incluye tabla de estadísticas
- Resumen completo del análisis

---

## 📈 Interpretación de Resultados

### Ejemplo de Salida:

```
============================================================
DISK SCHEDULING ALGORITHMS COMPARISON
============================================================
Number of cylinders: 5000
Number of requests: 1000
Initial head position: 2500
============================================================

FCFS:
  Total head movement: 2,450,234 cylinders

SCAN:
  Total head movement: 1,245,678 cylinders

C-SCAN:
  Total head movement: 1,198,456 cylinders

============================================================
SUMMARY:
Best algorithm:  C-SCAN (1,198,456 cylinders)
Worst algorithm: FCFS (2,450,234 cylinders)
Difference: 1,251,778 cylinders
============================================================
```

### Análisis:

| Métrica | Interpretación |
|---------|---|
| **Total Movement** | Cilindros totales que recorre el cabezal. Menor es mejor. |
| **Eficiencia** | Porcentaje del mejor algoritmo. 100% = óptimo. |
| **Promedio por Solicitud** | Cilindros promedio por solicitud. Menor es más eficiente. |

---

## 🔍 Detalles de Implementación

### Complejidad Temporal
- **FCFS**: O(n)
- **SCAN**: O(n log n) - debido al ordenamiento
- **C-SCAN**: O(n log n) - debido al ordenamiento

### Complejidad Espacial
- Todos los algoritmos: O(n) - almacenan la lista de solicitudes

### Parámetros Configurables

En los archivos Python, puedes modificar:

```python
NUM_CYLINDERS = 5000        # Número total de cilindros
NUM_REQUESTS = 1000         # Número de solicitudes
INITIAL_POSITION = 2500     # Posición inicial del cabezal
```

---

## 📁 Estructura de Archivos

```
Assigment-lll/
├── disk_scheduling.py       # Implementación de los algoritmos
├── visualizations.py        # Módulo de visualizaciones
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
└── results/                # Carpeta con las gráficas (generada al ejecutar)
    ├── 1_comparison_bar.png
    ├── 2_head_movements.png
    ├── 3_performance_metrics.png
    ├── 4_efficiency_comparison.png
    └── 5_summary_report.png
```

---

## 💡 Conceptos Teóricos

### ¿Por qué es importante la planificación de disco?

1. **Latencia**: Tiempo entre solicitud y finalización
2. **Throughput**: Número de solicitudes completadas por unidad de tiempo
3. **Fairness**: Equidad en el tiempo de espera para cada solicitud

### Comparación Teórica de Algoritmos:

| Algoritmo | Movimiento Típico | Tiempo Espera Máximo | Justicia |
|-----------|------------------|-------------------|---------|
| **FCFS** | Muy Alto | Alto | Equitativo |
| **SCAN** | Medio | Bajo | Bueno |
| **C-SCAN** | Bajo | Muy Bajo | Excelente |

---

## 🧪 Ejemplos de Uso Avanzado

### Ejecutar con diferentes parámetros:

```python
from disk_scheduling import DiskScheduler, print_results

# Probar con diferentes posiciones iniciales
initial_positions = [0, 1250, 2500, 3750, 4999]

for pos in initial_positions:
    scheduler = DiskScheduler(5000, 1000, pos)
    results = scheduler.run_all_algorithms()
    print(f"\nResultados con posición inicial {pos}:")
    print_results(scheduler, results)
```

### Calcular estadísticas adicionales:

```python
from disk_scheduling import DiskScheduler
import numpy as np

scheduler = DiskScheduler(5000, 1000, 2500)
results = scheduler.run_all_algorithms()

for algorithm, (total_movement, positions) in results.items():
    movements_list = [abs(positions[i] - positions[i-1]) for i in range(1, len(positions))]
    print(f"\n{algorithm}:")
    print(f"  Total: {total_movement}")
    print(f"  Promedio: {np.mean(movements_list):.2f}")
    print(f"  Mediana: {np.median(movements_list):.2f}")
    print(f"  Desv. Est.: {np.std(movements_list):.2f}")
    print(f"  Máximo: {np.max(movements_list)}")
    print(f"  Mínimo: {np.min(movements_list)}")
```

---

## 📝 Notas Importantes

1. **Aleatoriedad**: Cada ejecución genera solicitudes diferentes. Los números varían, pero las tendencias se mantienen.

2. **Posición Inicial**: El algoritmo C-SCAN puede ser más lento si comienza en el inicio (0) comparado con FCFS, porque debe hacer un movimiento circular.

3. **Casos Especiales**: Si todas las solicitudes son iguales o muy cercanas, los tres algoritmos tendrán resultados similares.

4. **Rendimiento**: SCAN y C-SCAN siempre gastarán menos movimiento que FCFS para solicitudes aleatorias distribuidas uniformemente.

---

## 🤝 Contribuciones

Si deseas mejorar este proyecto, puedes:
- Agregar más algoritmos (SSTF, LOOK, C-LOOK)
- Mejorar las visualizaciones
- Optimizar el código
- Agregar más parámetros configurables

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

---

## 📞 Preguntas Frecuentes (FAQ)

**P: ¿Qué diferencia hay entre SCAN y C-SCAN?**
R: SCAN va en ambas direcciones desde donde está. C-SCAN siempre termina en el final del disco y vuelve al principio (movimiento circular).

**P: ¿Por qué FCFS es tan ineficiente?**
R: Porque no ordena las solicitudes, puede hacer que el cabezal viaje de extremo a extremo innecesariamente.

**P: ¿Puedo cambiar el número de cilindros?**
R: Sí, modifica `NUM_CYLINDERS` en los archivos Python. Funciona con cualquier número.

**P: ¿Qué pasa si cambio la posición inicial?**
R: Los resultados variarán ligeramente, pero las tendencias se mantienen. SCAN y C-SCAN seguirán siendo más eficientes que FCFS.

---

## ✅ Conclusión

Este proyecto implementa exitosamente los tres algoritmos de planificación de disco más importantes y proporciona herramientas visuales para comparar su rendimiento. Es una excelente base para entender cómo los sistemas operativos optimizan el acceso al disco.

**Generado**: Noviembre 2025
**Versión**: 1.0