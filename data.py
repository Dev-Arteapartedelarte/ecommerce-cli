# -*- coding: utf-8 -*-
"""
Módulo de datos del E-commerce.

Define el catálogo de productos y funciones para manipular datos.
Implementa el patrón Repository de forma funcional.

Patrón aplicado: Repository Pattern (funcional)
- Abstrae el acceso a datos
- Centraliza operaciones CRUD
- Permite cambiar implementación sin afectar lógica

NOTA: Precios en pesos chilenos (CLP) - valores enteros sin decimales
"""

from typing import List, Dict, Optional, Any
import config


# ============= TIPO DE DATOS =============

# Type alias para mejorar legibilidad
Producto = Dict[str, Any]  # {'id': int, 'nombre': str, 'categoria': str, 'precio': int}
ItemCarrito = Dict[str, Any]  # Producto + {'cantidad': int, 'subtotal': int}


# ============= CATÁLOGO DE PRODUCTOS =============

def crear_catalogo_inicial() -> List[Producto]:
    """
    Crea el catálogo inicial de productos del e-commerce.
    
    Patrón aplicado: Factory Function
    - Encapsula la creación del catálogo
    - Facilita modificar productos sin tocar otras partes
    - Retorna una nueva lista cada vez (inmutabilidad)
    
    Returns:
        Lista con el catálogo de productos
        
    Note:
        Cada producto DEBE tener: id, nombre, categoria, precio
        - id: entero único y positivo
        - nombre: string descriptivo
        - categoria: string de CATEGORIAS_VALIDAS
        - precio: int (pesos chilenos, sin decimales)
    """
    catalogo = [
        # Categoría: Tecnología
        {
            config.KEY_ID: 1,
            config.KEY_NOMBRE: "Laptop HP Pavilion 15",
            config.KEY_CATEGORIA: "tecnología",
            config.KEY_PRECIO: 599990
        },
        {
            config.KEY_ID: 2,
            config.KEY_NOMBRE: "Mouse Inalámbrico Logitech",
            config.KEY_CATEGORIA: "tecnología",
            config.KEY_PRECIO: 15990
        },
        {
            config.KEY_ID: 3,
            config.KEY_NOMBRE: "Teclado Mecánico RGB",
            config.KEY_CATEGORIA: "tecnología",
            config.KEY_PRECIO: 45990
        },
        {
            config.KEY_ID: 4,
            config.KEY_NOMBRE: "Monitor 24 pulgadas Full HD",
            config.KEY_CATEGORIA: "tecnología",
            config.KEY_PRECIO: 129990
        },
        
        # Categoría: Ropa
        {
            config.KEY_ID: 5,
            config.KEY_NOMBRE: "Polera Básica Algodón",
            config.KEY_CATEGORIA: "ropa",
            config.KEY_PRECIO: 9990
        },
        {
            config.KEY_ID: 6,
            config.KEY_NOMBRE: "Jeans Slim Fit",
            config.KEY_CATEGORIA: "ropa",
            config.KEY_PRECIO: 29990
        },
        {
            config.KEY_ID: 7,
            config.KEY_NOMBRE: "Chaqueta Impermeable",
            config.KEY_CATEGORIA: "ropa",
            config.KEY_PRECIO: 49990
        },
        {
            config.KEY_ID: 8,
            config.KEY_NOMBRE: "Zapatillas Deportivas",
            config.KEY_CATEGORIA: "ropa",
            config.KEY_PRECIO: 39990
        },
        
        # Categoría: Hogar
        {
            config.KEY_ID: 9,
            config.KEY_NOMBRE: "Lámpara LED Escritorio",
            config.KEY_CATEGORIA: "hogar",
            config.KEY_PRECIO: 19990
        },
        {
            config.KEY_ID: 10,
            config.KEY_NOMBRE: "Set de Sartenes Antiadherentes",
            config.KEY_CATEGORIA: "hogar",
            config.KEY_PRECIO: 39990
        },
        {
            config.KEY_ID: 11,
            config.KEY_NOMBRE: "Almohada Memory Foam",
            config.KEY_CATEGORIA: "hogar",
            config.KEY_PRECIO: 24990
        },
        
        # Categoría: Deportes
        {
            config.KEY_ID: 12,
            config.KEY_NOMBRE: "Pelota de Fútbol Profesional",
            config.KEY_CATEGORIA: "deportes",
            config.KEY_PRECIO: 24990
        },
        {
            config.KEY_ID: 13,
            config.KEY_NOMBRE: "Botella Térmica 1L",
            config.KEY_CATEGORIA: "deportes",
            config.KEY_PRECIO: 12990
        },
        {
            config.KEY_ID: 14,
            config.KEY_NOMBRE: "Pesas Mancuernas 5kg (Par)",
            config.KEY_CATEGORIA: "deportes",
            config.KEY_PRECIO: 19990
        },
        
        # Categoría: Libros
        {
            config.KEY_ID: 15,
            config.KEY_NOMBRE: "Python Crash Course",
            config.KEY_CATEGORIA: "libros",
            config.KEY_PRECIO: 34990
        },
        {
            config.KEY_ID: 16,
            config.KEY_NOMBRE: "Clean Code (Robert Martin)",
            config.KEY_CATEGORIA: "libros",
            config.KEY_PRECIO: 39990
        },
        {
            config.KEY_ID: 17,
            config.KEY_NOMBRE: "El Principito",
            config.KEY_CATEGORIA: "libros",
            config.KEY_PRECIO: 8990
        },
        
        # Categoría: Alimentos
        {
            config.KEY_ID: 18,
            config.KEY_NOMBRE: "Café Colombiano Premium 500g",
            config.KEY_CATEGORIA: "alimentos",
            config.KEY_PRECIO: 7990
        },
        {
            config.KEY_ID: 19,
            config.KEY_NOMBRE: "Aceite de Oliva Extra Virgen 1L",
            config.KEY_CATEGORIA: "alimentos",
            config.KEY_PRECIO: 12990
        },
        {
            config.KEY_ID: 20,
            config.KEY_NOMBRE: "Miel Orgánica 500g",
            config.KEY_CATEGORIA: "alimentos",
            config.KEY_PRECIO: 9990
        }
    ]
    
    return catalogo


