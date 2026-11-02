
import numpy as np
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

SEMILLA = 42


def preparar_datos_mnist_binario(
    clase_0=3,
    clase_1=8,
    formato="vector",
    one_hot=False,
    etiquetas=(0, 1),
    val_size=0.15,
    test_size=0.15,
    semilla=SEMILLA,
):
    """
    Prepara un subconjunto binario de MNIST para el entrenamiento
    y la evaluación de diferentes arquitecturas de redes neuronales.

    Las particiones originales de MNIST se combinan y posteriormente
    se seleccionan las imágenes correspondientes a las dos clases
    especificadas. Los datos se dividen de forma estratificada en
    entrenamiento, validación y prueba.

    Parámetros
    ----------
    clase_0, clase_1 : int
        Dígitos utilizados para la clasificación binaria.
    formato : str
        'vector': imágenes aplanadas con dimensiones (N, 784).
        'imagen': imágenes con dimensiones (N, 1, 28, 28).
    one_hot : bool
        Si es True, las etiquetas se representan mediante vectores
        de dos componentes, con dimensiones (N, 2).
    etiquetas : tuple
        Valores asignados a las clases seleccionadas.
        Por ejemplo, (0, 1) o (-1, 1).
    val_size, test_size : float
        Proporciones del conjunto completo destinadas a validación
        y prueba, respectivamente.
    semilla : int
        Semilla utilizada para la reproducibilidad de las particiones.

    Devuelve
    --------
    dict
        Diccionario con las particiones 'train', 'val' y 'test',
        cada una formada por una tupla (X, y).

        Cuando one_hot=False, las etiquetas tienen dimensiones (N, 1).
        Cuando one_hot=True, tienen dimensiones (N, 2).

        La entrada 'info' contiene información general sobre
        las particiones y los parámetros de selección.
    """
    np.random.seed(semilla)

    # Carga y combinación de las particiones originales de MNIST
    (X_tr, y_tr), (X_te, y_te) = mnist.load_data()

    X = np.concatenate([X_tr, X_te], axis=0)
    y = np.concatenate([y_tr, y_te], axis=0)

    # Selección de las dos clases de interés
    mask = (y == clase_0) | (y == clase_1)

    X = X[mask]
    y = y[mask]

    # Partición estratificada en entrenamiento y evaluación
    X_train, X_resto, y_train, y_resto = train_test_split(
        X,
        y,
        test_size=(val_size + test_size),
        stratify=y,
        random_state=semilla,
    )

    # División del conjunto de evaluación en validación y prueba
    proporcion_test = test_size / (val_size + test_size)

    X_val, X_test, y_val, y_test = train_test_split(
        X_resto,
        y_resto,
        test_size=proporcion_test,
        stratify=y_resto,
        random_state=semilla,
    )

    # Normalización de las intensidades al intervalo [0, 1]
    X_train = X_train.astype(np.float32) / 255.0
    X_val = X_val.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0

    # Adaptación de las dimensiones según la arquitectura
    if formato == "vector":
        X_train = X_train.reshape(-1, 784)
        X_val = X_val.reshape(-1, 784)
        X_test = X_test.reshape(-1, 784)

    elif formato == "imagen":
        X_train = X_train[:, np.newaxis, :, :]
        X_val = X_val[:, np.newaxis, :, :]
        X_test = X_test[:, np.newaxis, :, :]

    else:
        raise ValueError("formato debe ser 'vector' o 'imagen'")

    # Codificación de las etiquetas
    val_0, val_1 = etiquetas

    y_train = np.where(y_train == clase_1, val_1, val_0)
    y_val = np.where(y_val == clase_1, val_1, val_0)
    y_test = np.where(y_test == clase_1, val_1, val_0)

    if one_hot:

        def to_one_hot(labels):
            # Conversión a índices binarios para la codificación one-hot
            labels01 = (labels == val_1).astype(int)

            oh = np.zeros((len(labels01), 2))
            oh[np.arange(len(labels01)), labels01] = 1

            return oh

        y_train, y_val, y_test = map(
            to_one_hot,
            (y_train, y_val, y_test),
        )

    else:
        y_train = y_train.reshape(-1, 1).astype(np.float32)
        y_val = y_val.reshape(-1, 1).astype(np.float32)
        y_test = y_test.reshape(-1, 1).astype(np.float32)

    info = {
        "n_train": len(X_train),
        "n_val": len(X_val),
        "n_test": len(X_test),
        "clase_0": clase_0,
        "clase_1": clase_1,
        "semilla": semilla,
    }

    return {
        "train": (X_train, y_train),
        "val": (X_val, y_val),
        "test": (X_test, y_test),
        "info": info,
    }


def calcular_metricas(y_true, y_pred, y_scores=None, clase_positiva=1):
    """
    Calcula las métricas de evaluación utilizadas para comparar
    los modelos de clasificación binaria.

    Parámetros
    ----------
    y_true : array
        Etiquetas reales.
    y_pred : array
        Clases predichas por el modelo.
    y_scores : array, opcional
        Puntuaciones continuas utilizadas para calcular el AUC.
        Deben corresponder a la clase positiva.
    clase_positiva : int
        Valor utilizado para identificar la clase positiva.

    Devuelve
    --------
    dict
        Diccionario con exactitud, sensibilidad, especificidad,
        puntuación F1 y AUC.

        Si no se proporcionan puntuaciones continuas,
        el AUC no se calcula y se devuelve None.
    """
    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()

    acc = accuracy_score(y_true, y_pred)

    sensibilidad = recall_score(
        y_true,
        y_pred,
        pos_label=clase_positiva,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        y_pred,
        pos_label=clase_positiva,
        zero_division=0,
    )

    # Identificación de la clase negativa
    clases_negativas = [
        clase for clase in np.unique(y_true)
        if clase != clase_positiva
    ]

    if len(clases_negativas) != 1:
        raise ValueError(
            "Se requieren dos clases y una clase positiva válida."
        )

    clase_negativa = clases_negativas[0]

    # Cálculo de la especificidad a partir de la matriz de confusión
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[clase_negativa, clase_positiva],
    ).ravel()

    especificidad = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else np.nan
    )

    # Cálculo del área bajo la curva ROC
    auc = None

    if y_scores is not None:
        try:
            scores = np.asarray(y_scores).flatten()
            y_true_binario = (y_true == clase_positiva).astype(int)
            auc = roc_auc_score(y_true_binario, scores)

        except ValueError:
            auc = np.nan

    return {
        "accuracy": acc,
        "sensibilidad": sensibilidad,
        "especificidad": especificidad,
        "f1": f1,
        "auc": auc,
    }


if __name__ == "__main__":
    # Verificación de la preparación de los datos
    datos = preparar_datos_mnist_binario(formato="vector")

    print("Información de las particiones:", datos["info"])

    X_train, y_train = datos["train"]
    X_val, y_val = datos["val"]
    X_test, y_test = datos["test"]

    print("Entrenamiento:", X_train.shape, y_train.shape)
    print("Validación:   ", X_val.shape, y_val.shape)
    print("Prueba:       ", X_test.shape, y_test.shape)
