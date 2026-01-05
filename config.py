# -*- coding: utf-8 -*-
"""
Módulo de configuración del E-commerce.

Este módulo centraliza todas las constantes y configuraciones de la aplicación,
siguiendo el principio DRY (Don't Repeat Yourself) y facilitando el mantenimiento.

Patrón aplicado: Configuration Pattern
- Centraliza valores mágicos
- Facilita cambios sin tocar lógica
- Tipo seguro con type hints

NOTA: Precios en pesos chilenos (CLP) - valores enteros sin decimales
"""

from typing import Final

# ============= INFORMACIÓN DE LA APLICACIÓN =============

APP_NAME: Final[str] = "E-commerce Python Chile"
APP_VERSION: Final[str] = "1.0.0"
APP_AUTHOR: Final[str] = "Gulliver"


# ============= MONEDA Y FORMATO =============

# Chile usa pesos (CLP) sin decimales
SIMBOLO_MONEDA: Final[str] = "$"
CODIGO_MONEDA: Final[str] = "CLP"


# ============= OPCIONES DEL MENÚ =============

# Opciones del menú principal
# Usar constantes evita "números mágicos" en el código
OPCION_VER_CATALOGO: Final[int] = 1
OPCION_BUSCAR_PRODUCTO: Final[int] = 2
OPCION_AGREGAR_AL_CARRITO: Final[int] = 3
OPCION_VER_CARRITO: Final[int] = 4
OPCION_VACIAR_CARRITO: Final[int] = 5
OPCION_SALIR: Final[int] = 0

# Rango válido de opciones
OPCION_MINIMA: Final[int] = 0
OPCION_MAXIMA: Final[int] = 5


# ============= VALIDACIONES DE PRODUCTO =============

# Restricciones para productos (precios en pesos chilenos)
PRECIO_MINIMO: Final[int] = 1  # Mínimo 1 peso
CANTIDAD_MINIMA: Final[int] = 1
CANTIDAD_MAXIMA: Final[int] = 999

# Longitudes para validaciones de texto
NOMBRE_MIN_LENGTH: Final[int] = 3
NOMBRE_MAX_LENGTH: Final[int] = 100
CATEGORIA_MIN_LENGTH: Final[int] = 3
CATEGORIA_MAX_LENGTH: Final[int] = 50


# ============= CATEGORÍAS VÁLIDAS =============

# Categorías predefinidas del catálogo
# Usar tupla para inmutabilidad
CATEGORIAS_VALIDAS: Final[tuple] = (
    "ropa",
    "tecnología",
    "hogar",
    "deportes",
    "libros",
    "alimentos"
)


# ============= FORMATO Y PRESENTACIÓN =============

# Símbolos y caracteres para la UI
SEPARADOR_LINEA: Final[str] = "-" * 70
SEPARADOR_TABLA: Final[str] = "=" * 70

# Ancho de columnas para tablas
ANCHO_COLUMNA_ID: Final[int] = 5
ANCHO_COLUMNA_NOMBRE: Final[int] = 30
ANCHO_COLUMNA_CATEGORIA: Final[int] = 15
ANCHO_COLUMNA_PRECIO: Final[int] = 15
ANCHO_COLUMNA_CANTIDAD: Final[int] = 10
ANCHO_COLUMNA_SUBTOTAL: Final[int] = 15


# ============= MENSAJES DE LA APLICACIÓN =============

# Mensajes de bienvenida y despedida
MSG_BIENVENIDA: Final[str] = f"🛒 Bienvenido/a a {APP_NAME}"
MSG_DESPEDIDA: Final[str] = "¡Gracias por tu visita! Vuelve pronto 👋"

# Mensajes de éxito
MSG_PRODUCTO_AGREGADO: Final[str] = "✓ Producto agregado al carrito exitosamente"
MSG_CARRITO_VACIADO: Final[str] = "✓ Carrito vaciado correctamente"

