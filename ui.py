# -*- coding: utf-8 -*-

"""
Módulo de interfaz de usuario del E-commerce.

Contiene todas las funciones relacionadas con la interacción con el usuario:
menú principal, solicitud de datos, presentación de información.

Patrón aplicado: Presentation Layer
- Separa UI de lógica de negocio
- Coordina flujo de la aplicación
- Maneja input/output del usuario

Principios:
- Funciones enfocadas en UI
- Delegan lógica a business_logic
- Validan input antes de procesar
"""

from typing import List, Dict, Any, Tuple
import config
import data
import validators
import business_logic
import utils


# ============= ESTADO DE LA APLICACIÓN =============

def inicializar_aplicacion() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Inicializa el estado de la aplicación.
    
    Returns:
        Tupla (catalogo, carrito)
        - catalogo: Catálogo inicial de productos
        - carrito: Carrito vacío
    """
    catalogo = data.crear_catalogo_inicial()
    carrito = data.crear_carrito_vacio()
    
    return catalogo, carrito


# ============= MENÚ PRINCIPAL =============

def mostrar_menu_principal() -> None:
    """
    Muestra el menú principal de la aplicación.
    
    Note:
        Esta función tiene side effect (imprime en consola)
    """
    # Limpiar pantalla para mejor visualización
    utils.limpiar_pantalla()
    
    # Mostrar menú desde config
    print(config.obtener_texto_menu())


def solicitar_opcion_menu() -> int:
    """
    Solicita al usuario que seleccione una opción del menú.
    
    Valida que la entrada sea un número entero válido y dentro del rango.
    
    Returns:
        Número de opción seleccionada
        
    Note:
        Esta función tiene side effects (input/output)
    """
    while True:
        # Solicitar entrada
        entrada = utils.solicitar_entrada("Selecciona una opción")
        
        # Validar que sea entero
        exito, valor, mensaje = validators.convertir_a_entero(entrada)
        
        if not exito:
            utils.mostrar_mensaje_error(mensaje)
            utils.pausar()
            mostrar_menu_principal()
            continue
        
        # Validar que esté en rango
        es_valido, mensaje = validators.validar_opcion_menu(valor)
        
        if not es_valido:
            utils.mostrar_mensaje_error(mensaje)
            utils.pausar()
            mostrar_menu_principal()
            continue
        
        # Opción válida
        return valor


# ============= OPCIÓN 1: VER CATÁLOGO =============

def ejecutar_ver_catalogo(catalogo: List[Dict[str, Any]]) -> None:
    """
    Ejecuta la opción de ver el catálogo completo.
    
    Args:
        catalogo: Lista de productos
        
    Note:
        Esta función tiene side effects (imprime en consola)
    """
    utils.limpiar_pantalla()
    
    # Mostrar título
    utils.mostrar_titulo("VER CATÁLOGO DE PRODUCTOS")
    
    # Mostrar catálogo usando utilidad
    utils.mostrar_catalogo_productos(catalogo)
    
    # Mostrar estadísticas adicionales
    stats = business_logic.obtener_estadisticas_catalogo(catalogo)
    print(f"\n📊 Estadísticas:")
    print(f"  • Categorías disponibles: {stats['total_categorias']}")
    print(f"  • Precio promedio: {config.formatear_precio(stats['precio_promedio'])}")
    print(f"  • Rango de precios: {config.formatear_precio(stats['precio_minimo'])} - {config.formatear_precio(stats['precio_maximo'])}")


# ============= OPCIÓN 2: BUSCAR PRODUCTO =============

def ejecutar_buscar_producto(catalogo: List[Dict[str, Any]]) -> None:
    """
    Ejecuta la opción de buscar productos.
    
    Args:
        catalogo: Lista de productos
        
    Note:
        Esta función tiene side effects (input/output)
    """
    utils.limpiar_pantalla()
    
    # Mostrar título
    utils.mostrar_titulo("BUSCAR PRODUCTO")
    
    # Mostrar categorías disponibles
    utils.mostrar_categorias_disponibles(catalogo)
    
    # Solicitar criterio de búsqueda
    print("\nCriterios de búsqueda:")
    print("  1) Por nombre")
    print("  2) Por categoría")
    
    entrada_criterio = utils.solicitar_entrada("Selecciona el criterio (1 o 2)")
    
    # Convertir criterio
    if entrada_criterio == "1":
        criterio = config.CRITERIO_NOMBRE
        campo_texto = "nombre"
    elif entrada_criterio == "2":
        criterio = config.CRITERIO_CATEGORIA
        campo_texto = "categoría"
    else:
        utils.mostrar_mensaje_error("Criterio inválido. Usa 1 o 2")
        return
    
    # Solicitar término de búsqueda
    termino = utils.solicitar_entrada(f"Ingresa el {campo_texto} a buscar")
    
    # Realizar búsqueda
    exito, mensaje, resultados = business_logic.procesar_busqueda_producto(
        termino, criterio, catalogo
    )
    
    if not exito:
        utils.mostrar_mensaje_error(mensaje)
        return
    
    # Mostrar resultados
    utils.limpiar_pantalla()
    titulo_resultados = f"RESULTADOS DE BÚSQUEDA: {campo_texto.upper()} '{termino}'"
    utils.mostrar_lista_productos(resultados, titulo_resultados)
    
    if len(resultados) > 0:
        utils.mostrar_mensaje_exito(mensaje)


# ============= OPCIÓN 3: AGREGAR AL CARRITO =============

def ejecutar_agregar_al_carrito(
    catalogo: List[Dict[str, Any]],
    carrito: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Ejecuta la opción de agregar un producto al carrito.
    
    Args:
        catalogo: Lista de productos
        carrito: Carrito actual
        
    Returns:
        Carrito actualizado (puede ser el mismo si falla)
        
    Note:
        Esta función tiene side effects (input/output)
    """
    utils.limpiar_pantalla()
    
    # Mostrar título
    utils.mostrar_titulo("AGREGAR PRODUCTO AL CARRITO")
    
    # Mostrar catálogo resumido (primeros 10 productos)
    print("\nProductos disponibles (mostrando primeros 10):")
    print(config.SEPARADOR_LINEA)
    print(utils.formatear_encabezado_productos())
    print(config.SEPARADOR_LINEA)
    
    for producto in catalogo[:10]:
        print(utils.formatear_fila_producto(producto))
    
    if len(catalogo) > 10:
        print(f"\n... y {len(catalogo) - 10} productos más")
        print("💡 Usa la opción 1 para ver el catálogo completo")
    
    print(config.SEPARADOR_LINEA)
    
    # Solicitar ID del producto
    entrada_id = utils.solicitar_entrada("Ingresa el ID del producto")
    
    # Solicitar cantidad
    entrada_cantidad = utils.solicitar_entrada("Ingresa la cantidad")
    
    # Procesar operación
    exito, mensaje, nuevo_carrito = business_logic.procesar_agregar_al_carrito(
        entrada_id, entrada_cantidad, catalogo, carrito
    )
    
    # Mostrar resultado
    utils.limpiar_pantalla()
    
    if exito:
        utils.mostrar_mensaje_exito(mensaje)
        
        # Mostrar resumen del carrito
        resumen = business_logic.obtener_resumen_carrito(nuevo_carrito)
        print(f"\n🛒 Resumen del carrito:")
        print(f"  • Productos distintos: {resumen['total_items']}")
        print(f"  • Unidades totales: {resumen['total_unidades']}")
        print(f"  • Total: {config.formatear_precio(resumen['total_pagar'])}")
        
        return nuevo_carrito
    else:
        utils.mostrar_mensaje_error(mensaje)
        return carrito


