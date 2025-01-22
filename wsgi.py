import sys
import os

# RUTA donde se encuentran tus archivos
project_home = '/home/yourusername'
if project_home not in sys.path:
    sys.path.append(project_home)

# Importa tu aplicación
from app import app as application
