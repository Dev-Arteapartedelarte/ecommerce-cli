# -*- coding: utf-8 -*-
"""
Módulo de validaciones del E-commerce.

Contiene funciones puras de validación que retornan tuplas (bool, str)
en lugar de lanzar excepciones, siguiendo el patrón Result/Either.

Patrón aplicado: Result Pattern (sin excepciones)
- Funciones retornan (éxito: bool, mensaje: str)
- Código más funcional y predecible
- Fácil de testear

Principios:
- Funciones puras (sin side effects)
- Sin excepciones (retornan resultados)
- Validaciones explícitas y claras
"""

from typing import Tuple, List, Dict, Any
import config
import data


# ============= TIPO DE RESULTADO =============

# Type alias para mejorar legibilidad
ResultadoValidacion = Tuple[bool, str]
# Tupla: (es_valido: bool, mensaje_error: str)


# ============= VALIDACIONES DE ENTRADA DE USUARIO =============

def validar_entrada_entero(entrada: str) -> ResultadoValidacion:
    """
    Valida que una entrada de usuario sea un número entero válido.
    
    Args:
        entrada: String ingresado por el usuario
        
    Returns:
        Tupla (es_valido, mensaje_error)
        - es_valido: True si es entero válido, False si no
        - mensaje_error: Descripción del error o string vacío si válido
        
    Example:
        >>> validar_entrada_entero("123")
        (True, '')
        >>> validar_entrada_entero("abc")
        (False, 'Debe ingresar un número entero válido')
        >>> validar_entrada_entero("12.5")
        (False, 'Debe ingresar un número entero válido')
    """
    # Validar que no esté vacío
    if not entrada or entrada.strip() == "":
        return False, "La entrada no puede estar vacía"
    
    # Limpiar espacios
    entrada_limpia = entrada.strip()
    
    # Validar que sea un entero
    # Usar isdigit() para números positivos
    # Manejar negativos manualmente
    if entrada_limpia.startswith('-'):
        # Número negativo
        if len(entrada_limpia) > 1 and entrada_limpia[1:].isdigit():
            return True, ""
        return False, "Debe ingresar un número entero válido"
    else:
        # Número positivo
        if entrada_limpia.isdigit():
            return True, ""
        return False, "Debe ingresar un número entero válido"


def convertir_a_entero(entrada: str) -> Tuple[bool, int, str]:
    """
    Convierte una entrada de usuario a entero.
    
    Args:
        entrada: String a convertir
        
    Returns:
        Tupla (exito, valor, mensaje_error)
        - exito: True si la conversión fue exitosa
        - valor: El entero convertido (0 si falla)
        - mensaje_error: Descripción del error o string vacío
        
    Example:
        >>> convertir_a_entero("123")
        (True, 123, '')
        >>> convertir_a_entero("abc")
        (False, 0, 'Debe ingresar un número entero válido')
    """
    # Primero validar
    es_valido, mensaje = validar_entrada_entero(entrada)
    
    if not es_valido:
        return False, 0, mensaje
    
    # Convertir
    try:
        valor = int(entrada.strip())
        return True, valor, ""
    except ValueError:
        # Esto no debería ocurrir si la validación funciona bien
        return False, 0, "Error al convertir a número entero"


# ============= VALIDACIONES DE PRODUCTO =============

def validar_id_producto(producto_id: int, catalogo: List[Dict[str, Any]]) -> ResultadoValidacion:
    """
    Valida que un ID de producto exista en el catálogo.
    
    Args:
        producto_id: ID a validar
        catalogo: Lista de productos
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> catalogo = data.crear_catalogo_inicial()
        >>> validar_id_producto(1, catalogo)
        (True, '')
        >>> validar_id_producto(999, catalogo)
        (False, 'El producto con ID 999 no existe en el catálogo')
    """
    # Validar que sea positivo
    if producto_id <= 0:
        return False, "El ID debe ser un número positivo"
    
    # Buscar en catálogo
    producto = data.buscar_producto_por_id(catalogo, producto_id)
    
    if producto is None:
        return False, f"El producto con ID {producto_id} no existe en el catálogo"
    
    return True, ""


