# -*- coding: utf-8 -*-

"""
E-commerce en Python - Aplicación de Consola

Sistema de gestión de e-commerce con las siguientes funcionalidades:
- Ver catálogo de productos
- Buscar productos por nombre o categoría
- Agregar productos al carrito
- Ver carrito y calcular total
- Vaciar carrito

Autor: Gulliver
Versión: 1.0.0
Python: 3.10+

Uso:
    python ecommerce_m3.py

Características técnicas:
- Sin uso de clases (solo funciones)
- Sin excepciones (validaciones con retorno de tuplas)
- Código pythonic (PEP 8, Zen of Python)
- Patrones de diseño funcionales
- Separación de responsabilidades en módulos

Arquitectura:
    config.py         → Configuración y constantes
    data.py           → Datos y Repository Pattern
    validators.py     → Validaciones sin excepciones
    utils.py          → Utilidades de UI
    business_logic.py → Lógica de negocio
    ui.py             → Interfaz de usuario
    ecommerce_m3.py   → Punto de entrada (este archivo)
"""

# ============= IMPORTS =============

# Importar módulo principal de UI
import ui


# ============= FUNCIÓN PRINCIPAL =============

def main() -> None:
    """
    Función principal que inicia la aplicación.
    
    Esta es la función de entrada que se ejecuta al correr el programa.
    Delega toda la lógica a ui.ejecutar_aplicacion() que maneja el loop
    principal y la interacción con el usuario.
    
    Note:
        Esta función es simple intencionalmente siguiendo el principio
        de Single Responsibility: solo iniciar la aplicación.
    """
    # Ejecutar la aplicación
    # Todo el flujo está manejado por el módulo ui
    ui.ejecutar_aplicacion()


# ============= PUNTO DE ENTRADA =============

if __name__ == "__main__":
    """
    Punto de entrada del programa.
    
    Este bloque se ejecuta solo cuando el archivo se ejecuta directamente:
        python ecommerce_m3.py
    
    No se ejecuta cuando se importa como módulo:
        from ecommerce_m3 import main
    
    Esto permite:
    - Usar el archivo como script ejecutable
    - Importar funciones sin ejecutar el programa
    - Facilitar testing
    """
    # Ejecutar función principal
    main()