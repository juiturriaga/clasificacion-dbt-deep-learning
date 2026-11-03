# Validación conceptual con MNIST

Esta carpeta contiene implementaciones **desde cero** de tres modelos de clasificación binaria para distinguir los dígitos **3 y 8** del conjunto MNIST. Esta etapa se realizó como validación conceptual previa a los experimentos con imágenes DBT; no debe confundirse con el entrenamiento de los modelos empleados sobre BCS-DBT.

## Archivos

| Archivo | Contenido |
|---|---|
| `preparar_datos.py` | Funciones compartidas para obtener y preparar MNIST y calcular métricas. |
| `perceptron_simple.ipynb` | Perceptrón simple. |
| `perceptron_multicapa.ipynb` | Perceptrón multicapa (MLP). |
| `cnn_desde_cero.ipynb` | Red neuronal convolucional (CNN). |

## Ejecución

1. Colocar `preparar_datos.py` en el mismo directorio de trabajo que los notebooks o añadir su ubicación al entorno de Python.
2. Abrir uno de los notebooks y ejecutar sus celdas en orden.
3. Permitir la descarga de MNIST si el conjunto aún no está disponible en el entorno.

Los notebooks comparten funciones de preparación de datos para mantener criterios de evaluación comparables. El perceptrón simple emplea etiquetas `-1` y `1` en su implementación; los otros modelos pueden utilizar una codificación distinta según el procedimiento definido en cada notebook.

## Alcance

El objetivo es comparar implementaciones fundamentales sobre un problema binario sencillo. Estos resultados no representan el rendimiento de los modelos sobre imágenes de tomosíntesis digital de mama.
