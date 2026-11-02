# Modelos de clasificación de imágenes DBT

Esta carpeta contiene los notebooks utilizados para el entrenamiento y la evaluación de modelos de aprendizaje profundo y algoritmos clásicos de aprendizaje automático aplicados a la clasificación binaria de imágenes de tomosíntesis digital de mama (DBT).

El trabajo utiliza el conjunto de datos BCS-DBT, disponible en The Cancer Imaging Archive (TCIA).

Se consideran dos clases:

- **Clase negativa (0):** imágenes correspondientes a estudios sin hallazgos anormales (*Normal*).
- **Clase positiva (1):** imágenes correspondientes a las categorías *Actionable*, *Benign* y *Cancer*.

## 1. Modelos de aprendizaje profundo

Se implementaron las arquitecturas DenseNet121 y DenseNet201 mediante aprendizaje por transferencia, utilizando pesos preentrenados en ImageNet y ajuste fino parcial (*fine-tuning*).

Para cada arquitectura se evaluaron dos configuraciones, descongelando las últimas 100 o 200 capas de la base convolucional.

Los ocho notebooks disponibles corresponden a las siguientes configuraciones:

| Arquitectura | Capas descongeladas | Balanceado | Desbalanceado |
|---|---:|---|---|
| DenseNet121 | 100 | `densenet121_100capas_bal.ipynb` | `densenet121_100capas_desbal.ipynb` |
| DenseNet121 | 200 | `densenet121_200capas_bal.ipynb` | `densenet121_200capas_desbal.ipynb` |
| DenseNet201 | 100 | `densenet201_100capas_bal.ipynb` | `densenet201_100capas_desbal.ipynb` |
| DenseNet201 | 200 | `densenet201_200_capas_bal.ipynb` | `densenet201_200capas_desbal.ipynb` |

Las imágenes de entrada tienen dimensiones de 512 × 512 píxeles y se replican en tres canales para adaptarse a las arquitecturas utilizadas.

## 2. Algoritmos clásicos de aprendizaje automático

Se evaluaron tres algoritmos:

- **K-Nearest Neighbors (KNN):** clasificación utilizando un vecino (`k=1`).
- **Gaussian Naive Bayes:** clasificador probabilístico basado en una distribución gaussiana de las características.
- **Support Vector Machine (SVM):** clasificador con núcleo polinómico de grado 2 y parámetro `C=1`.

Para estos modelos se utilizan imágenes redimensionadas a 224 × 224 píxeles, posteriormente convertidas en vectores de 50.176 características.

Cada algoritmo se evalúa en los escenarios balanceado y desbalanceado.

## 3. Escenarios experimentales

Se emplearon dos distribuciones de clases:

| Escenario | Entrenamiento | Validación | Prueba |
|---|---:|---:|---:|
| Balanceado | 3197 | 400 | 400 |
| Desbalanceado (aprox. 3:1) | 2904 | 334 | 334 |

Las particiones se realizaron por paciente, evitando que imágenes de un mismo paciente se distribuyeran entre entrenamiento, validación y prueba.

## 4. Datos necesarios y ejecución

Los notebooks utilizan archivos NumPy (`.npy`) con las imágenes previamente procesadas y sus etiquetas binarias.

Para ejecutarlos:

1. Descargar y preparar el conjunto BCS-DBT siguiendo los procedimientos documentados en `preprocesamiento/`.
2. Disponer de los archivos `.npy` correspondientes al escenario experimental.
3. Configurar la variable `DATA_DIR` de cada notebook para indicar la ubicación de los datos.
4. Verificar que los nombres de los archivos coincidan con los utilizados en las instrucciones de carga.
5. Ejecutar las celdas en orden, contando con las dependencias de Python correspondientes.

Los datos de entrada no se incluyen en este repositorio debido a su tamaño.

**Importante:** los archivos `.npy` generados mediante el preprocesamiento documentado pueden tener nombres y selecciones de imágenes diferentes de los utilizados en los entrenamientos originales. Por lo tanto, puede ser necesario adaptar la carga de archivos y no se garantiza obtener las mismas métricas.

## 5. Evaluación de los modelos

Los notebooks contienen los procedimientos para calcular métricas de clasificación, entre ellas:

- Exactitud (*accuracy*).
- Sensibilidad (*recall*).
- Especificidad.
- Precisión (*precision*).
- Puntuación F1.
- Área bajo la curva ROC (AUC).

También incluyen las matrices de confusión y las visualizaciones correspondientes, según el modelo.

## 6. Reproducibilidad

Los resultados y las gráficas conservados en los notebooks corresponden a las ejecuciones experimentales originales del proyecto.

La reproducción exacta de estos resultados requiere utilizar los mismos conjuntos de imágenes, particiones, configuraciones y condiciones de entrenamiento.

El código de preprocesamiento disponible en el repositorio documenta una reconstrucción del procedimiento metodológico, por lo que su ejecución puede producir conjuntos de imágenes diferentes de los originales.

Los notebooks se publican con sus salidas guardadas para permitir la consulta del procedimiento y de los resultados obtenidos, sin necesidad de repetir los entrenamientos.