def validar_cantidad(cantidad: int) -> ResultadoValidacion:
    """
    Valida que una cantidad esté en el rango permitido.
    
    Args:
        cantidad: Cantidad a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_cantidad(5)
        (True, '')
        >>> validar_cantidad(0)
        (False, 'La cantidad debe estar entre 1 y 999')
        >>> validar_cantidad(1000)
        (False, 'La cantidad debe estar entre 1 y 999')
    """
    if cantidad < config.CANTIDAD_MINIMA:
        return False, f"La cantidad debe ser al menos {config.CANTIDAD_MINIMA}"
    
    if cantidad > config.CANTIDAD_MAXIMA:
        return False, f"La cantidad no puede ser mayor a {config.CANTIDAD_MAXIMA}"
    
    return True, ""


def validar_precio(precio: int) -> ResultadoValidacion:
    """
    Valida que un precio sea válido (entero positivo).
    
    Args:
        precio: Precio a validar en pesos chilenos
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_precio(1000)
        (True, '')
        >>> validar_precio(0)
        (False, 'El precio debe ser al menos $1')
        >>> validar_precio(-500)
        (False, 'El precio debe ser al menos $1')
    """
    if not isinstance(precio, int):
        return False, "El precio debe ser un número entero"
    
    if precio < config.PRECIO_MINIMO:
        return False, f"El precio debe ser al menos {config.formatear_precio(config.PRECIO_MINIMO)}"
    
    return True, ""


# ============= VALIDACIONES DE TEXTO =============

def validar_texto_no_vacio(texto: str, nombre_campo: str = "campo") -> ResultadoValidacion:
    """
    Valida que un texto no esté vacío.
    
    Args:
        texto: Texto a validar
        nombre_campo: Nombre del campo para el mensaje de error
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_texto_no_vacio("hola", "búsqueda")
        (True, '')
        >>> validar_texto_no_vacio("", "búsqueda")
        (False, 'El campo búsqueda no puede estar vacío')
        >>> validar_texto_no_vacio("   ", "búsqueda")
        (False, 'El campo búsqueda no puede estar vacío')
    """
    # Verificar que no sea None
    if texto is None:
        return False, f"El campo {nombre_campo} no puede estar vacío"
    
    # Verificar que no esté vacío o solo espacios
    if not texto or texto.strip() == "":
        return False, f"El campo {nombre_campo} no puede estar vacío"
    
    return True, ""


def validar_longitud_texto(
    texto: str,
    min_length: int,
    max_length: int,
    nombre_campo: str = "campo"
) -> ResultadoValidacion:
    """
    Valida que un texto tenga una longitud dentro del rango permitido.
    
    Args:
        texto: Texto a validar
        min_length: Longitud mínima
        max_length: Longitud máxima
        nombre_campo: Nombre del campo para mensajes
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_longitud_texto("hola", 2, 10, "nombre")
        (True, '')
        >>> validar_longitud_texto("a", 2, 10, "nombre")
        (False, 'El campo nombre debe tener entre 2 y 10 caracteres')
    """
    # Primero validar que no esté vacío
    es_valido, mensaje = validar_texto_no_vacio(texto, nombre_campo)
    if not es_valido:
        return False, mensaje
    
    # Obtener longitud (sin espacios al inicio/fin)
    longitud = len(texto.strip())
    
    if longitud < min_length:
        return False, f"El campo {nombre_campo} debe tener al menos {min_length} caracteres"
    
    if longitud > max_length:
        return False, f"El campo {nombre_campo} no puede tener más de {max_length} caracteres"
    
    return True, ""


# ============= VALIDACIONES DE OPCIÓN DE MENÚ =============

def validar_opcion_menu(opcion: int) -> ResultadoValidacion:
    """
    Valida que una opción esté en el rango del menú.
    
    Args:
        opcion: Opción del menú
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_opcion_menu(1)
        (True, '')
        >>> validar_opcion_menu(99)
        (False, 'Opción inválida. Debe estar entre 0 y 5')
    """
    if not config.es_opcion_valida(opcion):
        return False, f"Opción inválida. Debe estar entre {config.OPCION_MINIMA} y {config.OPCION_MAXIMA}"
    
    return True, ""


