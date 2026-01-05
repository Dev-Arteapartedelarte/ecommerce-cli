# 🛒 E-commerce Python - Sistema de Gestión de Productos

## URL : https://github.com/Dev-Arteapartedelarte/ecommerce-cli

Sistema de e-commerce desarrollado en Python con interfaz de consola, implementando patrones de diseño funcionales y mejores prácticas de programación.

## 📋 Descripción

Aplicación de consola que simula un e-commerce básico con las siguientes funcionalidades:

- ✅ Ver catálogo completo de productos
- ✅ Buscar productos por nombre o categoría
- ✅ Agregar productos al carrito de compras
- ✅ Ver carrito con detalle y total a pagar
- ✅ Vaciar carrito
- ✅ Cálculo automático de descuentos por monto

## 🚀 Cómo Ejecutar

### Requisitos

- Python 3.10 o superior
- No requiere librerías externas (solo biblioteca estándar)

### Ejecución

```bash
python ecommerce_m3.py
```

### Verificar Versión de Python

```bash
python --version
# Debe mostrar Python 3.10.x o superior
```

## 📂 Estructura del Proyecto

```
ecommerce/
│
├── ecommerce_m3.py          # Punto de entrada principal
├── config.py                # Configuración y constantes
├── data.py                  # Catálogo y manejo de datos
├── validators.py            # Validaciones sin excepciones
├── utils.py                 # Utilidades de interfaz
├── business_logic.py        # Lógica de negocio
├── ui.py                    # Interfaz de usuario
│
└── README.md                # Este archivo
```

## 🎮 Uso de la Aplicación

### Menú Principal

Al ejecutar el programa, verás el siguiente menú:

```
======================================================================
              🛒 Bienvenido/a a E-commerce Python Chile
======================================================================

MENÚ PRINCIPAL:

  1) Ver catálogo de productos
  2) Buscar producto por nombre o categoría
  3) Agregar producto al carrito
  4) Ver carrito y total
  5) Vaciar carrito
  0) Salir

----------------------------------------------------------------------
```

### Opción 1: Ver Catálogo

Muestra todos los productos disponibles con:
- ID único
- Nombre del producto
- Categoría
- Precio en pesos chilenos

**Ejemplo de salida:**
```
   ID NOMBRE                         CATEGORÍA       PRECIO
----------------------------------------------------------------------
    1 Laptop HP Pavilion 15          tecnología      $599.990
    2 Mouse Inalámbrico Logitech     tecnología       $15.990
    3 Teclado Mecánico RGB           tecnología       $45.990
```

### Opción 2: Buscar Producto

Permite buscar productos de dos formas:

**Por nombre:**
```
Selecciona el criterio (1 o 2): 1
Ingresa el nombre a buscar: laptop
```

**Por categoría:**
```
Selecciona el criterio (1 o 2): 2
Ingresa la categoría a buscar: tecnología
```

**Categorías disponibles:**
- alimentos
- deportes
- hogar
- libros
- ropa
- tecnología

### Opción 3: Agregar al Carrito

Permite agregar productos al carrito:

```
Ingresa el ID del producto: 1
Ingresa la cantidad: 2

✓ Producto agregado al carrito exitosamente
  Producto: Laptop HP Pavilion 15
  Cantidad: 2 unidad(es)
  Precio unitario: $599.990
  Subtotal: $1.199.980
```

**Validaciones:**
- ID debe existir en el catálogo
- Cantidad debe ser entre 1 y 999
- Si el producto ya está en el carrito, suma las cantidades

### Opción 4: Ver Carrito

Muestra el contenido del carrito con detalle:

```
======================================================================
                      🛒 CARRITO DE COMPRAS
======================================================================
   ID NOMBRE                         CANT.      PRECIO UNIT.      SUBTOTAL
----------------------------------------------------------------------
    1 Laptop HP Pavilion 15            2          $599.990     $1.199.980
    5 Polera Básica Algodón            3            $9.990        $29.970
----------------------------------------------------------------------
Productos distintos: 2
Unidades totales: 5
======================================================================
TOTAL A PAGAR: $1.229.950
======================================================================
```

**Descuentos automáticos:**
- Compras ≥ $100.000: 5% de descuento
- Compras ≥ $200.000: 10% de descuento
- Compras ≥ $500.000: 15% de descuento

### Opción 5: Vaciar Carrito

Solicita confirmación antes de vaciar:

```
¿Estás seguro de vaciar el carrito? (s/n): s

✓ Carrito vaciado correctamente (2 producto(s) eliminado(s))
```

### Opción 0: Salir

Sale de la aplicación mostrando mensaje de despedida.

## 🏗️ Arquitectura y Patrones de Diseño

### Patrones Implementados

#### 1. Repository Pattern (Funcional)
Abstrae el acceso a datos del catálogo y carrito.

```python
# data.py
def buscar_producto_por_id(catalogo, producto_id):
    # Encapsula la lógica de búsqueda
```

#### 2. Service Layer Pattern
Coordina operaciones entre capas.

```python
# business_logic.py
def procesar_agregar_al_carrito(entrada_id, entrada_cantidad, catalogo, carrito):
    # Valida, busca, procesa y retorna resultado
```

#### 3. Strategy Pattern (Funcional)
Permite seleccionar algoritmo de búsqueda dinámicamente.

```python
estrategias_busqueda = {
    'nombre': buscar_por_nombre,
    'categoria': buscar_por_categoria
}
```

