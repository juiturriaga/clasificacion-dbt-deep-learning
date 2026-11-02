# Preprocesamiento de imágenes DBT

Esta carpeta contiene los procedimientos de selección, partición, extracción y preprocesamiento de imágenes de tomosíntesis digital de mama (DBT), utilizados como referencia para el Proyecto Final de Titulación de Ingeniería Biomédica.

Se utiliza el conjunto público **BCS-DBT**, disponible en The Cancer Imaging Archive (TCIA).

## Notebooks

**`01_seleccion_y_particion.ipynb`**

Realiza la selección de series y la partición de los datos por paciente, evitando que un mismo paciente aparezca en distintos conjuntos. Construye los escenarios balanceado y desbalanceado y genera seis archivos CSV con las series seleccionadas y las posiciones de los cortes previstos.

**`02_extraccion_y_preprocesamiento.ipynb`**

Utiliza los CSV generados por el primer notebook para implementar:

- Descarga de series DICOM desde TCIA.
- Extracción de los cortes seleccionados de cada volumen.
- Conversión de las imágenes a `float32`.
- Normalización de las intensidades por su valor máximo.
- Redimensionamiento a 512 × 512 píxeles.
- Almacenamiento de imágenes y etiquetas en formato `.npy`.

## Datos necesarios

Para ejecutar el primer notebook se requieren los archivos de metadatos de BCS-DBT:

- `BCS-DBT-file-paths-train-v2`
- `BCS-DBT-labels-train-v2`

El segundo notebook requiere los seis CSV generados por el primero y acceso a las series DICOM correspondientes. La descarga necesita disponer del identificador `SeriesInstanceUID` de cada serie.

## Ejecución

Los notebooks están preparados para utilizarse en Google Colab y deben ejecutarse en orden.

El segundo notebook tiene la descarga desactivada por defecto mediante `EJECUTAR_DESCARGA = False`. Para procesar imágenes es necesario habilitarla explícitamente.

También incluye un modo de prueba para procesar una única serie antes de ejecutar conjuntos completos.

## Reproducibilidad y limitaciones

El primer notebook reconstruye el procedimiento de selección y partición, por lo que las series elegidas pueden diferir de las utilizadas en los experimentos originales.

El segundo notebook proporciona la implementación de descarga y preprocesamiento, pero no se ha verificado mediante la ejecución completa de los conjuntos experimentales.

La extracción implementada presupone volúmenes DICOM multiframe. Otras organizaciones de archivos pueden requerir adaptaciones.

Las cantidades de imágenes indicadas en la metodología corresponden a las distribuciones planificadas y no deben interpretarse como evidencia de que todas las descargas y extracciones se hayan completado.
