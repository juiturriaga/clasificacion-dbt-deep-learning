
# Selección, preprocesamiento y análisis de imágenes DBT

Esta carpeta contiene tres notebooks que documentan los procedimientos de selección de series, división de datos por paciente, preparación de imágenes y análisis complementario de los conjuntos de tomosíntesis digital de mama (DBT) del conjunto **BCS-DBT**, disponible en The Cancer Imaging Archive (TCIA).

## Notebooks

### 1. Selección y partición de los datos

**`01_seleccion_y_particion.ipynb`**

Utiliza los metadatos del conjunto BCS-DBT para seleccionar series y generar los escenarios balanceado (1:1) y desbalanceado (3:1).

El notebook comprueba que no haya pacientes compartidos entre las particiones de entrenamiento, validación y prueba. Como resultado, genera seis archivos CSV con las series y los cortes seleccionados, que se guardan en la carpeta `selecciones_generadas/` del entorno de ejecución.

### 2. Extracción y preprocesamiento de imágenes

**`02_extraccion_y_preprocesamiento.ipynb`**

Utiliza los seis archivos CSV generados en la etapa anterior para recuperar las series DICOM correspondientes desde TCIA y extraer los cortes seleccionados.

Las imágenes se convierten a `float32`, se normalizan dividiendo sus intensidades por el valor máximo y se redimensionan a 512 × 512 píxeles. Posteriormente, las imágenes y sus etiquetas se almacenan en archivos `.npy`.

### 3. Análisis de FID y entropía de Shannon

**`Analisis_FID_Shannon.ipynb`**

Contiene los procedimientos empleados para comparar y caracterizar los conjuntos de entrenamiento balanceado (1:1) y desbalanceado (3:1).

Se realizaron los siguientes análisis:

- **Distancia de Fréchet Inception (FID):** comparación de las distribuciones de características de las imágenes de la clase positiva de ambos conjuntos, utilizando características extraídas de la capa intermedia `mixed6` de InceptionV3.
- **Entropía de Shannon:** cálculo de la entropía de las imágenes y comparación de sus valores medios y desviaciones estándar entre ambos conjuntos.
- **Verificaciones adicionales:** comprobación de las cantidades de imágenes por clase y cálculo de una FID de control entre las clases negativa y positiva.

Este análisis se utilizó como una etapa complementaria de caracterización de los datos y no forma parte del entrenamiento de los modelos de clasificación.

## Datos de entrada

### Selección y partición

Para ejecutar `01_seleccion_y_particion.ipynb` se necesitan los metadatos originales de BCS-DBT:

- `BCS-DBT-file-paths-train-v2*.xlsx`
- `BCS-DBT-labels-train-v2*.csv`

### Extracción y preprocesamiento

El notebook `02_extraccion_y_preprocesamiento.ipynb` requiere los seis archivos CSV generados por el primer notebook y acceso a TCIA para recuperar las series DICOM identificadas por `SeriesInstanceUID`.

### Análisis de FID y Shannon

El notebook `Analisis_FID_Shannon.ipynb` utiliza los siguientes archivos:

- `X_train_3a1.npy`
- `X_train_1a1.npy`
- `y_train_3a1.npy`
- `y_train_1a1.npy`

Estos archivos corresponden a los conjuntos de entrenamiento procesados y deben estar disponibles en las rutas configuradas dentro del notebook.

Las rutas utilizadas corresponden al entorno original de Google Drive y deben adaptarse para ejecutar el análisis en otro entorno.

## Orden de ejecución

1. Abrir `01_seleccion_y_particion.ipynb` en Google Colab y proporcionar los dos archivos de metadatos.
2. Ejecutar sus celdas y localizar los seis CSV generados en `selecciones_generadas/`.
3. Colocar los seis CSV en el directorio desde el cual se ejecutará `02_extraccion_y_preprocesamiento.ipynb` (o cargarlos cuando el notebook lo solicite).
4. En el segundo notebook, revisar las opciones de ejecución. Por defecto, `EJECUTAR_DESCARGA = False` (no descarga), `MODO_PRUEBA = True` (una serie al habilitar la descarga) y `TODOS_LOS_CONJUNTOS = False` (un conjunto elegido).
5. Habilitar explícitamente la descarga solo cuando se disponga de espacio, conexión y datos adecuados. El modo de prueba permite comprobar una serie, pero no verifica el procesamiento integral.
6. Para realizar el análisis complementario, abrir `Analisis_FID_Shannon.ipynb`, disponer de los archivos `.npy` correspondientes a ambos escenarios de entrenamiento y adaptar las rutas de Google Drive antes de ejecutar sus celdas.

## Limitaciones y reproducibilidad

- La selección de series incluida reconstruye el procedimiento y puede diferir de las series utilizadas en los experimentos originales.
- El procesamiento completo de los conjuntos mediante el flujo de selección y descarga publicado no se ha verificado.
- La extracción implementada supone volúmenes DICOM multiframe; otras organizaciones de archivos pueden requerir adaptaciones.
- Las distribuciones objetivo comprueban la selección planificada, pero no demuestran que todas las imágenes hayan sido descargadas y procesadas.
- Los archivos resultantes pueden requerir ajustes de nombre y ubicación para ser utilizados por los notebooks de [`../modelos/`](../modelos/).
- El notebook de FID y entropía de Shannon conserva los procedimientos y resultados del análisis original. Su ejecución requiere disponer de los archivos de entrada correspondientes y configurar las rutas utilizadas.
- La FID se calculó a partir de características de una capa intermedia de InceptionV3, por lo que sus valores no deben interpretarse como directamente equivalentes a los obtenidos mediante la implementación convencional basada en la capa final de características.

Los archivos de imagen y los conjuntos de datos procesados no se incluyen en el repositorio debido a su tamaño. La descarga y utilización de los datos originales requieren respetar las condiciones de uso y atribución del conjunto BCS-DBT.
