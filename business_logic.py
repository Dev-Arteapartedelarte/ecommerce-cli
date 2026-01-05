# -*- coding: utf-8 -*-

"""
Módulo de lógica de negocio del E-commerce.

Contiene las operaciones principales del sistema: agregar al carrito,
buscar productos, calcular totales, etc.

Patrón aplicado: Service Layer Pattern
- Capa intermedia entre UI y datos
- Coordina operaciones complejas
- Aplica reglas de negocio

Principios:
- Funciones que orquestan operaciones
- Validaciones antes de modificar datos
- Retornan resultados estructurados
"""

from typing import List, Dict, Any, Tuple
import config
import data
import validators


# ============= TIPO DE RESULTADOS =============

# Type aliases para mejorar legibilidad
ResultadoOperacion = Tuple[bool, str, Any]
# Tupla: (exito: bool, mensaje: str, datos: Any)


# ============= OPERACIONES DEL CARRITO =============

def procesar_agregar_al_carrito(
    entrada_id: str,
    entrada_cantidad: str,
    catalogo: List[Dict[str, Any]],
    carrito: List[Dict[str, Any]]
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Procesa la operación de agregar un producto al carrito.
    
    Esta función coordina:
    1. Validación de entradas
    2. Búsqueda del producto
    3. Agregar al carrito
    4. Retornar resultado
    
    Args:
        entrada_id: String del ID ingresado por usuario
        entrada_cantidad: String de la cantidad ingresada
        catalogo: Lista de productos disponibles
        carrito: Carrito actual
        
    Returns:
        Tupla (exito, mensaje, nuevo_carrito)
        - exito: True si se agregó correctamente
        - mensaje: Mensaje de éxito o error
        - nuevo_carrito: Carrito actualizado (original si falla)
        
    Example:
        >>> catalogo = data.crear_catalogo_inicial()
        >>> carrito = data.crear_carrito_vacio()
        >>> exito, msg, nuevo_carrito = procesar_agregar_al_carrito("1", "2", catalogo, carrito)
        >>> exito
        True
    """
    # Validar todas las entradas
    es_valido, producto_id, cantidad, mensaje_error = validators.validar_agregar_al_carrito(
        entrada_id, entrada_cantidad, catalogo
    )
    
    if not es_valido:
        # Validación falló: retornar carrito sin cambios
        return False, mensaje_error, carrito
    
    # Buscar el producto en el catálogo
    producto = data.buscar_producto_por_id(catalogo, producto_id)
    
    if producto is None:
        # Esto no debería ocurrir si la validación funciona bien
        return False, config.MSG_ERROR_PRODUCTO_NO_EXISTE, carrito
    
    # Agregar al carrito (retorna nuevo carrito)
    nuevo_carrito = data.agregar_item_a_carrito(carrito, producto, cantidad)
    
    # Construir mensaje de éxito
    nombre_producto = producto[config.KEY_NOMBRE]
    precio_unitario = config.formatear_precio(producto[config.KEY_PRECIO])
    subtotal = config.formatear_precio(producto[config.KEY_PRECIO] * cantidad)
    
    mensaje_exito = (
        f"{config.MSG_PRODUCTO_AGREGADO}\n"
        f"  Producto: {nombre_producto}\n"
        f"  Cantidad: {cantidad} unidad(es)\n"
        f"  Precio unitario: {precio_unitario}\n"
        f"  Subtotal: {subtotal}"
    )
    
    return True, mensaje_exito, nuevo_carrito


def procesar_vaciar_carrito(
    carrito: List[Dict[str, Any]]
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Procesa la operación de vaciar el carrito.
    
    Args:
        carrito: Carrito actual
        
    Returns:
        Tupla (exito, mensaje, carrito_vacio)
        
    Example:
        >>> carrito = [{'id': 1, 'cantidad': 2}]
        >>> exito, msg, nuevo = procesar_vaciar_carrito(carrito)
        >>> len(nuevo)
        0
    """
    # Validar que el carrito no esté vacío
    es_valido, mensaje_error = validators.validar_carrito_no_vacio(carrito)
    
    if not es_valido:
        return False, mensaje_error, carrito
    
    # Crear carrito vacío
    carrito_vacio = data.crear_carrito_vacio()
    
    # Construir mensaje de éxito
    items_eliminados = data.contar_items_en_carrito(carrito)
    mensaje_exito = f"{config.MSG_CARRITO_VACIADO} ({items_eliminados} producto(s) eliminado(s))"
    
    return True, mensaje_exito, carrito_vacio


def obtener_resumen_carrito(
    carrito: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Obtiene un resumen completo del carrito.
    
    Args:
        carrito: Lista de items del carrito
        
    Returns:
        Diccionario con estadísticas del carrito:
        - esta_vacio: bool
        - total_items: int (productos distintos)
        - total_unidades: int (suma de cantidades)
        - total_pagar: int (suma de subtotales)
        - items: list (los items del carrito)
        
    Example:
        >>> carrito = [{'cantidad': 2, 'subtotal': 1000}]
        >>> resumen = obtener_resumen_carrito(carrito)
        >>> resumen['total_items']
        1
        >>> resumen['total_unidades']
        2
    """
    resumen = {
        'esta_vacio': data.es_carrito_vacio(carrito),
        'total_items': data.contar_items_en_carrito(carrito),
        'total_unidades': data.contar_unidades_en_carrito(carrito),
        'total_pagar': data.calcular_total_carrito(carrito),
        'items': carrito
    }
    
    return resumen


# ============= OPERACIONES DE BÚSQUEDA =============

def procesar_busqueda_producto(
    termino: str,
    criterio: str,
    catalogo: List[Dict[str, Any]]
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Procesa la búsqueda de productos según el criterio.
    
    Patrón aplicado: Strategy Pattern (funcional)
    - Selecciona algoritmo de búsqueda según criterio
    - Permite agregar nuevos criterios fácilmente
    
    Args:
        termino: Término de búsqueda
        criterio: 'nombre' o 'categoria'
        catalogo: Lista de productos
        
    Returns:
        Tupla (exito, mensaje, resultados)
        - exito: True si la búsqueda fue exitosa
        - mensaje: Mensaje descriptivo
        - resultados: Lista de productos encontrados
        
    Example:
        >>> catalogo = data.crear_catalogo_inicial()
        >>> exito, msg, resultados = procesar_busqueda_producto("laptop", "nombre", catalogo)
        >>> len(resultados) > 0
        True
    """
    # Validar entradas
    es_valido, termino_limpio, criterio_limpio, mensaje_error = validators.validar_busqueda(
        termino, criterio
    )
    
    if not es_valido:
        return False, mensaje_error, []
    
    # Estrategia de búsqueda según criterio
    # Diccionario que mapea criterios a funciones (Strategy Pattern)
    estrategias_busqueda = {
        config.CRITERIO_NOMBRE: data.buscar_productos_por_nombre,
        config.CRITERIO_CATEGORIA: data.obtener_productos_por_categoria
    }
    
    # Obtener la función de búsqueda correspondiente
    funcion_busqueda = estrategias_busqueda.get(criterio_limpio)
    
    if funcion_busqueda is None:
        # Esto no debería ocurrir si la validación funciona bien
        return False, "Criterio de búsqueda no válido", []
    
    # Ejecutar búsqueda
    resultados = funcion_busqueda(catalogo, termino_limpio)
    
    # Construir mensaje
    if len(resultados) == 0:
        mensaje = config.MSG_NO_RESULTADOS_BUSQUEDA
        return True, mensaje, resultados
    
    criterio_texto = "nombre" if criterio_limpio == config.CRITERIO_NOMBRE else "categoría"
    mensaje = f"Se encontraron {len(resultados)} producto(s) con {criterio_texto} '{termino_limpio}'"
    
    return True, mensaje, resultados


def buscar_por_nombre(
    termino: str,
    catalogo: List[Dict[str, Any]]
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Atajo para buscar productos por nombre.
    
    Args:
        termino: Término a buscar
        catalogo: Lista de productos
        
    Returns:
        Tupla (exito, mensaje, resultados)
    """
    return procesar_busqueda_producto(termino, config.CRITERIO_NOMBRE, catalogo)


def buscar_por_categoria(
    categoria: str,
    catalogo: List[Dict[str, Any]]
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Atajo para buscar productos por categoría.
    
    Args:
        categoria: Categoría a buscar
        catalogo: Lista de productos
        
    Returns:
        Tupla (exito, mensaje, resultados)
    """
    return procesar_busqueda_producto(categoria, config.CRITERIO_CATEGORIA, catalogo)


# ============= OPERACIONES DEL CATÁLOGO =============

def obtener_catalogo_completo(
    catalogo: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Obtiene información completa del catálogo.
    
    Args:
        catalogo: Lista de productos
        
    Returns:
        Diccionario con información del catálogo:
        - total_productos: int
        - categorias: list
        - productos: list
    """
    informacion = {
        'total_productos': data.contar_productos_en_catalogo(catalogo),
        'categorias': data.obtener_todas_las_categorias(catalogo),
        'productos': catalogo
    }
    
    return informacion


def obtener_estadisticas_catalogo(
    catalogo: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calcula estadísticas del catálogo.
    
    Args:
        catalogo: Lista de productos
        
    Returns:
        Diccionario con estadísticas:
        - total_productos: int
        - total_categorias: int
        - productos_por_categoria: dict
        - precio_promedio: int
        - precio_minimo: int
        - precio_maximo: int
    """
    # Contar productos por categoría
    categorias = data.obtener_todas_las_categorias(catalogo)
    productos_por_categoria = {}
    
    for categoria in categorias:
        productos = data.obtener_productos_por_categoria(catalogo, categoria)
        productos_por_categoria[categoria] = len(productos)
    
    # Calcular estadísticas de precios
    precios = [producto[config.KEY_PRECIO] for producto in catalogo]
    
    estadisticas = {
        'total_productos': len(catalogo),
        'total_categorias': len(categorias),
        'productos_por_categoria': productos_por_categoria,
        'precio_promedio': sum(precios) // len(precios) if precios else 0,
        'precio_minimo': min(precios) if precios else 0,
        'precio_maximo': max(precios) if precios else 0
    }
    
    return estadisticas


# ============= OPERACIONES DE VALIDACIÓN DE NEGOCIO =============

def puede_agregar_al_carrito(
    producto_id: int,
    cantidad: int,
    catalogo: List[Dict[str, Any]]
) -> Tuple[bool, str]:
    """
    Valida si se puede agregar un producto al carrito.
    
    Aplica reglas de negocio:
    - El producto debe existir
    - La cantidad debe ser válida
    - (Futuro: verificar stock, límites por cliente, etc.)
    
    Args:
        producto_id: ID del producto
        cantidad: Cantidad a agregar
        catalogo: Lista de productos
        
    Returns:
        Tupla (puede_agregar, mensaje_error)
    """
    # Validar ID
    es_valido, mensaje = validators.validar_id_producto(producto_id, catalogo)
    if not es_valido:
        return False, mensaje
    
    # Validar cantidad
    es_valido, mensaje = validators.validar_cantidad(cantidad)
    if not es_valido:
        return False, mensaje
    
    # Todas las reglas de negocio se cumplen
    return True, ""


def calcular_descuento(total: int) -> Tuple[int, int, str]:
    """
    Calcula descuento según el total de compra.
    
    Reglas de negocio (ejemplo):
    - Compras >= $100.000: 5% descuento
    - Compras >= $200.000: 10% descuento
    - Compras >= $500.000: 15% descuento
    
    Args:
        total: Total de la compra
        
    Returns:
        Tupla (descuento, total_con_descuento, mensaje)
        
    Example:
        >>> calcular_descuento(150000)
        (7500, 142500, 'Descuento 5% aplicado')
    
    Note:
        Esta función demuestra cómo agregar lógica de negocio
        sin modificar otras partes del código.
    """
    # Sin descuento por defecto
    if total < 100000:
        return 0, total, ""
    
    # Determinar porcentaje de descuento
    if total >= 500000:
        porcentaje = 15
    elif total >= 200000:
        porcentaje = 10
    else:
        porcentaje = 5
    
    # Calcular descuento
    descuento = (total * porcentaje) // 100
    total_con_descuento = total - descuento
    
    mensaje = f"¡Descuento del {porcentaje}% aplicado! Ahorras {config.formatear_precio(descuento)}"
    
    return descuento, total_con_descuento, mensaje


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    print("=== Tests de Lógica de Negocio ===\n")
    
    # Inicializar datos
    catalogo = data.crear_catalogo_inicial()
    carrito = data.crear_carrito_vacio()
    
    # Test 1: Agregar al carrito
    print("Test 1: Agregar producto al carrito")
    exito, mensaje, carrito = procesar_agregar_al_carrito("1", "2", catalogo, carrito)
    print(f"  Éxito: {exito}")
    print(f"  Mensaje: {mensaje}")
    
    # Test 2: Resumen del carrito
    print("\nTest 2: Resumen del carrito")
    resumen = obtener_resumen_carrito(carrito)
    print(f"  Vacío: {resumen['esta_vacio']}")
    print(f"  Items: {resumen['total_items']}")
    print(f"  Unidades: {resumen['total_unidades']}")
    print(f"  Total: {config.formatear_precio(resumen['total_pagar'])}")
    
    # Test 3: Búsqueda por nombre
    print("\nTest 3: Búsqueda por nombre")
    exito, mensaje, resultados = buscar_por_nombre("laptop", catalogo)
    print(f"  Éxito: {exito}")
    print(f"  Mensaje: {mensaje}")
    print(f"  Resultados: {len(resultados)}")
    
    # Test 4: Búsqueda por categoría
    print("\nTest 4: Búsqueda por categoría")
    exito, mensaje, resultados = buscar_por_categoria("tecnología", catalogo)
    print(f"  Éxito: {exito}")
    print(f"  Mensaje: {mensaje}")
    print(f"  Resultados: {len(resultados)}")
    
    # Test 5: Estadísticas del catálogo
    print("\nTest 5: Estadísticas del catálogo")
    stats = obtener_estadisticas_catalogo(catalogo)
    print(f"  Total productos: {stats['total_productos']}")
    print(f"  Total categorías: {stats['total_categorias']}")
    print(f"  Precio promedio: {config.formatear_precio(stats['precio_promedio'])}")
    print(f"  Precio mínimo: {config.formatear_precio(stats['precio_minimo'])}")
    print(f"  Precio máximo: {config.formatear_precio(stats['precio_maximo'])}")
    print("  Productos por categoría:")
    for cat, cant in stats['productos_por_categoria'].items():
        print(f"    - {cat}: {cant}")
    
    # Test 6: Cálculo de descuentos
    print("\nTest 6: Cálculo de descuentos")
    totales_prueba = [50000, 150000, 250000, 600000]
    for total in totales_prueba:
        descuento, total_desc, mensaje = calcular_descuento(total)
        print(f"  Total: {config.formatear_precio(total)}")
        if descuento > 0:
            print(f"    {mensaje}")
            print(f"    Total con descuento: {config.formatear_precio(total_desc)}")
        else:
            print(f"    Sin descuento")
    
    # Test 7: Vaciar carrito
    print("\nTest 7: Vaciar carrito")
    exito, mensaje, carrito = procesar_vaciar_carrito(carrito)
    print(f"  Éxito: {exito}")
    print(f"  Mensaje: {mensaje}")
    print(f"  Items restantes: {data.contar_items_en_carrito(carrito)}")