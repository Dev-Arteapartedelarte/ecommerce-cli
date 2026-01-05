# -*- coding: utf-8 -*-
"""
Módulo de utilidades del E-commerce.

Contiene funciones auxiliares para formateo, presentación y UI.

Patrón aplicado: Helper/Utility Pattern
- Funciones puras de propósito general
- Separación de concerns (UI separada de lógica)
- Reutilizables en toda la aplicación
"""

from typing import List, Dict, Any
import os
import platform
import config
import data


# ============= UTILIDADES DE CONSOLA =============

def limpiar_pantalla() -> None:
    """
    Limpia la pantalla de la consola según el sistema operativo.
    
    - Windows: usa 'cls'
    - Unix/Linux/Mac: usa 'clear'
    
    Note:
        Esta función tiene side effect (modifica la consola)
    """
    sistema = platform.system()
    
    if sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def pausar() -> None:
    """
    Pausa la ejecución hasta que el usuario presione Enter.
    
    Note:
        Esta función tiene side effect (espera input del usuario)
    """
    input("\nPresiona ENTER para continuar...")


# ============= UTILIDADES DE FORMATEO =============

def centrar_texto(texto: str, ancho: int) -> str:
    """
    Centra un texto dentro de un ancho dado.
    
    Args:
        texto: Texto a centrar
        ancho: Ancho total disponible
        
    Returns:
        Texto centrado con espacios
        
    Example:
        >>> centrar_texto("Hola", 10)
        '   Hola   '
    """
    return texto.center(ancho)


def alinear_derecha(texto: str, ancho: int) -> str:
    """
    Alinea un texto a la derecha dentro de un ancho dado.
    
    Args:
        texto: Texto a alinear
        ancho: Ancho total disponible
        
    Returns:
        Texto alineado a la derecha
        
    Example:
        >>> alinear_derecha("100", 10)
        '       100'
    """
    return texto.rjust(ancho)


def alinear_izquierda(texto: str, ancho: int) -> str:
    """
    Alinea un texto a la izquierda dentro de un ancho dado.
    
    Args:
        texto: Texto a alinear
        ancho: Ancho total disponible
        
    Returns:
        Texto alineado a la izquierda
        
    Example:
        >>> alinear_izquierda("Producto", 10)
        'Producto  '
    """
    return texto.ljust(ancho)


def truncar_texto(texto: str, max_length: int) -> str:
    """
    Trunca un texto a una longitud máxima agregando '...' si es necesario.
    
    Args:
        texto: Texto a truncar
        max_length: Longitud máxima (incluyendo '...')
        
    Returns:
        Texto truncado
        
    Example:
        >>> truncar_texto("Producto muy largo", 10)
        'Product...'
    """
    if len(texto) <= max_length:
        return texto
    
    # Restar 3 para los puntos suspensivos
    return texto[:max_length - 3] + "..."


# ============= PRESENTACIÓN DE PRODUCTOS =============

def formatear_fila_producto(producto: Dict[str, Any]) -> str:
    """
    Formatea una fila de producto para mostrar en tabla.
    
    Args:
        producto: Diccionario del producto
        
    Returns:
        String formateado con columnas alineadas
        
    Example:
        >>> producto = {'id': 1, 'nombre': 'Laptop', 'categoria': 'tech', 'precio': 1000}
        >>> formatear_fila_producto(producto)
        '  1   Laptop                         tech            $1.000'
    """
    # Extraer datos del producto
    producto_id = producto[config.KEY_ID]
    nombre = producto[config.KEY_NOMBRE]
    categoria = producto[config.KEY_CATEGORIA]
    precio = producto[config.KEY_PRECIO]
    
    # Truncar nombre si es muy largo
    nombre_truncado = truncar_texto(nombre, config.ANCHO_COLUMNA_NOMBRE)
    
    # Formatear precio
    precio_formateado = config.formatear_precio(precio)
    
    # Construir fila con columnas alineadas
    fila = (
        f"{str(producto_id).rjust(config.ANCHO_COLUMNA_ID)} "
        f"{nombre_truncado.ljust(config.ANCHO_COLUMNA_NOMBRE)} "
        f"{categoria.ljust(config.ANCHO_COLUMNA_CATEGORIA)} "
        f"{precio_formateado.rjust(config.ANCHO_COLUMNA_PRECIO)}"
    )
    
    return fila


def formatear_encabezado_productos() -> str:
    """
    Formatea el encabezado de la tabla de productos.
    
    Returns:
        String con el encabezado formateado
    """
    encabezado = (
        f"{'ID'.rjust(config.ANCHO_COLUMNA_ID)} "
        f"{'NOMBRE'.ljust(config.ANCHO_COLUMNA_NOMBRE)} "
        f"{'CATEGORÍA'.ljust(config.ANCHO_COLUMNA_CATEGORIA)} "
        f"{'PRECIO'.rjust(config.ANCHO_COLUMNA_PRECIO)}"
    )
    
    return encabezado