# ============= OPERACIONES DEL CATÁLOGO (Repository Pattern) =============

def buscar_producto_por_id(catalogo: List[Producto], producto_id: int) -> Optional[Producto]:
    """
    Busca un producto en el catálogo por su ID.
    
    Función pura: no modifica el catálogo, solo consulta.
    
    Args:
        catalogo: Lista de productos
        producto_id: ID del producto a buscar
        
    Returns:
        Diccionario del producto si existe, None si no existe
        
    Example:
        >>> catalogo = crear_catalogo_inicial()
        >>> producto = buscar_producto_por_id(catalogo, 1)
        >>> producto['nombre']
        'Laptop HP Pavilion 15'
    """
    # Recorrer catálogo buscando el ID
    for producto in catalogo:
        if producto[config.KEY_ID] == producto_id:
            # Retornar copia para evitar modificaciones externas
            return producto.copy()
    
    # No encontrado
    return None


def obtener_productos_por_categoria(catalogo: List[Producto], categoria: str) -> List[Producto]:
    """
    Filtra productos por categoría.
    
    Patrón aplicado: Filter Pattern
    - Función de orden superior
    - No modifica el catálogo original
    
    Args:
        catalogo: Lista de productos
        categoria: Categoría a filtrar (case-insensitive)
        
    Returns:
        Lista de productos que pertenecen a la categoría
        
    Example:
        >>> catalogo = crear_catalogo_inicial()
        >>> tecnologia = obtener_productos_por_categoria(catalogo, "tecnología")
        >>> len(tecnologia)
        4
    """
    # Normalizar categoría a minúsculas para comparación
    categoria_lower = categoria.lower()
    
    # List comprehension pythonic
    return [
        producto.copy()
        for producto in catalogo
        if producto[config.KEY_CATEGORIA].lower() == categoria_lower
    ]


def buscar_productos_por_nombre(catalogo: List[Producto], termino: str) -> List[Producto]:
    """
    Busca productos cuyo nombre contenga el término de búsqueda.
    
    Búsqueda case-insensitive y parcial.
    
    Args:
        catalogo: Lista de productos
        termino: Texto a buscar en los nombres
        
    Returns:
        Lista de productos que coinciden
        
    Example:
        >>> catalogo = crear_catalogo_inicial()
        >>> resultados = buscar_productos_por_nombre(catalogo, "laptop")
        >>> len(resultados)
        1
    """
    # Normalizar término de búsqueda
    termino_lower = termino.lower()
    
    # Buscar coincidencias parciales
    return [
        producto.copy()
        for producto in catalogo
        if termino_lower in producto[config.KEY_NOMBRE].lower()
    ]


