# Selection Sort

Selection Sort (ordenación por selección) es un algoritmo de ordenación que divide el array en una parte ordenada y otra desordenada. En cada paso, busca el elemento más pequeño de la parte desordenada y lo coloca al final de la parte ordenada.

## Idea

Mantiene una parte ordenada a la izquierda que crece de uno en uno. En cada paso, busca el elemento más pequeño de la parte desordenada y lo intercambia con el primer elemento de esa parte. Se repite hasta el final.

## Complejidad en el mejor caso

O(n²) → aunque los elementos ya estén ordenados, siempre hay que recorrer la parte desordenada para buscar el elemento más pequeño.

## Complejidad en el peor caso

O(n²) → hay que recorrer la parte desordenada en cada paso para encontrar el elemento más pequeño.

## Complejidad en el caso promedio

O(n²) → normalmente se realizan aproximadamente el mismo número de comparaciones que en el peor caso.

## ¿Es adecuado para Big Data?

No, generalmente no. Su complejidad en todos los casos es O(n²), por lo que el tiempo de ejecución crece mucho cuando aumenta el número de elementos. Para grandes volúmenes de datos suelen utilizarse algoritmos más eficientes, como Merge Sort u otros métodos adaptados al procesamiento distribuido.

## Recursos

**Vídeo:**  
https://youtu.be/92BfuxHn2XE?si=ExfscaH2d1IPqXHP
