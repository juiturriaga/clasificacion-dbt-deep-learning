# Selección y preprocesamiento de imágenes DBT

Esta carpeta contiene dos notebooks que documentan un procedimiento de referencia para seleccionar series, dividir los datos por paciente y preparar imágenes de tomosíntesis digital de mama (DBT) del conjunto **BCS-DBT** disponible en TCIA.

## Notebooks

**`01_seleccion_y_particion.ipynb`**: utiliza los metadatos del conjunto para seleccionar series y crear los escenarios balanceado y desbalanceado. Comprueba que no haya pacientes compartidos entre las particiones y genera seis CSV con series y cortes seleccionados. Los CSV se guardan en la carpeta `selecciones_generadas/` del entorno de ejecución.

**`02_extraccion_y_preprocesamiento.ipynb`**: lee los seis CSV, permite descargar los DICOM correspondientes, extrae los cortes indicados, convierte las imágenes a `float32`, normaliza las intensidades por su valor máximo, redimensiona a 512 × 512 píxeles y guarda imágenes y etiquetas en archivos `.npy`.

## Datos de entrada

Para el primer notebook se necesitan los metadatos originales de BCS-DBT:

- `BCS-DBT-file-paths-train-v2*.xlsx`
- `BCS-DBT-labels-train-v2*.csv`

El segundo notebook requiere los seis CSV generados por el primero y acceso a TCIA para recuperar las series DICOM identificadas por `SeriesInstanceUID`.

## Orden de ejecución

1. Abrir `01_seleccion_y_particion.ipynb` en Google Colab y proporcionar los dos archivos de metadatos.
2. Ejecutar sus celdas y localizar los seis CSV en `selecciones_generadas/`.
3. Colocar los seis CSV en el directorio desde el cual se ejecutará `02_extraccion_y_preprocesamiento.ipynb` (o cargarlos cuando el notebook lo solicite).
4. En el segundo notebook, revisar las opciones de ejecución. Por defecto `EJECUTAR_DESCARGA = False` (no descarga), `MODO_PRUEBA = True` (una serie al habilitar la descarga) y `TODOS_LOS_CONJUNTOS = False` (un conjunto elegido).
5. Habilitar explícitamente la descarga solo cuando se disponga de espacio, conexión y datos adecuados. El modo de prueba permite comprobar una serie, pero no verifica el procesamiento integral.

## Limitaciones y reproducibilidad

- La selección incluida reconstruye el procedimiento y puede diferir de las series utilizadas en los experimentos originales.
- El procesamiento completo de los conjuntos con este flujo publicado no se ha verificado.
- La extracción implementada supone volúmenes DICOM multiframe; otras organizaciones de archivos pueden requerir adaptaciones.
- Las distribuciones objetivo comprueban la selección planificada, pero no demuestran que todas las imágenes hayan sido descargadas y procesadas.
- Los archivos resultantes pueden requerir ajustes de nombre y ubicación para ser usados por los notebooks de [`../modelos/`](../modelos/).

Los archivos de imagen no están incluidos en el repositorio por su tamaño. La descarga requiere respetar las condiciones de uso y atribución del conjunto original.
