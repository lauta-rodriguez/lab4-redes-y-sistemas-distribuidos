# Análisis de enrutamiento en redes de topología de anillo

# Grupo 29

## Integrantes:

- Lara Kurtz, lara.kurtz@mi.unc.edu.ar
- Lautaro Rodríguez, lautaro.rodriguez@mi.unc.edu.ar

# Abstract

Este informe analiza el comportamiento del tráfico de red en una topología de anillo utilizando diferentes algoritmos de enrutamiento. El objetivo es comparar el rendimiento de estos algoritmos en términos del `retardo` de los paquetes. Para lograrlo, se implementaron dos algoritmos: uno **inicial** proporcionado por la cátedra y otro **modificado** llamado "Hop count modificado".

# Introducción

La red sobre la que se va a trabajar es una red con una topología en forma de anillo compuesta por 8 nodos numerados del 0 al 7.

![topologia](/images/General_Network.png)

Cada nodo posee dos interfaces de comunicación full-duplex, una para establecer conexión con el nodo de la izquierda y otra para comunicarse con el nodo de la derecha.

![node](/images/Node.png)

El algoritmo proporcionado por la cátedra para el enrutamiento de paquetes solo los envía en una dirección, siguiendo el sentido de las agujas del reloj (a través de la Interfaz `0`). Esto implica que no se aprovecha la otra interfaz de comunicación disponible.

Esta limitación conlleva un `retardo` en la entrega de los paquetes:

- Si el nodo de destino se encuentra a la izquierda del nodo emisor, el paquete debe realizar una vuelta completa a la red antes de llegar a su destino.

- Dado que todos los paquetes se envían en el mismo sentido, se crea un cuello de botella en los nodos ubicados a la derecha del nodo emisor, ya que todos los paquetes deben pasar por ellos. Este problema se acentúa cuando múltiples nodos envían paquetes al mismo tiempo.

# Algoritmo de enrutamiento modificado

Se presenta un nuevo algoritmo que tiene como objetivo principal disminuir el retardo de los paquetes. Este algoritmo permite enviar los paquetes en ambos sentidos, aprovechando las dos interfaces de comunicación disponibles en cada nodo.

El nuevo algoritmo utiliza el método de contar saltos (hop count) para determinar la interfaz por la cual enviar cada paquete. Se busca seleccionar la interfaz que requiera la menor cantidad de saltos para llegar al nodo destino, con el fin de reducir el retardo en la entrega de los paquetes.

Además, este algoritmo busca mitigar el problema del cuello de botella que se genera en los nodos ubicados a la derecha del nodo emisor. Al distribuir de manera más equitativa la carga de tráfico, se logra una mejor utilización de los recursos de la red.

### Suposiciones:

- Se asume que la red de topología de anillo es simétrica.

- Se considera que la topología de la red es estática, lo que implica que no hay cambios en la conexión entre los nodos durante el funcionamiento del algoritmo.

### Algoritmo

El algoritmo de enrutamiento modificado sigue los siguientes pasos:

1. Al iniciar la simulación, cada nodo envía un paquete de reconocimiento denominado `Hello` a través de la interfaz `REC_LNK`, definida como `0`. El paquete circula en sentido horario y se incrementa un contador de saltos dentro del mismo en cada salto. El objetivo es que el paquete complete una vuelta al anillo y regrese al nodo de origen.

2. Cuando el paquete `Hello` llega al nodo destino establecido en el archivo de configuración `omnetpp.ini`, se registra el número de saltos realizados hasta ese momento en un campo especial dentro del paquete. Luego, el paquete continúa su trayectoria en la misma dirección que venía.

3. Al regresar el paquete `Hello` al nodo emisor, este utiliza la información contenida en el paquete para determinar la interfaz óptima para enviar paquetes al destino, y luego lo descarta. Se selecciona la interfaz que requiera la menor cantidad de saltos para alcanzar el nodo destino. Para tomar la decisión, se considera lo siguiente dado que la topología de anillo simétrica:

   - Si se necesitó saltar menos de la mitad de los nodos de la red para llegar al destino desde la interfaz `REC_LNK`, se elige esa interfaz como óptima (`REC_LNK`).
   - Si se necesitó saltar más de la mitad de los nodos (o igual a la mitad), se selecciona la otra interfaz como óptima (`!REC_LNK`)

   Esta información se almacena en un booleano, ya que hay dos posibles interfaces.

# Análisis de las redes bajo los algoritmos de enrutamiento