def obtener_todas_las_categorias(catalogo: List[Producto]) -> List[str]:
    """
    Obtiene lista única de todas las categorías en el catálogo.
    
    Args:
        catalogo: Lista de productos
        
    Returns:
        Lista de categorías únicas (ordenadas)
        
    Example:
        >>> catalogo = crear_catalogo_inicial()
        >>> categorias = obtener_todas_las_categorias(catalogo)
        >>> 'tecnología' in categorias
        True
    """
    # Usar set para eliminar duplicados, luego convertir a lista ordenada
    categorias_unicas = set(
        producto[config.KEY_CATEGORIA]
        for producto in catalogo
    )
    
    return sorted(list(categorias_unicas))


def contar_productos_en_catalogo(catalogo: List[Producto]) -> int:
    """
    Cuenta el total de productos en el catálogo.
    
    Args:
        catalogo: Lista de productos
        
    Returns:
        Número total de productos
    """
    return len(catalogo)


# ============= OPERACIONES DEL CARRITO =============

def crear_carrito_vacio() -> List[ItemCarrito]:
    """
    Crea un carrito vacío.
    
    Patrón aplicado: Factory Function
    
    Returns:
        Lista vacía que representa el carrito
    """
    return []


def crear_item_carrito(producto: Producto, cantidad: int) -> ItemCarrito:
    """
    Crea un item del carrito a partir de un producto y cantidad.
    
    Args:
        producto: Diccionario del producto
        cantidad: Cantidad a agregar
        
    Returns:
        Diccionario con producto + cantidad + subtotal
        
    Example:
        >>> producto = {'id': 1, 'nombre': 'Laptop', 'categoria': 'tech', 'precio': 1000}
        >>> item = crear_item_carrito(producto, 2)
        >>> item['subtotal']
        2000
        
    Note:
        El subtotal se calcula como: precio * cantidad (ambos enteros)
    """
    # Calcular subtotal (ambos son int, resultado es int)
    subtotal = producto[config.KEY_PRECIO] * cantidad
    
    # Crear nuevo diccionario combinando producto con info del carrito
    item = producto.copy()
    item[config.KEY_CANTIDAD] = cantidad
    item[config.KEY_SUBTOTAL] = subtotal
    
    return item


def buscar_item_en_carrito(carrito: List[ItemCarrito], producto_id: int) -> Optional[int]:
    """
    Busca un producto en el carrito y retorna su índice.
    
    Args:
        carrito: Lista de items del carrito
        producto_id: ID del producto a buscar
        
    Returns:
        Índice del item si existe, None si no existe
    """
    # Recorrer carrito con enumerate para obtener índice
    for indice, item in enumerate(carrito):
        if item[config.KEY_ID] == producto_id:
            return indice
    
    return None


def agregar_item_a_carrito(
    carrito: List[ItemCarrito],
    producto: Producto,
    cantidad: int
) -> List[ItemCarrito]:
    """
    Agrega un producto al carrito o actualiza cantidad si ya existe.
    
    Patrón aplicado: Pure Function
    - No modifica el carrito original
    - Retorna nuevo carrito
    
    Args:
        carrito: Lista actual del carrito
        producto: Producto a agregar
        cantidad: Cantidad a agregar
        
    Returns:
        Nuevo carrito con el producto agregado/actualizado
    """
    # Crear copia del carrito para no modificar el original
    nuevo_carrito = [item.copy() for item in carrito]
    
    # Buscar si el producto ya está en el carrito
    indice = buscar_item_en_carrito(nuevo_carrito, producto[config.KEY_ID])
    
    if indice is not None:
        # Producto ya existe: actualizar cantidad y subtotal
        nuevo_carrito[indice][config.KEY_CANTIDAD] += cantidad
        nuevo_carrito[indice][config.KEY_SUBTOTAL] = (
            nuevo_carrito[indice][config.KEY_PRECIO] * 
            nuevo_carrito[indice][config.KEY_CANTIDAD]
        )
    else:
        # Producto nuevo: crear item y agregar
        item = crear_item_carrito(producto, cantidad)
        nuevo_carrito.append(item)
    
    return nuevo_carrito


def calcular_total_carrito(carrito: List[ItemCarrito]) -> int:
    """
    Calcula el total a pagar del carrito en pesos chilenos.
    
    Función pura: no modifica el carrito.
    
    Args:
        carrito: Lista de items del carrito
        
    Returns:
        Total a pagar en pesos (entero)
        
    Example:
        >>> item1 = {'subtotal': 1000}
        >>> item2 = {'subtotal': 500}
        >>> total = calcular_total_carrito([item1, item2])
        >>> total
        1500
    """
    # Sumar todos los subtotales usando sum() pythonic
    # Como todos los subtotales son int, el resultado es int
    return sum(item[config.KEY_SUBTOTAL] for item in carrito)