def mostrar_catalogo_productos(catalogo: List[Dict[str, Any]]) -> None:
    """
    Muestra el catálogo completo de productos en formato tabla.
    
    Args:
        catalogo: Lista de productos
        
    Note:
        Esta función tiene side effect (imprime en consola)
    """
    print("\n" + config.SEPARADOR_TABLA)
    print(centrar_texto("CATÁLOGO DE PRODUCTOS", 70))
    print(config.SEPARADOR_TABLA)
    
    # Mostrar encabezado
    print(formatear_encabezado_productos())
    print(config.SEPARADOR_LINEA)
    
    # Mostrar cada producto
    for producto in catalogo:
        print(formatear_fila_producto(producto))
    
    print(config.SEPARADOR_TABLA)
    print(f"Total de productos: {data.contar_productos_en_catalogo(catalogo)}")


def mostrar_lista_productos(productos: List[Dict[str, Any]], titulo: str) -> None:
    """
    Muestra una lista de productos (por ejemplo, resultados de búsqueda).
    
    Args:
        productos: Lista de productos a mostrar
        titulo: Título de la lista
        
    Note:
        Esta función tiene side effect (imprime en consola)
    """
    print("\n" + config.SEPARADOR_TABLA)
    print(centrar_texto(titulo, 70))
    print(config.SEPARADOR_TABLA)
    
    if not productos:
        print(centrar_texto(config.MSG_NO_RESULTADOS_BUSQUEDA, 70))
        print(config.SEPARADOR_TABLA)
        return
    
    # Mostrar encabezado
    print(formatear_encabezado_productos())
    print(config.SEPARADOR_LINEA)
    
    # Mostrar cada producto
    for producto in productos:
        print(formatear_fila_producto(producto))
    
    print(config.SEPARADOR_TABLA)
    print(f"Productos encontrados: {len(productos)}")


# ============= PRESENTACIÓN DEL CARRITO =============

def formatear_fila_carrito(item: Dict[str, Any]) -> str:
    """
    Formatea una fila del carrito para mostrar en tabla.
    
    Args:
        item: Item del carrito (producto + cantidad + subtotal)
        
    Returns:
        String formateado con columnas alineadas
    """
    # Extraer datos del item
    item_id = item[config.KEY_ID]
    nombre = item[config.KEY_NOMBRE]
    cantidad = item[config.KEY_CANTIDAD]
    precio = item[config.KEY_PRECIO]
    subtotal = item[config.KEY_SUBTOTAL]
    
    # Truncar nombre si es muy largo
    nombre_truncado = truncar_texto(nombre, config.ANCHO_COLUMNA_NOMBRE)
    
    # Formatear precios
    precio_formateado = config.formatear_precio(precio)
    subtotal_formateado = config.formatear_precio(subtotal)
    
    # Construir fila
    fila = (
        f"{str(item_id).rjust(config.ANCHO_COLUMNA_ID)} "
        f"{nombre_truncado.ljust(config.ANCHO_COLUMNA_NOMBRE)} "
        f"{str(cantidad).center(config.ANCHO_COLUMNA_CANTIDAD)} "
        f"{precio_formateado.rjust(config.ANCHO_COLUMNA_PRECIO)} "
        f"{subtotal_formateado.rjust(config.ANCHO_COLUMNA_SUBTOTAL)}"
    )
    
    return fila


def formatear_encabezado_carrito() -> str:
    """
    Formatea el encabezado de la tabla del carrito.
    
    Returns:
        String con el encabezado formateado
    """
    encabezado = (
        f"{'ID'.rjust(config.ANCHO_COLUMNA_ID)} "
        f"{'NOMBRE'.ljust(config.ANCHO_COLUMNA_NOMBRE)} "
        f"{'CANT.'.center(config.ANCHO_COLUMNA_CANTIDAD)} "
        f"{'PRECIO UNIT.'.rjust(config.ANCHO_COLUMNA_PRECIO)} "
        f"{'SUBTOTAL'.rjust(config.ANCHO_COLUMNA_SUBTOTAL)}"
    )
    
    return encabezado


def mostrar_carrito(carrito: List[Dict[str, Any]]) -> None:
    """
    Muestra el contenido del carrito en formato tabla.
    
    Args:
        carrito: Lista de items del carrito
        
    Note:
        Esta función tiene side effect (imprime en consola)
    """
    print("\n" + config.SEPARADOR_TABLA)
    print(centrar_texto("🛒 CARRITO DE COMPRAS", 70))
    print(config.SEPARADOR_TABLA)
    
    # Verificar si está vacío
    if data.es_carrito_vacio(carrito):
        print(centrar_texto(config.MSG_CARRITO_VACIO, 70))
        print(config.SEPARADOR_TABLA)
        return
    
    # Mostrar encabezado
    print(formatear_encabezado_carrito())
    print(config.SEPARADOR_LINEA)
    
    # Mostrar cada item
    for item in carrito:
        print(formatear_fila_carrito(item))
    
    # Calcular y mostrar totales
    total_items = data.contar_items_en_carrito(carrito)
    total_unidades = data.contar_unidades_en_carrito(carrito)
    total_pagar = data.calcular_total_carrito(carrito)
    
    print(config.SEPARADOR_LINEA)
    print(f"Productos distintos: {total_items}")
    print(f"Unidades totales: {total_unidades}")
    print(config.SEPARADOR_TABLA)
    
    # Mostrar total en grande
    total_formateado = config.formatear_precio(total_pagar)
    print(f"TOTAL A PAGAR: {total_formateado}".rjust(70))
    print(config.SEPARADOR_TABLA)