# Mensajes de error
MSG_ERROR_OPCION_INVALIDA: Final[str] = "✗ Opción inválida. Por favor, selecciona una opción del menú."
MSG_ERROR_PRODUCTO_NO_EXISTE: Final[str] = "✗ El producto con ese ID no existe en el catálogo."
MSG_ERROR_CANTIDAD_INVALIDA: Final[str] = f"✗ La cantidad debe ser un número entre {CANTIDAD_MINIMA} y {CANTIDAD_MAXIMA}."
MSG_ERROR_ID_INVALIDO: Final[str] = "✗ El ID debe ser un número entero positivo."
MSG_ERROR_PRECIO_INVALIDO: Final[str] = f"✗ El precio debe ser un número entero mayor o igual a {PRECIO_MINIMO}."

# Mensajes informativos
MSG_CARRITO_VACIO: Final[str] = "ℹ El carrito está vacío."
MSG_NO_RESULTADOS_BUSQUEDA: Final[str] = "ℹ No se encontraron productos que coincidan con tu búsqueda."


# ============= CÓDIGOS DE ESTADO =============

# Códigos para operaciones (similar a HTTP status codes)
# Facilita el manejo de resultados sin excepciones
STATUS_OK: Final[int] = 200
STATUS_ERROR_VALIDACION: Final[int] = 400
STATUS_ERROR_NO_ENCONTRADO: Final[int] = 404
STATUS_ERROR_CARRITO_VACIO: Final[int] = 204


# ============= CONFIGURACIÓN DE BÚSQUEDA =============

# Criterios de búsqueda válidos
CRITERIO_NOMBRE: Final[str] = "nombre"
CRITERIO_CATEGORIA: Final[str] = "categoria"

CRITERIOS_BUSQUEDA_VALIDOS: Final[tuple] = (
    CRITERIO_NOMBRE,
    CRITERIO_CATEGORIA
)


# ============= CLAVES DEL DICCIONARIO DE PRODUCTO =============

# Claves estándar para diccionarios de producto
# Centralizar evita errores de tipeo
KEY_ID: Final[str] = "id"
KEY_NOMBRE: Final[str] = "nombre"
KEY_CATEGORIA: Final[str] = "categoria"
KEY_PRECIO: Final[str] = "precio"

# Claves adicionales para items del carrito
KEY_CANTIDAD: Final[str] = "cantidad"
KEY_SUBTOTAL: Final[str] = "subtotal"


# ============= VALORES POR DEFECTO =============

# Valor por defecto cuando no se encuentra un producto
PRECIO_POR_DEFECTO: Final[int] = 0
CANTIDAD_POR_DEFECTO: Final[int] = 1


# ============= FUNCIONES DE CONFIGURACIÓN =============

def formatear_precio(precio: int) -> str:
    """
    Formatea un precio en pesos chilenos con separadores de miles.
    
    En Chile los precios son enteros (sin decimales) y se usa punto como
    separador de miles.
    
    Args:
        precio: Precio en pesos chilenos (entero)
        
    Returns:
        Precio formateado como string (ej: "$1.234.567")
        
    Example:
        >>> formatear_precio(1234567)
        '$1.234.567'
        >>> formatear_precio(9990)
        '$9.990'
        >>> formatear_precio(500)
        '$500'
    """
    # Usar separador de miles con punto (estilo chileno)
    # {:,} usa coma, luego la reemplazamos por punto
    precio_formateado = f"{precio:,}".replace(",", ".")
    return f"{SIMBOLO_MONEDA}{precio_formateado}"


