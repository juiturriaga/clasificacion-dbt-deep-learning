# Preprocesamiento de imágenes DBT

## Descripción

Esta carpeta contiene los procedimientos de selección, partición y preparación de los datos correspondientes al conjunto *Breast Cancer Screening Digital Breast Tomosynthesis* (BCS-DBT), utilizado en el Proyecto Final de Titulación de Ingeniería Biomédica.

El notebook `01_seleccion_y_particion.ipynb` presenta una reconstrucción reproducible del procedimiento metodológico empleado para organizar los conjuntos experimentales balanceado y desbalanceado.

La selección generada permite obtener las distribuciones de clases descritas en la tesis, aunque las series y los pacientes seleccionados pueden diferir de los utilizados en los experimentos originales.

## Conjunto de datos

Se utiliza el subconjunto de entrenamiento de BCS-DBT, disponible públicamente a través de The Cancer Imaging Archive (TCIA).

Para ejecutar el notebook se requieren los archivos de metadatos:

- `BCS-DBT-file-paths-train-v2.csv`
- `BCS-DBT-labels-train-v2.csv`

Estos archivos permiten identificar las series, las categorías diagnósticas, los pacientes y las rutas de acceso a los volúmenes DICOM.

**Fuente:** [BCS-DBT — The Cancer Imaging Archive](https://www.cancerimagingarchive.net/collection/breast-cancer-screening-dbt/)

## Selección y partición

Las categorías `Cancer`, `Benign` y `Actionable` se agrupan como clase positiva (1), mientras que `Normal` corresponde a la clase negativa (0).

Inicialmente se seleccionan 916 series positivas y 916 negativas. Posteriormente, se construyen particiones de entrenamiento, validación y prueba mediante una asignación por paciente, evitando que un mismo paciente aparezca en más de una partición.

A partir de estas selecciones se preparan dos escenarios experimentales:

**Escenario balanceado**

| Partición | Negativas | Positivas | Total |
|---|---:|---:|---:|
| Entrenamiento | 1600 | 1597 | 3197 |
| Validación | 200 | 200 | 400 |
| Prueba | 200 | 200 | 400 |

**Escenario desbalanceado**

| Partición | Negativas | Positivas | Total |
|---|---:|---:|---:|
| Entrenamiento | 2178 | 726 | 2904 |
| Validación | 250 | 84 | 334 |
| Prueba | 251 | 83 | 334 |

Estas cantidades corresponden a las imágenes bidimensionales previstas según la estrategia de selección de cortes.

## Ejecución

1. Descargar los archivos de metadatos de BCS-DBT desde TCIA.
2. Abrir `01_seleccion_y_particion.ipynb` en Google Colab.
3. Cargar los archivos de metadatos cuando lo solicite el notebook.
4. Ejecutar las celdas en orden.

El notebook comprueba las distribuciones de clases y verifica que no existan pacientes compartidos entre entrenamiento, validación y prueba.

También genera archivos CSV con las selecciones de series correspondientes a cada escenario.

## Alcance y limitaciones

El notebook implementa la selección de series y la planificación de los cortes que deben extraerse de cada volumen.

No descarga los volúmenes DICOM ni genera las imágenes procesadas. Estas operaciones corresponden a una etapa posterior del preprocesamiento.

Por tanto, las cantidades indicadas representan los tamaños previstos de los conjuntos experimentales y no una comprobación de que todas las imágenes hayan sido descargadas y procesadas correctamente.