# ============= VALIDACIONES DE CATEGORÍA =============

def validar_categoria(categoria: str) -> ResultadoValidacion:
    """
    Valida que una categoría exista en las categorías válidas.
    
    Args:
        categoria: Categoría a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_categoria("tecnología")
        (True, '')
        >>> validar_categoria("invalida")
        (False, 'Categoría inválida. Categorías válidas: ...')
    """
    # Primero validar que no esté vacía
    es_valido, mensaje = validar_texto_no_vacio(categoria, "categoría")
    if not es_valido:
        return False, mensaje
    
    # Normalizar a minúsculas
    categoria_lower = categoria.lower().strip()
    
    # Verificar si está en las categorías válidas
    if categoria_lower not in config.CATEGORIAS_VALIDAS:
        categorias_str = ", ".join(config.CATEGORIAS_VALIDAS)
        return False, f"Categoría inválida. Categorías válidas: {categorias_str}"
    
    return True, ""


# ============= VALIDACIONES DE CARRITO =============

def validar_carrito_no_vacio(carrito: List[Dict[str, Any]]) -> ResultadoValidacion:
    """
    Valida que el carrito no esté vacío.
    
    Args:
        carrito: Lista de items del carrito
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Example:
        >>> validar_carrito_no_vacio([{'id': 1}])
        (True, '')
        >>> validar_carrito_no_vacio([])
        (False, 'El carrito está vacío')
    """
    if data.es_carrito_vacio(carrito):
        return False, "El carrito está vacío"
    
    return True, ""


# ============= VALIDACIONES COMBINADAS =============

def validar_agregar_al_carrito(
    entrada_id: str,
    entrada_cantidad: str,
    catalogo: List[Dict[str, Any]]
) -> Tuple[bool, int, int, str]:
    """
    Valida todos los datos necesarios para agregar un producto al carrito.
    
    Función que combina múltiples validaciones.
    
    Args:
        entrada_id: String del ID ingresado por usuario
        entrada_cantidad: String de la cantidad ingresada
        catalogo: Lista de productos
        
    Returns:
        Tupla (es_valido, producto_id, cantidad, mensaje_error)
        - es_valido: True si todas las validaciones pasan
        - producto_id: ID convertido (0 si falla)
        - cantidad: Cantidad convertida (0 si falla)
        - mensaje_error: Descripción del error o string vacío
        
    Example:
        >>> catalogo = data.crear_catalogo_inicial()
        >>> validar_agregar_al_carrito("1", "2", catalogo)
        (True, 1, 2, '')
    """
    # Validar y convertir ID
    exito_id, producto_id, mensaje_id = convertir_a_entero(entrada_id)
    if not exito_id:
        return False, 0, 0, mensaje_id
    
    # Validar que el ID exista en el catálogo
    es_valido_id, mensaje_id = validar_id_producto(producto_id, catalogo)
    if not es_valido_id:
        return False, producto_id, 0, mensaje_id
    
    # Validar y convertir cantidad
    exito_cant, cantidad, mensaje_cant = convertir_a_entero(entrada_cantidad)
    if not exito_cant:
        return False, producto_id, 0, mensaje_cant
    
    # Validar que la cantidad esté en el rango
    es_valido_cant, mensaje_cant = validar_cantidad(cantidad)
    if not es_valido_cant:
        return False, producto_id, cantidad, mensaje_cant
    
    # Todas las validaciones pasaron
    return True, producto_id, cantidad, ""


