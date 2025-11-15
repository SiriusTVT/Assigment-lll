"""
Implementación de Algoritmos de Planificación de Disco
Este programa simula tres algoritmos diferentes para manejar las solicitudes de acceso al disco
"""

import random
import matplotlib.pyplot as plt
import numpy as np


class DiskScheduler:
    """Clase que simula el planificador de disco con tres algoritmos diferentes"""
    
    def __init__(self, num_cylinders=5000, num_requests=1000, initial_position=0):
        """
        Inicializa nuestro planificador de disco
        
        Parámetros:
            num_cylinders: Cuántos cilindros tiene el disco (por defecto 5000, del 0 al 4999)
            num_requests: Cuántas solicitudes vamos a generar aleatoriamente
            initial_position: Dónde empieza el cabezal del disco
        """
        self.num_cylinders = num_cylinders
        self.num_requests = num_requests
        self.initial_position = initial_position
        
        # Generamos las solicitudes aleatorias (números entre 0 y el máximo de cilindros)
        self.requests = [random.randint(0, num_cylinders - 1) for _ in range(num_requests)]
    
    def fcfs(self):
        """
        FCFS - First Come First Served (El primero que llega, primero se atiende)
        Este es el algoritmo más simple: atendemos las solicitudes en el orden que llegaron
        
        Retorna:
            Una tupla con (movimiento_total, historial_de_posiciones)
        """
        current_position = self.initial_position
        total_movement = 0
        positions_history = [current_position]
        
        # Recorremos cada solicitud en el orden que llegó
        for request in self.requests:
            # Calculamos cuánto se tiene que mover el cabezal
            movement = abs(current_position - request)
            total_movement += movement
            current_position = request
            positions_history.append(current_position)
        
        return total_movement, positions_history
    
    def scan(self):
        """
        SCAN - Algoritmo del Ascensor
        El cabezal se mueve en una dirección atendiendo solicitudes hasta llegar al final,
        luego se devuelve atendiendo las que quedaron pendientes
        
        Retorna:
            Una tupla con (movimiento_total, historial_de_posiciones)
        """
        current_position = self.initial_position
        total_movement = 0
        positions_history = [current_position]
        
        # Primero ordenamos todas las solicitudes
        sorted_requests = sorted(self.requests)
        
        # Las dividimos en dos grupos: las que están a la izquierda y a la derecha de donde empezamos
        left_requests = [r for r in sorted_requests if r < self.initial_position]
        right_requests = [r for r in sorted_requests if r >= self.initial_position]
        
        # Primero vamos hacia la derecha (hacia los cilindros más altos)
        if right_requests:
            for request in right_requests:
                movement = abs(current_position - request)
                total_movement += movement
                current_position = request
                positions_history.append(current_position)
        
        # Luego nos devolvemos hacia la izquierda (hacia los cilindros más bajos)
        if left_requests:
            for request in reversed(left_requests):
                movement = abs(current_position - request)
                total_movement += movement
                current_position = request
                positions_history.append(current_position)
        
        return total_movement, positions_history
    
    def c_scan(self):
        """
        C-SCAN - SCAN Circular
        Similar al SCAN, pero cuando llega al final, salta al inicio y sigue en la misma dirección.
        Es como un ascensor que siempre va en la misma dirección y cuando llega al último piso,
        se teletransporta al primero.
        
        Retorna:
            Una tupla con (movimiento_total, historial_de_posiciones)
        """
        current_position = self.initial_position
        total_movement = 0
        positions_history = [current_position]
        
        # Ordenamos todas las solicitudes
        sorted_requests = sorted(self.requests)
        
        # Las separamos: las que están antes y después de donde empezamos
        left_requests = [r for r in sorted_requests if r < self.initial_position]
        right_requests = [r for r in sorted_requests if r >= self.initial_position]
        
        # Primero vamos hacia la derecha hasta el final del disco
        if right_requests:
            for request in right_requests:
                movement = abs(current_position - request)
                total_movement += movement
                current_position = request
                positions_history.append(current_position)
        
        # Nos movemos hasta el último cilindro si aún no estamos ahí
        if current_position != self.num_cylinders - 1:
            movement = abs(current_position - (self.num_cylinders - 1))
            total_movement += movement
            current_position = self.num_cylinders - 1
            positions_history.append(current_position)
        
        # Aquí viene lo circular: saltamos al cilindro 0
        if left_requests:
            movement = current_position  # Del último cilindro al 0
            total_movement += movement
            current_position = 0
            positions_history.append(current_position)
            
            # Ahora atendemos las solicitudes que quedaron desde el cilindro 0
            for request in left_requests:
                movement = abs(current_position - request)
                total_movement += movement
                current_position = request
                positions_history.append(current_position)
        
        return total_movement, positions_history
    
    def run_all_algorithms(self):
        """
        Ejecuta los tres algoritmos y nos da los resultados de todos
        
        Retorna:
            Un diccionario con los resultados de cada algoritmo
        """
        results = {
            'FCFS': self.fcfs(),
            'SCAN': self.scan(),
            'C-SCAN': self.c_scan()
        }
        return results


def print_results(scheduler, results):
    """Imprime los resultados de forma bonita para que sea fácil comparar"""
    print("=" * 60)
    print("COMPARACIÓN DE ALGORITMOS DE PLANIFICACIÓN DE DISCO")
    print("=" * 60)
    print(f"Número de cilindros: {scheduler.num_cylinders}")
    print(f"Número de solicitudes: {scheduler.num_requests}")
    print(f"Posición inicial del cabezal: {scheduler.initial_position}")
    print("=" * 60)
    
    for algorithm, (total_movement, _) in results.items():
        print(f"\n{algorithm}:")
        print(f"  Movimiento total del cabezal: {total_movement} cilindros")
    
    print("\n" + "=" * 60)
    print("RESUMEN:")
    movements = {alg: result[0] for alg, result in results.items()}
    best_algorithm = min(movements, key=movements.get)
    worst_algorithm = max(movements, key=movements.get)
    
    print(f"Mejor algoritmo:  {best_algorithm} ({movements[best_algorithm]} cilindros)")
    print(f"Peor algoritmo: {worst_algorithm} ({movements[worst_algorithm]} cilindros)")
    print(f"Diferencia: {movements[worst_algorithm] - movements[best_algorithm]} cilindros")
    print("=" * 60)


def main():
    """Función principal que ejecuta todo el programa"""
    # Aquí definimos los parámetros del disco
    NUM_CYLINDERS = 5000
    NUM_REQUESTS = 1000
    INITIAL_POSITION = 2500  # Empezamos en la mitad del disco
    
    print("\nGenerando escenario de planificación de disco...")
    print(f"Cilindros del disco: 0 - {NUM_CYLINDERS - 1}")
    print(f"Número de solicitudes: {NUM_REQUESTS}")
    print(f"Posición inicial del cabezal: {INITIAL_POSITION}")
    print("\nProcesando algoritmos...\n")
    
    # Creamos nuestro planificador y ejecutamos los algoritmos
    scheduler = DiskScheduler(NUM_CYLINDERS, NUM_REQUESTS, INITIAL_POSITION)
    results = scheduler.run_all_algorithms()
    
    # Mostramos los resultados
    print_results(scheduler, results)
    
    # Preparamos los datos por si queremos hacer gráficas después
    visualization_data = {
        'scheduler': scheduler,
        'results': results
    }
    
    return scheduler, results


if __name__ == "__main__":
    scheduler, results = main()