Se utiliza una distribución exponencial con un parámetro variable y analizamos el comportamiento de la red para los siguientes valores: `0.3`, `0.6` y `1`, lo que significa que los eventos se producen en promedio cada `0.3`, `0.6` y `1` segundo. Esto afecta inversamente a la frecuencia con la que los paquetes son enviados desde la capa de aplicación, es decir, a una distribución exponencial más chica, obtenemos una inyección de paquetes en la red más alta.

Se plantean dos casos de estudio:

## Caso 1: Dos nodos envían paquetes al mismo nodo destino

Los nodos **0** y **2** envían paquetes al nodo **5**.

### Comparación de ocupación de búferes de las interfaces en ambos algoritmos

Para ambos algoritmos, se observa que la ocupación de los búferes disminuye a medida que aumenta el valor de `interArrivalTime`. Esto se debe a que los eventos ocurren más espaciados en el tiempo, lo que resulta en una menor inyección de paquetes en la red.

En general, en el algoritmo inicial, se observa que el nodo `0` presenta una ocupación de búfer significativamente mayor que los demás nodos. Esto se debe a que todos los paquetes viajan en sentido horario y el nodo `0` actúa como nodo intermedio para los paquetes enviados por el nodo `2`, además de gestionar sus propios paquetes.

Por otro lado, se puede notar que en todas las variaciones de `interArrivalTime`, el algoritmo modificado distribuye de manera más equitativa la carga de tráfico entre los nodos, evitando especialmente la sobrecarga del búfer del nodo `0`. Esto se evidencia en el hecho de que las curvas en los gráficos del algoritmo modificado son bastante similares y alcanzan valores más bajos en comparación con el algoritmo inicial.

![buffer_p1_s1](/plots/img/time-buffer-p1c1-0.png)
![buffer_p1_s1](/plots/img/time-buffer-p2c1-0.png)
![buffer_p1_s2](/plots/img/time-buffer-p1c1-1.png)
![buffer_p1_s2](/plots/img/time-buffer-p2c1-1.png)
![buffer_p1_s3](/plots/img/time-buffer-p1c1-2.png)
![buffer_p1_s3](/plots/img/time-buffer-p2c1-2.png)

Obtenemos los mejores resultados con `interArrivalTime=1`, ya que con menos paquetes en la red se logra que estos utilicen los búferes intermedios de manera más eficiente y no permanezcan allí durante mucho tiempo. Particularmente, se observa lo siguiente:

- **Algoritmo inicial**: El nodo 2 presenta una ocupación de búfer muy baja, ya que los paquetes se envían desde ese nodo pero no se reciben paquetes de ningún otro lugar. Por otro lado, el nodo 0 muestra una ocupación muy alta debido a la carga de sus propios paquetes y los del nodo 2.
- **Algoritmo modificado**: Tanto el nodo 0 como el nodo 2 mantienen su ocupación cerca de cero.

### Average Hop Count

En cuanto a la cantidad de saltos que realiza un paquete para llegar a destino, logramos una reducción considerable, ya que en el agoritmo modificado se elige el camino más corto. Esto evita la necesidad de realizar un recorrido casi completo del anillo en casos donde los nodos de destino están cercanos entre sí.  
De esta manera, se logra minimizar la cantidad de saltos necesarios para entregar los paquetes.

| interArrivalTime | Algoritmo inicial | Algoritmo modificado |
| ---------------- | ----------------- | -------------------- |
| 0,3              | 3.44              | 3                    |
| 0,6              | 3.73              | 3                    |
| 1,0              | 3.91              | 3                    |

### Comparación del delay de los paquetes en ambos algoritmos

El algoritmo modificado reduce significativamente el **delay** de los paquetes en comparación con el algoritmo inicial. Esto se debe a dos factores:

- Reducción de la distancia recorrida por los paquetes: El algoritmo modificado disminuye la cantidad de saltos que los paquetes deben realizar para llegar a su destino.

- Distribución equitativa de la carga de tráfico: El nuevo algoritmo distribuye de manera más equitativa la carga de tráfico entre las interfaces de comunicación de los nodos. Esto evita la congestión y el cuello de botella que se producían en los nodos ubicados a la derecha del nodo emisor en el algoritmo inicial.

![delay_p1](/plots/img/time-delay-p1c1-2.png)
![delay_p2](/plots/img/time-delay-p2c1-2.png)