# ============= OPCIÓN 4: VER CARRITO =============

def ejecutar_ver_carrito(carrito: List[Dict[str, Any]]) -> None:
    """
    Ejecuta la opción de ver el carrito y total.
    
    Args:
        carrito: Carrito actual
        
    Note:
        Esta función tiene side effects (imprime en consola)
    """
    utils.limpiar_pantalla()
    
    # Mostrar carrito usando utilidad
    utils.mostrar_carrito(carrito)
    
    # Si el carrito no está vacío, mostrar información adicional
    if not data.es_carrito_vacio(carrito):
        # Calcular descuento potencial
        total = data.calcular_total_carrito(carrito)
        descuento, total_con_descuento, mensaje_descuento = business_logic.calcular_descuento(total)
        
        if descuento > 0:
            print("\n💰 " + mensaje_descuento)
            print(f"   Total final: {config.formatear_precio(total_con_descuento)}")
            print(config.SEPARADOR_TABLA)


# ============= OPCIÓN 5: VACIAR CARRITO =============

def ejecutar_vaciar_carrito(carrito: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ejecuta la opción de vaciar el carrito.
    
    Args:
        carrito: Carrito actual
        
    Returns:
        Carrito actualizado (vacío si confirma, original si cancela)
        
    Note:
        Esta función tiene side effects (input/output)
    """
    utils.limpiar_pantalla()
    
    # Mostrar título
    utils.mostrar_titulo("VACIAR CARRITO")
    
    # Verificar si el carrito está vacío
    if data.es_carrito_vacio(carrito):
        utils.mostrar_mensaje_info(config.MSG_CARRITO_VACIO)
        return carrito
    
    # Mostrar resumen actual
    resumen = business_logic.obtener_resumen_carrito(carrito)
    print(f"\nCarrito actual:")
    print(f"  • Productos distintos: {resumen['total_items']}")
    print(f"  • Unidades totales: {resumen['total_unidades']}")
    print(f"  • Total: {config.formatear_precio(resumen['total_pagar'])}")
    
    # Solicitar confirmación
    confirmar = utils.solicitar_confirmacion("\n¿Estás seguro de vaciar el carrito?")
    
    if not confirmar:
        utils.mostrar_mensaje_info("Operación cancelada. El carrito se mantiene sin cambios.")
        return carrito
    
    # Procesar vaciado
    exito, mensaje, nuevo_carrito = business_logic.procesar_vaciar_carrito(carrito)
    
    if exito:
        utils.mostrar_mensaje_exito(mensaje)
        return nuevo_carrito
    else:
        utils.mostrar_mensaje_error(mensaje)
        return carrito


# ============= OPCIÓN 0: SALIR =============

def ejecutar_salir() -> bool:
    """
    Ejecuta la opción de salir de la aplicación.
    
    Returns:
        False para indicar que se debe salir del loop principal
        
    Note:
        Esta función tiene side effects (imprime en consola)
    """
    utils.limpiar_pantalla()
    
    # Mostrar mensaje de despedida
    print("\n" + config.SEPARADOR_TABLA)
    print(utils.centrar_texto(config.MSG_DESPEDIDA, 70))
    print(config.SEPARADOR_TABLA)
    print()
    
    return False


# ============= DISPATCHER DE OPCIONES =============

def ejecutar_opcion(
    opcion: int,
    catalogo: List[Dict[str, Any]],
    carrito: List[Dict[str, Any]]
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Ejecuta la opción seleccionada por el usuario.
    
    Patrón aplicado: Command Dispatcher Pattern
    - Mapea opciones a funciones
    - Centraliza ejecución de comandos
    
    Args:
        opcion: Número de opción seleccionada
        catalogo: Lista de productos
        carrito: Carrito actual
        
    Returns:
        Tupla (continuar, nuevo_carrito)
        - continuar: True para continuar loop, False para salir
        - nuevo_carrito: Carrito actualizado
    """
    # Ejecutar según opción
    if opcion == config.OPCION_VER_CATALOGO:
        ejecutar_ver_catalogo(catalogo)
        return True, carrito
    
    elif opcion == config.OPCION_BUSCAR_PRODUCTO:
        ejecutar_buscar_producto(catalogo)
        return True, carrito
    
    elif opcion == config.OPCION_AGREGAR_AL_CARRITO:
        nuevo_carrito = ejecutar_agregar_al_carrito(catalogo, carrito)
        return True, nuevo_carrito
    
    elif opcion == config.OPCION_VER_CARRITO:
        ejecutar_ver_carrito(carrito)
        return True, carrito
    
    elif opcion == config.OPCION_VACIAR_CARRITO:
        nuevo_carrito = ejecutar_vaciar_carrito(carrito)
        return True, nuevo_carrito
    
    elif opcion == config.OPCION_SALIR:
        continuar = ejecutar_salir()
        return continuar, carrito
    
    else:
        # Esto no debería ocurrir si la validación funciona bien
        utils.mostrar_mensaje_error(config.MSG_ERROR_OPCION_INVALIDA)
        return True, carrito


# ============= LOOP PRINCIPAL =============

def ejecutar_aplicacion() -> None:
    """
    Ejecuta el loop principal de la aplicación.
    
    Este es el punto de entrada principal que controla el flujo:
    1. Inicializa la aplicación
    2. Muestra el menú
    3. Solicita opción
    4. Ejecuta la opción
    5. Repite hasta que el usuario salga
    
    Note:
        Esta función contiene el ciclo principal de la aplicación
    """
    # Inicializar estado
    catalogo, carrito = inicializar_aplicacion()
    
    # Variable de control del loop
    continuar = True
    
    # Loop principal (ciclo while)
    while continuar:
        # Mostrar menú
        mostrar_menu_principal()
        
        # Solicitar opción
        opcion = solicitar_opcion_menu()
        
        # Ejecutar opción
        continuar, carrito = ejecutar_opcion(opcion, catalogo, carrito)
        
        # Pausar antes de continuar (excepto si se sale)
        if continuar:
            utils.pausar()


# ============= TESTS BÁSICOS =============

if __name__ == "__main__":
    print("=== Tests de Interfaz de Usuario ===\n")
    
    # Test 1: Inicialización
    print("Test 1: Inicializar aplicación")
    catalogo, carrito = inicializar_aplicacion()
    print(f"  Catálogo cargado: {data.contar_productos_en_catalogo(catalogo)} productos")
    print(f"  Carrito vacío: {data.es_carrito_vacio(carrito)}")
    
    # Test 2: Mostrar menú (comentado para no interferir con tests)
    # print("\nTest 2: Mostrar menú principal")
    # mostrar_menu_principal()
    
    # Test 3: Ver catálogo
    print("\nTest 3: Ver catálogo")
    ejecutar_ver_catalogo(catalogo)
    
    # Test 4: Ver carrito vacío
    print("\nTest 4: Ver carrito vacío")
    ejecutar_ver_carrito(carrito)
    
    # Test 5: Agregar items programáticamente para test
    print("\nTest 5: Simular carrito con productos")
    producto1 = data.buscar_producto_por_id(catalogo, 1)
    producto2 = data.buscar_producto_por_id(catalogo, 5)
    carrito = data.agregar_item_a_carrito(carrito, producto1, 2)
    carrito = data.agregar_item_a_carrito(carrito, producto2, 1)
    ejecutar_ver_carrito(carrito)
    
    print("\n✓ Tests de UI completados")
    print("\nPara ejecutar la aplicación completa, ejecuta:")
    print("  python ecommerce_m3.py")