def obtener_texto_menu() -> str:
    """
    Retorna el texto completo del menú principal.
    
    Centralizar el menú permite modificarlo fácilmente sin tocar la lógica.
    
    Returns:
        String con el menú formateado
    """
    menu = f"""
{SEPARADOR_TABLA}
{MSG_BIENVENIDA.center(70)}
{SEPARADOR_TABLA}

MENÚ PRINCIPAL:

  {OPCION_VER_CATALOGO}) Ver catálogo de productos
  {OPCION_BUSCAR_PRODUCTO}) Buscar producto por nombre o categoría
  {OPCION_AGREGAR_AL_CARRITO}) Agregar producto al carrito
  {OPCION_VER_CARRITO}) Ver carrito y total
  {OPCION_VACIAR_CARRITO}) Vaciar carrito
  {OPCION_SALIR}) Salir

{SEPARADOR_LINEA}
"""
    return menu


def es_opcion_valida(opcion: int) -> bool:
    """
    Valida que una opción esté en el rango permitido.
    
    Args:
        opcion: Número de opción a validar
        
    Returns:
        True si la opción es válida, False en caso contrario
        
    Example:
        >>> es_opcion_valida(1)
        True
        >>> es_opcion_valida(99)
        False
    """
    return OPCION_MINIMA <= opcion <= OPCION_MAXIMA


def es_precio_valido(precio: int) -> bool:
    """
    Valida que un precio sea válido (entero positivo).
    
    Args:
        precio: Precio a validar en pesos chilenos
        
    Returns:
        True si el precio es válido, False en caso contrario
        
    Example:
        >>> es_precio_valido(1000)
        True
        >>> es_precio_valido(0)
        False
        >>> es_precio_valido(-500)
        False
    """
    return isinstance(precio, int) and precio >= PRECIO_MINIMO


def es_cantidad_valida(cantidad: int) -> bool:
    """
    Valida que una cantidad esté en el rango permitido.
    
    Args:
        cantidad: Cantidad a validar
        
    Returns:
        True si la cantidad es válida, False en caso contrario
        
    Example:
        >>> es_cantidad_valida(5)
        True
        >>> es_cantidad_valida(0)
        False
        >>> es_cantidad_valida(1000)
        False
    """
    return (isinstance(cantidad, int) and 
            CANTIDAD_MINIMA <= cantidad <= CANTIDAD_MAXIMA)


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    # Tests básicos para verificar configuración
    print("=== Tests de Configuración ===\n")
    
    # Test 1: Formateo de precios chilenos
    print("Test 1: Formateo de precios en pesos chilenos")
    print(f"  {formatear_precio(1234567)} (precio grande)")
    print(f"  {formatear_precio(99990)} (precio medio)")
    print(f"  {formatear_precio(500)} (precio pequeño)")
    print(f"  {formatear_precio(15990)} (precio típico)")
    
    # Test 2: Validación de precios
    print("\nTest 2: Validación de precios")
    print(f"  Precio 1000: {es_precio_valido(1000)}")
    print(f"  Precio 0: {es_precio_valido(0)}")
    print(f"  Precio -500: {es_precio_valido(-500)}")
    
    # Test 3: Validación de cantidades
    print("\nTest 3: Validación de cantidades")
    print(f"  Cantidad 5: {es_cantidad_valida(5)}")
    print(f"  Cantidad 0: {es_cantidad_valida(0)}")
    print(f"  Cantidad 1000: {es_cantidad_valida(1000)}")
    
    # Test 4: Validación de opciones
    print("\nTest 4: Validación de opciones")
    print(f"  Opción 1 válida: {es_opcion_valida(1)}")
    print(f"  Opción 99 válida: {es_opcion_valida(99)}")
    print(f"  Opción 0 válida: {es_opcion_valida(0)}")
    
    # Test 5: Mostrar menú
    print("\nTest 5: Menú principal")
    print(obtener_texto_menu())
    
    # Test 6: Constantes
    print("Test 6: Constantes definidas")
    print(f"  Moneda: {SIMBOLO_MONEDA} ({CODIGO_MONEDA})")
    print(f"  Categorías válidas: {CATEGORIAS_VALIDAS}")
    print(f"  Rango cantidad: {CANTIDAD_MINIMA} - {CANTIDAD_MAXIMA}")
    print(f"  Precio mínimo: {formatear_precio(PRECIO_MINIMO)}")