Incluso habiendo mejorado las métricas de retardo, notamos que a medida que avanza el tiempo de la simulación y aumenta la ocupación de los búferes, también se observa un incremento en el retardo. Esto se debe a que los paquetes no pueden ser reenviados tan rápidamente, ya que deben esperar a que los paquetes que estaban en los búferes al momento de su llegada sean liberados. Sin embargo, este efecto no se aprecia en el escenario con `interArrivalTime = 1`, donde la ocupación de los búferes se mantiene considerablemente más baja y constante.

### Average Delay

| interArrivalTime | Algoritmo inicial | Algoritmo modificado |
| ---------------- | ----------------- | -------------------- |
| 0,3              | 82                | 71.08                |
| 0,6              | 69.19             | 41.07                |
| 1,0              | 51.15             | 6.90                 |

## Caso 2: Todos los nodos envían paquetes al mismo nodo destino

Los nodos **0**, **1**, **2**, **3**, **4**, **5**, **6** y **7** envían paquetes al nodo **5**.

### Comparación de ocupación de búferes de las interfaces en ambos algoritmos

No observamos cambios significativos en cuanto a la ocupación de búferes para este caso de estudio, creemos que esto se debe a que al haber tantos paquetes en circulación, los búferes se llenan demasiado rápido y repartir la carga entre los demás nodos no llega a producir una diferencia significativa. Lo que sí podemos observar en las gráficas es que la carga de los búferes se reparte de manera más equitativa, lo que se evidencia en que las curvas para el algoritmo modificado suelen mantenerse más cercanas entre sí.

![buffer_p1_s1](/plots/img/time-buffer-p1c2-0.png)
![buffer_p1_s1](/plots/img/time-buffer-p2c2-0.png)
![buffer_p1_s2](/plots/img/time-buffer-p1c2-1.png)
![buffer_p1_s2](/plots/img/time-buffer-p2c2-1.png)
![buffer_p1_s3](/plots/img/time-buffer-p1c2-2.png)
![buffer_p1_s3](/plots/img/time-buffer-p2c2-2.png)

### Average Hop Count

| interArrivalTime | Algoritmo inicial | Algoritmo modificado |
| ---------------- | ----------------- | -------------------- |
| 0,3              | 1.33              | 1.31                 |
| 0,6              | 1.65              | 1.57                 |
| 1,0              | 2.06              | 1.84                 |

### Comparación del delay de los paquetes en ambos algoritmos

No observamos cambios significativos en cuanto al delay para este caso de estudio. Dado que en ambos casos de estudio vemos una fuerte relación entre el delay y la ocupación de los búferes, creemos que esto tiene que ver con la gran cantidad de paquetes que se encuentran en la red.

Sin embargo, parece haber una ligera mejora en el caso de `interArrivalTime = 1` (curva azul en ambos gráficos). Parece ser que los picos de esta curva no llegan tan alto como lo hacen en el caso del algoritmo inicial, esto lo podemos observar mejor si comparamos la curva azul con la curva verde en ambos gráficos, la cual se mantiene bastante parecida.

![delay_p1](/plots/img/time-delay-p1c2-2.png)
![delay_p2](/plots/img/time-delay-p2c2-2.png)

### Average Delay

| interArrivalTime | Algoritmo inicial | Algoritmo modificado |
| ---------------- | ----------------- | -------------------- |
| 0,3              | 79.31             | 80.25                |
| 0,6              | 70.83             | 71.51                |
| 1,0              | 64.53             | 63.66                |

# Conclusiones

En el primer caso de estudio, donde solo dos nodos envían paquetes al mismo destino, se observa que el algoritmo modificado logra reducir tanto el retardo como la cantidad promedio de saltos necesarios para entregar los paquetes. Esto se debe a la distribución equitativa de la carga de tráfico entre las interfaces de comunicación de los nodos.

En el segundo caso de estudio, donde todos los nodos envían paquetes al mismo destino, el algoritmo modificado también consigue una ligera disminución en el retardo promedio de los paquetes y la cantidad promedio de saltos en comparación con el algoritmo inicial, aunque no de manera significativa. Esto podría atribuirse al hecho de que muchos paquetes se envían al mismo nodo, por lo que varios nodos deben actuar como intermediarios y a la vez que deben gestionar el envío de sus propios paquetes.

Es importante destacar que el algoritmo modificado puede ser mejorado. En lugar de hardcodear la ruta de los paquetes en la etapa de inundación, se podría implementar un análisis periódico del estado de la red para enrutar los paquetes en función de los cambios en la topología y ocupación de búferes. Esto permitiría adaptar el enrutamiento de manera dinámica y optimizar aún más el rendimiento de la red.
