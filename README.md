# Clasificación binaria de imágenes de tomosíntesis digital de mama mediante aprendizaje automático

Repositorio de código asociado a un Proyecto Final de Titulación de Ingeniería Biomédica de la Universidad Tecnológica (UTEC), Uruguay.

El proyecto estudia la clasificación binaria de imágenes de tomosíntesis digital de mama (DBT) del conjunto público **BCS-DBT**, disponible en [The Cancer Imaging Archive (TCIA)](https://www.cancerimagingarchive.net/), mediante modelos de aprendizaje profundo y algoritmos clásicos de aprendizaje automático.

## Organización del repositorio

| Carpeta | Contenido |
|---|---|
| [`MNIST/`](MNIST/) | Validación conceptual con implementaciones desde cero de perceptrón simple, perceptrón multicapa y CNN sobre los dígitos 3 y 8. |
| [`preprocesamiento/`](preprocesamiento/) | Notebooks de selección y partición por paciente, descarga de series DICOM, extracción de cortes, preparación de matrices NumPy y análisis complementario mediante FID y entropía de Shannon. |
| [`modelos/`](modelos/) | Notebooks de entrenamiento y evaluación de DenseNet121, DenseNet201, KNN, Gaussian Naive Bayes y SVM. |

Cada carpeta contiene un README con indicaciones específicas.

## Diseño experimental

Las imágenes de DBT se agruparon en dos clases: **negativa (0)**, correspondiente a *Normal*, y **positiva (1)**, que agrupa *Actionable*, *Benign* y *Cancer*. Se trabajó con un escenario balanceado y otro desbalanceado (aproximadamente 3:1, clase negativa:positiva). Las particiones experimentales se definieron por paciente para evitar su presencia simultánea en entrenamiento, validación y prueba.

| Escenario | Entrenamiento | Validación | Prueba |
|---|---:|---:|---:|
| Balanceado | 3197 | 400 | 400 |
| Desbalanceado | 2904 | 334 | 334 |

Se evaluaron DenseNet121 y DenseNet201 con aprendizaje por transferencia y ajuste fino de las últimas 100 o 200 capas, además de KNN (`k=1`), Gaussian Naive Bayes y SVM con núcleo polinómico de grado 2.

Como análisis complementario de los conjuntos de entrenamiento, se utilizó
la distancia de Fréchet Inception (FID) para comparar las distribuciones
de características de las imágenes de la clase positiva de ambos escenarios,
y la entropía de Shannon para caracterizar la distribución de intensidades
de las imágenes.

## Cómo consultar y utilizar el código

1. Para la **validación conceptual**, comenzar por [`MNIST/README.md`](MNIST/README.md).
2. Para reconstruir el **flujo de preparación de DBT**, seguir [`preprocesamiento/README.md`](preprocesamiento/README.md).
3. Para revisar los **entrenamientos y resultados de clasificación**, consultar [`modelos/README.md`](modelos/README.md).

Los notebooks fueron desarrollados para ejecutarse con Python, principalmente en Google Colab. El conjunto de imágenes y los archivos NumPy de gran tamaño no se distribuyen en este repositorio. Antes de ejecutar los notebooks de modelos, es necesario disponer de los datos esperados y configurar las rutas de acceso; el nombre y la estructura de los archivos varían entre algunas implementaciones.

## Alcance y reproducibilidad

Este repositorio documenta el procedimiento de trabajo y conserva notebooks de los experimentos realizados. Los resultados guardados en los notebooks corresponden a las ejecuciones del proyecto; su presencia **no equivale a haber verificado nuevamente una ejecución integral del repositorio**.

Los notebooks publicados de selección y preprocesamiento constituyen una reconstrucción del flujo metodológico y **no garantizan recuperar las mismas series e imágenes** de los experimentos originales. En consecuencia, ejecutar el flujo publicado puede dar lugar a conjuntos distintos y no garantiza obtener las mismas métricas. Véanse las limitaciones particulares en [`preprocesamiento/README.md`](preprocesamiento/README.md) y [`modelos/README.md`](modelos/README.md).

Este código está destinado a documentación académica e investigación; no constituye un sistema validado para uso clínico.