def contar_items_en_carrito(carrito: List[ItemCarrito]) -> int:
    """
    Cuenta el número de items (productos distintos) en el carrito.
    
    Args:
        carrito: Lista de items
        
    Returns:
        Número de items distintos
    """
    return len(carrito)


def contar_unidades_en_carrito(carrito: List[ItemCarrito]) -> int:
    """
    Cuenta el número total de unidades en el carrito.
    
    Suma las cantidades de todos los items.
    
    Args:
        carrito: Lista de items
        
    Returns:
        Número total de unidades
        
    Example:
        >>> item1 = {'cantidad': 2}
        >>> item2 = {'cantidad': 3}
        >>> total = contar_unidades_en_carrito([item1, item2])
        >>> total
        5
    """
    return sum(item[config.KEY_CANTIDAD] for item in carrito)


def es_carrito_vacio(carrito: List[ItemCarrito]) -> bool:
    """
    Verifica si el carrito está vacío.
    
    Args:
        carrito: Lista de items
        
    Returns:
        True si está vacío, False si tiene items
    """
    return len(carrito) == 0


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    # Tests básicos para verificar funcionamiento
    print("=== Tests de Data (Precios en Pesos Chilenos) ===\n")
    
    # Test 1: Crear catálogo
    print("Test 1: Catálogo inicial")
    catalogo = crear_catalogo_inicial()
    print(f"  Total productos: {contar_productos_en_catalogo(catalogo)}")
    print(f"  Categorías: {obtener_todas_las_categorias(catalogo)}")
    
    # Test 2: Buscar producto por ID
    print("\nTest 2: Buscar por ID")
    producto = buscar_producto_por_id(catalogo, 1)
    if producto:
        print(f"  Encontrado: {producto[config.KEY_NOMBRE]}")
        print(f"  Precio: {config.formatear_precio(producto[config.KEY_PRECIO])}")
    
    # Test 3: Buscar por categoría
    print("\nTest 3: Filtrar por categoría 'tecnología'")
    tecnologia = obtener_productos_por_categoria(catalogo, "tecnología")
    print(f"  Productos encontrados: {len(tecnologia)}")
    for prod in tecnologia:
        print(f"    - {prod[config.KEY_NOMBRE]}: {config.formatear_precio(prod[config.KEY_PRECIO])}")
    
    # Test 4: Buscar por nombre
    print("\nTest 4: Buscar por nombre 'laptop'")
    resultados = buscar_productos_por_nombre(catalogo, "laptop")
    print(f"  Resultados: {len(resultados)}")
    
    # Test 5: Operaciones del carrito con precios enteros
    print("\nTest 5: Operaciones del carrito")
    carrito = crear_carrito_vacio()
    print(f"  Carrito vacío: {es_carrito_vacio(carrito)}")
    
    # Agregar producto
    producto1 = buscar_producto_por_id(catalogo, 1)
    carrito = agregar_item_a_carrito(carrito, producto1, 2)
    print(f"  Después de agregar: {contar_items_en_carrito(carrito)} productos distintos")
    print(f"  Unidades totales: {contar_unidades_en_carrito(carrito)}")
    print(f"  Total: {config.formatear_precio(calcular_total_carrito(carrito))}")
    
    # Agregar mismo producto (debe actualizar cantidad)
    carrito = agregar_item_a_carrito(carrito, producto1, 1)
    print(f"  Después de agregar más: {carrito[0][config.KEY_CANTIDAD]} unidades del mismo producto")
    print(f"  Unidades totales: {contar_unidades_en_carrito(carrito)}")
    print(f"  Total: {config.formatear_precio(calcular_total_carrito(carrito))}")
    
    # Agregar producto diferente
    producto2 = buscar_producto_por_id(catalogo, 5)
    carrito = agregar_item_a_carrito(carrito, producto2, 3)
    print(f"  Después de agregar otro producto: {contar_items_en_carrito(carrito)} productos distintos")
    print(f"  Unidades totales: {contar_unidades_en_carrito(carrito)}")
    print(f"  Total: {config.formatear_precio(calcular_total_carrito(carrito))}")
    
    # Test 6: Precios típicos chilenos
    print("\nTest 6: Ejemplos de precios chilenos")
    productos_ejemplo = [
        buscar_producto_por_id(catalogo, 2),   # Mouse
        buscar_producto_por_id(catalogo, 5),   # Polera
        buscar_producto_por_id(catalogo, 18),  # Café
    ]
    for prod in productos_ejemplo:
        print(f"  {prod[config.KEY_NOMBRE]:40} {config.formatear_precio(prod[config.KEY_PRECIO])}")