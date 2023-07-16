import os
import sys

# Definir los argumentos
arg1 = sys.argv[1]

# Construir el comando para ejecutar el archivo de Python pasando los argumentos
comando = ["python", "..\..\GreedyPathPlanning\main.py --t print --f ", arg1]

# Ejecutar el comando
os.system(" ".join(comando))
