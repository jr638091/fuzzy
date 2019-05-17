# Informe de lógica difusa

## Datos del estudiante

​	Nombre: Juan Jose Roque Cires

​	Grupo: C-411

## Caracteristicas del Sistema de logica difusa

​	El ususario dispone de funciones de membresia triangulares (**trimf**), trapezoidales (**trapmf**), segnozoidales (**segmf**), camana de Gauss (**gaussmf**) y campana genérica (**gbell**). La librería ofrece como funciones de agregación Takagi-Sugeno-Kang (**TSK**) y Tsukamoto (**Tsuka**). La variable de post-condición para todas las reglas son la misma. Como métodos de desfuzzy contamos con centroide (**centroide**), bisectriz (**bis**) y las variantes de Máximo (**MoM**, **GoM**, **LoM**).

## Principales ideas seguidas para la implementacion

​	Se uso como lenguaje Python 3, por la expresividad que se alcanza con dicho lenguaje.

### Experiencia de usuario

​	El módulo tiene la clase FuzzyModel que es el modelo de lógica difusa. Cuando de instancia se define que método de agregación y  de defuzzy se utilizaran para resolver el problema.

```python
from fuzzpy import *

model = FuzzyModel()# por defecto del metodo de agregacion es TSK y sin desfuzzy
```

 	

​	En la biblioteca en la clase Membership las funciones de membresía.

```python
Membership.trapmf(10, 15, 30, 30, 0, 30)
Membership.trimf(1, 2, 3, 0, 5)
```

​	

​	Pra crear las variables se usa el método add_var que recive la variable lingüística, los valores lingüísticos y las funciones de membresía de cada valor.

```python
model.add_var(
    'tamaño',
    ['larga', 'normal', 'corta'],
    [
        Membership.trapmf(10, 15, 30, 30, 0, 30),
        Membership.trapmf(8, 9, 11, 12, 0, 30),
        Membership.trapmf(0, 0, 7, 10, 0, 30)
        ]
    )
model.add_var(
    'velocidad',
    ['lenta', 'normal', 'rapida'],
    [
        Membership.trapmf(0, 0, 3, 5, 0, 5),
        Membership.trimf(1, 2, 3, 0, 5),
        Membership.trapmf(2, 3, 5, 5, 0, 5)
    ]
)
model.add_var(
    'bronca',
    ['alta', 'normal', 'baja'],
    [
        Membership.trapmf(50, 60, 100, 100, 0, 100),
        Membership.trimf(40, 50, 60, 0, 100),
        Membership.trapmf(0, 0, 50, 40, 0, 100)
    ]
)
```

​	

​	Para un mejor interpretación del usuario se definen las reglas se usa el metodo add_rule que recive la precondicion y pos-condición, la precondición siempre es un string y la pos-condición puede ser una función como en el caso del metodo TSK o un string para el metodo Tsukamoto.	

``` python
# Gramatica de precondiciones
# Inicio => Atomo | Atomo Cond
# Cond => Operacion Atomo Cond | epsilon
# Atomo => var ' is ' valor | 'not ' var ' is ' valor
# Operacion => 'and' | 'or'
model.add_rule('tenderos is lenta', lambda x: 100)
model.add_rule('cola is larga', lambda x: 100)
model.add_rule('cola is normal and tenderos is normal', lambda x, y: x*y)
# model.add_rule('tenderos is lenta', 'bronca is alta')
# model.add_rule('cola is larga', 'bronca is alta')
# model.add_rule('cola is normal and tenderos is normal', 'bronca is alta')
```

 

​	Para definir la entrada del modelo se usa el método add_input que recive el nombre de la variable, el tipo y el valor, con este metodo ya se hace fuzzy a las variables.

```python
model.add_input('cola', 'tamaño', 19)
model.add_input('tenderos', 'velocidad', 2)
```



   Para resolver el problema ya definido solo queda utilizar solve que no recive nada.

```python
model.solve()
```

### Detalles técnicos

​	Las funciones de pertenencia son clases que en el método __\_\_init\_\___ recibe los parámetros de la función y en el __\_\_call\_\___ evalúo de esta manera actua como una función.

​	A la hora de parsear y evaluar las pre-condiciones realizo split por los espacios y mientras itero por el array de la precondición voy determinando los valores de las variables.

Para calcular las integrales de las funciones continuas lo que se hizo fue discretizar las funciones y proceder con una sumatoria.



## Problema propuesto

​	Todo Cuba sabe que las colas son un problema, sobre todo si es para comprar el pollo. Viendo que con la situación del pollo se han dado casos de colas que terminan en bronca tumultuaria, propongo a partir de la cantidad de personas que hay en la cola, y la velocidad que entran las personas (cantidad de personas que entran promedio a la vez) , determinar cuan posible es que termine bronca.



## Consideraciones

​	Me percate que cada el Centroide y bisectriz en muchas ocaciones relativamente cercanos, y que las distintas alternativas de máximos se debe ser escogido cuidadozamente.