def validar_busqueda(
    termino: str,
    criterio: str
) -> Tuple[bool, str, str, str]:
    """
    Valida los datos de una búsqueda.
    
    Args:
        termino: Término de búsqueda
        criterio: Criterio de búsqueda ('nombre' o 'categoria')
        
    Returns:
        Tupla (es_valido, termino_limpio, criterio_limpio, mensaje_error)
        
    Example:
        >>> validar_busqueda("laptop", "nombre")
        (True, 'laptop', 'nombre', '')
        >>> validar_busqueda("", "nombre")
        (False, '', '', 'El término de búsqueda no puede estar vacío')
    """
    # Validar término
    es_valido_termino, mensaje = validar_texto_no_vacio(termino, "término de búsqueda")
    if not es_valido_termino:
        return False, "", "", mensaje
    
    # Validar longitud mínima del término
    es_valido_long, mensaje = validar_longitud_texto(
        termino,
        config.NOMBRE_MIN_LENGTH,
        config.NOMBRE_MAX_LENGTH,
        "término de búsqueda"
    )
    if not es_valido_long:
        return False, "", "", mensaje
    
    # Normalizar criterio
    criterio_limpio = criterio.lower().strip()
    
    # Validar criterio
    if criterio_limpio not in config.CRITERIOS_BUSQUEDA_VALIDOS:
        criterios_str = ", ".join(config.CRITERIOS_BUSQUEDA_VALIDOS)
        return False, "", "", f"Criterio inválido. Criterios válidos: {criterios_str}"
    
    # Todo válido
    termino_limpio = termino.strip()
    return True, termino_limpio, criterio_limpio, ""


# ============= FUNCIONES DE UTILIDAD =============

def crear_resultado_exitoso() -> ResultadoValidacion:
    """
    Crea un resultado de validación exitoso.
    
    Returns:
        Tupla (True, '')
    """
    return True, ""


def crear_resultado_error(mensaje: str) -> ResultadoValidacion:
    """
    Crea un resultado de validación con error.
    
    Args:
        mensaje: Mensaje de error
        
    Returns:
        Tupla (False, mensaje)
    """
    return False, mensaje


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    print("=== Tests de Validaciones ===\n")
    
    # Test 1: Validación de entrada entero
    print("Test 1: Validación de entrada entero")
    casos = ["123", "-5", "abc", "12.5", "", "  456  "]
    for caso in casos:
        es_valido, mensaje = validar_entrada_entero(caso)
        print(f"  '{caso}': {es_valido} - {mensaje}")
    
    # Test 2: Conversión a entero
    print("\nTest 2: Conversión a entero")
    casos = ["123", "abc", "0"]
    for caso in casos:
        exito, valor, mensaje = convertir_a_entero(caso)
        print(f"  '{caso}': exito={exito}, valor={valor}, mensaje={mensaje}")
    
    # Test 3: Validación de cantidad
    print("\nTest 3: Validación de cantidad")
    cantidades = [0, 1, 5, 999, 1000]
    for cant in cantidades:
        es_valido, mensaje = validar_cantidad(cant)
        print(f"  {cant}: {es_valido} - {mensaje}")
    
    # Test 4: Validación de ID producto
    print("\nTest 4: Validación de ID producto")
    catalogo = data.crear_catalogo_inicial()
    ids = [1, 10, 999]
    for producto_id in ids:
        es_valido, mensaje = validar_id_producto(producto_id, catalogo)
        print(f"  ID {producto_id}: {es_valido} - {mensaje}")
    
    # Test 5: Validación de texto no vacío
    print("\nTest 5: Validación de texto no vacío")
    textos = ["hola", "", "   ", None]
    for texto in textos:
        es_valido, mensaje = validar_texto_no_vacio(str(texto) if texto else "", "test")
        print(f"  '{texto}': {es_valido} - {mensaje}")
    
    # Test 6: Validación combinada para agregar al carrito
    print("\nTest 6: Validación combinada agregar al carrito")
    casos = [
        ("1", "2"),      # Válido
        ("999", "1"),    # ID no existe
        ("1", "0"),      # Cantidad inválida
        ("abc", "2"),    # ID no numérico
    ]
    for entrada_id, entrada_cant in casos:
        es_valido, pid, cant, msg = validar_agregar_al_carrito(
            entrada_id, entrada_cant, catalogo
        )
        print(f"  ID='{entrada_id}', Cant='{entrada_cant}':")
        print(f"    Válido: {es_valido}, ID: {pid}, Cant: {cant}")
        if msg:
            print(f"    Error: {msg}")