# ============= MENSAJES Y FEEDBACK =============

def mostrar_mensaje_exito(mensaje: str) -> None:
    """
    Muestra un mensaje de éxito.
    
    Args:
        mensaje: Mensaje a mostrar
    """
    print(f"\n✓ {mensaje}")


def mostrar_mensaje_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error.
    
    Args:
        mensaje: Mensaje a mostrar
    """
    print(f"\n✗ ERROR: {mensaje}")


def mostrar_mensaje_info(mensaje: str) -> None:
    """
    Muestra un mensaje informativo.
    
    Args:
        mensaje: Mensaje a mostrar
    """
    print(f"\nℹ {mensaje}")


# ============= SOLICITUD DE ENTRADA =============

def solicitar_entrada(mensaje: str) -> str:
    """
    Solicita entrada al usuario con un mensaje.
    
    Args:
        mensaje: Mensaje a mostrar al usuario
        
    Returns:
        String ingresado por el usuario (con strip())
        
    Example:
        >>> solicitar_entrada("Ingrese su nombre")
        # Usuario ingresa: "  Juan  "
        # Retorna: "Juan"
    """
    entrada = input(f"\n{mensaje}: ")
    return entrada.strip()


def solicitar_confirmacion(mensaje: str) -> bool:
    """
    Solicita confirmación al usuario (s/n).
    
    Args:
        mensaje: Mensaje de confirmación
        
    Returns:
        True si el usuario confirma (s/S/si/SI), False en caso contrario
        
    Example:
        >>> solicitar_confirmacion("¿Desea continuar?")
        # Usuario ingresa: "s"
        # Retorna: True
    """
    respuesta = solicitar_entrada(f"{mensaje} (s/n)").lower()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']


# ============= UTILIDADES DE PRESENTACIÓN =============

def mostrar_titulo(titulo: str) -> None:
    """
    Muestra un título destacado.
    
    Args:
        titulo: Título a mostrar
    """
    print("\n" + config.SEPARADOR_TABLA)
    print(centrar_texto(titulo, 70))
    print(config.SEPARADOR_TABLA)


def mostrar_categorias_disponibles(catalogo: List[Dict[str, Any]]) -> None:
    """
    Muestra las categorías disponibles en el catálogo.
    
    Args:
        catalogo: Lista de productos
    """
    categorias = data.obtener_todas_las_categorias(catalogo)
    
    print("\nCategorías disponibles:")
    for categoria in categorias:
        # Contar productos por categoría
        productos_categoria = data.obtener_productos_por_categoria(catalogo, categoria)
        cantidad = len(productos_categoria)
        print(f"  • {categoria.capitalize()} ({cantidad} productos)")


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    print("=== Tests de Utilidades ===\n")
    
    # Test 1: Formateo de texto
    print("Test 1: Formateo de texto")
    print(f"  Centrado: '{centrar_texto('Hola', 20)}'")
    print(f"  Derecha:  '{alinear_derecha('100', 20)}'")
    print(f"  Izquierda: '{alinear_izquierda('Producto', 20)}'")
    print(f"  Truncado: '{truncar_texto('Producto muy muy largo', 15)}'")
    
    # Test 2: Encabezado de productos
    print("\nTest 2: Encabezado de productos")
    print(formatear_encabezado_productos())
    print(config.SEPARADOR_LINEA)
    
    # Test 3: Formateo de producto
    print("\nTest 3: Formateo de fila de producto")
    catalogo = data.crear_catalogo_inicial()
    producto = catalogo[0]
    print(formatear_fila_producto(producto))
    
    # Test 4: Mostrar catálogo completo
    print("\nTest 4: Mostrar catálogo completo")
    mostrar_catalogo_productos(catalogo[:5])  # Solo primeros 5
    
    # Test 5: Formateo de carrito
    print("\nTest 5: Formateo de carrito")
    carrito = data.crear_carrito_vacio()
    carrito = data.agregar_item_a_carrito(carrito, catalogo[0], 2)
    carrito = data.agregar_item_a_carrito(carrito, catalogo[4], 1)
    mostrar_carrito(carrito)
    
    # Test 6: Mensajes
    print("\nTest 6: Mensajes")
    mostrar_mensaje_exito("Operación exitosa")
    mostrar_mensaje_error("Algo salió mal")
    mostrar_mensaje_info("Información importante")
    
    # Test 7: Categorías disponibles
    print("\nTest 7: Categorías disponibles")
    mostrar_categorias_disponibles(catalogo)