#### 4. Result Pattern
Validaciones sin excepciones usando tuplas.

```python
def validar_cantidad(cantidad):
    if cantidad < 1:
        return False, "Cantidad inválida"
    return True, ""
```

#### 5. Command Dispatcher Pattern
Mapea opciones del menú a funciones.

```python
def ejecutar_opcion(opcion, catalogo, carrito):
    if opcion == 1:
        ejecutar_ver_catalogo(catalogo)
    # ...
```

### Separación en Capas

```
┌─────────────────────────────────────┐
│   Presentation (ui.py)              │  ← Interfaz de usuario
├─────────────────────────────────────┤
│   Business Logic (business_logic)   │  ← Lógica de negocio
├─────────────────────────────────────┤
│   Validation (validators.py)        │  ← Validaciones
├─────────────────────────────────────┤
│   Data (data.py)                    │  ← Acceso a datos
└─────────────────────────────────────┘
```

## 💻 Características Técnicas

### Código Sin Clases (Funcional)

Todo el código usa funciones en lugar de clases:

```python
# ✅ Enfoque funcional
def crear_carrito_vacio():
    return []

def agregar_item_a_carrito(carrito, producto, cantidad):
    nuevo_carrito = carrito.copy()
    # ...
    return nuevo_carrito
```

### Sin Excepciones

Todas las validaciones retornan tuplas con resultado:

```python
# ✅ Sin try-except
es_valido, mensaje = validar_cantidad(5)
if not es_valido:
    print(mensaje)
```

### Type Hints Completos

```python
from typing import List, Dict, Any, Tuple

def buscar_producto(
    catalogo: List[Dict[str, Any]],
    producto_id: int
) -> Tuple[bool, str]:
    # ...
```

### Funciones Puras

Muchas funciones no tienen side effects:

```python
def calcular_total_carrito(carrito: List[Dict]) -> int:
    # No modifica el carrito, solo calcula
    return sum(item['subtotal'] for item in carrito)
```

### PEP 8 y Código Pythonic

- ✅ Variables en `snake_case`
- ✅ Constantes en `UPPER_CASE`
- ✅ Docstrings en todas las funciones
- ✅ List comprehensions donde es apropiado
- ✅ Funciones con una sola responsabilidad

## 📊 Catálogo de Productos

El sistema incluye 20 productos en 6 categorías:

### Tecnología (4 productos)
- Laptop HP Pavilion 15 - $599.990
- Mouse Inalámbrico Logitech - $15.990
- Teclado Mecánico RGB - $45.990
- Monitor 24 pulgadas Full HD - $129.990

### Ropa (4 productos)
- Polera Básica Algodón - $9.990
- Jeans Slim Fit - $29.990
- Chaqueta Impermeable - $49.990
- Zapatillas Deportivas - $39.990

### Hogar (3 productos)
- Lámpara LED Escritorio - $19.990
- Set de Sartenes Antiadherentes - $39.990
- Almohada Memory Foam - $24.990

### Deportes (3 productos)
- Pelota de Fútbol Profesional - $24.990
- Botella Térmica 1L - $12.990
- Pesas Mancuernas 5kg (Par) - $19.990

### Libros (3 productos)
- Python Crash Course - $34.990
- Clean Code (Robert Martin) - $39.990
- El Principito - $8.990

### Alimentos (3 productos)
- Café Colombiano Premium 500g - $7.990
- Aceite de Oliva Extra Virgen 1L - $12.990
- Miel Orgánica 500g - $9.990

## 🧪 Testing

Cada módulo incluye tests básicos que se ejecutan al correr el archivo directamente:

```bash
# Test de config
python config.py

# Test de data
python data.py

# Test de validators
python validators.py

# Test de utils
python utils.py

# Test de business_logic
python business_logic.py

# Test de ui
python ui.py
```

## 🎓 Conceptos Aplicados

### Principios SOLID (Adaptados a Funcional)

- **S**ingle Responsibility: Cada función hace una cosa
- **O**pen/Closed: Extensible mediante estrategias
- **D**ependency Inversion: Funciones dependen de abstracciones

### Zen of Python

```python
import this
```

Principios aplicados:
- ✅ Beautiful is better than ugly
- ✅ Explicit is better than implicit
- ✅ Simple is better than complex
- ✅ Flat is better than nested
- ✅ Readability counts

## 📝 Notas Importantes

### Formato de Precios

Los precios están en **pesos chilenos (CLP)** como números enteros:

```python
precio = 599990  # $599.990 (sin decimales)
```

### Validaciones

Todas las validaciones retornan tuplas sin usar excepciones:

```python
(es_valido: bool, mensaje_error: str)
```

### Inmutabilidad

Las funciones que modifican datos retornan nuevas estructuras:

```python
nuevo_carrito = agregar_item_a_carrito(carrito, producto, cantidad)
# carrito original no se modifica
```

## 🚀 Posibles Extensiones

Funcionalidades que se podrían agregar:

- [ ] Persistencia en archivo (guardar/cargar carrito)
- [ ] Sistema de usuarios
- [ ] Historial de compras
- [ ] Más criterios de búsqueda (precio, rango)
- [ ] Ordenamiento de productos
- [ ] Límite de stock por producto
- [ ] Cupones de descuento
- [ ] Múltiples métodos de pago

## 👨‍💻 Autor

**Gulliver**  
Proyecto desarrollado como parte de la capacitación en desarrollo de software con Python.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**¡Gracias por usar E-commerce Python!** 🛒✨