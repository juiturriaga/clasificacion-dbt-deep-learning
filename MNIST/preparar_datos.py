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
    formato="vector",          # 'vector' (perceptrón/MLP) o 'imagen' (CNN)
    one_hot=False,             # True solo si el modelo espera salida softmax de 2 neuronas
    etiquetas=(0, 1),          # valores de salida para (clase_0, clase_1). Perceptrón usa (-1, 1)
    val_size=0.15,
    test_size=0.15,
    semilla=SEMILLA,
):
    """
    Descarga MNIST, se queda solo con dos dígitos, y devuelve un split
    estratificado train/val/test, con formato y etiquetas configurables
    según lo que espera cada arquitectura.

    Parámetros
    ----------
    formato : 'vector' -> arrays (N, 784), normalizados [0,1]
              'imagen' -> arrays (N, 1, 28, 28), normalizados [0,1]
    one_hot : si True, y tiene shape (N, 2) en lugar de (N, 1)/(N,)
    etiquetas : tupla (valor_clase_0, valor_clase_1). Ej: (0,1) o (-1,1)

    Devuelve
    --------
    dict con 'train', 'val', 'test', cada uno tupla (X, y),
    más 'info' con conteos por partición para reportar en la tesis.
    """
    np.random.seed(semilla)

    # 1. Cargar y combinar train+test originales
    (X_tr, y_tr), (X_te, y_te) = mnist.load_data()
    X = np.concatenate([X_tr, X_te], axis=0)
    y = np.concatenate([y_tr, y_te], axis=0)

    # 2. Quedarnos solo con las dos clases de interés
    mask = (y == clase_0) | (y == clase_1)
    X = X[mask]
    y = y[mask]

    # 3. Split estratificado train / val+test
    X_train, X_resto, y_train, y_resto = train_test_split(
        X, y,
        test_size=(val_size + test_size),
        stratify=y,
        random_state=semilla,
    )
    # 4. Split val / test dentro del resto
    proporcion_test = test_size / (val_size + test_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_resto, y_resto,
        test_size=proporcion_test,
        stratify=y_resto,
        random_state=semilla,
    )

    # 5. Normalizar [0, 1] 
    X_train = X_train.astype(np.float32) / 255.0
    X_val = X_val.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0

    # 6. Dar forma según el modelo 
    if formato == "vector":
        X_train = X_train.reshape(-1, 784)
        X_val = X_val.reshape(-1, 784)
        X_test = X_test.reshape(-1, 784)
    elif formato == "imagen":
        X_train = X_train[:, np.newaxis, :, :]   # (N, 1, 28, 28)
        X_val = X_val[:, np.newaxis, :, :]
        X_test = X_test[:, np.newaxis, :, :]
    else:
        raise ValueError("formato debe ser 'vector' o 'imagen'")

    # 7. Recodificar etiquetas
    val_0, val_1 = etiquetas
    y_train = np.where(y_train == clase_1, val_1, val_0)
    y_val = np.where(y_val == clase_1, val_1, val_0)
    y_test = np.where(y_test == clase_1, val_1, val_0)

    if one_hot:
        def to_one_hot(labels):
            # asume etiquetas 0/1 para poder indexar
            labels01 = (labels == val_1).astype(int)
            oh = np.zeros((len(labels01), 2))
            oh[np.arange(len(labels01)), labels01] = 1
            return oh
        y_train, y_val, y_test = map(to_one_hot, (y_train, y_val, y_test))
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
    Calcula el mismo set de métricas para los tres modelos, de forma
    que sean directamente comparables.

    y_true, y_pred : arrays 1D con las etiquetas 0/1 (o -1/1, ver nota)
    y_scores       : opcional, puntuación continua (para AUC-ROC).
                      Si no se pasa, AUC queda como None.

    Nota: si tu modelo usa etiquetas -1/1 (como el Perceptrón), convertí
    a 0/1 antes de llamar a esta función:
        y_true01 = np.where(y_true == 1, 1, 0)

    Devuelve un dict con: accuracy, sensibilidad (recall clase positiva),
    especificidad (recall clase negativa), f1, auc.
    """
    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()

    acc = accuracy_score(y_true, y_pred)
    sensibilidad = recall_score(y_true, y_pred, pos_label=clase_positiva)
    f1 = f1_score(y_true, y_pred, pos_label=clase_positiva)

    # especificidad = recall de la clase negativa
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    especificidad = tn / (tn + fp) if (tn + fp) > 0 else np.nan

    auc = None
    if y_scores is not None:
        try:
            auc = roc_auc_score(y_true, np.asarray(y_scores).flatten())
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
    # Prueba rápida / demo de uso
    datos = preparar_datos_mnist_binario(formato="vector")
    print("Info del split:", datos["info"])
    X_train, y_train = datos["train"]
    X_val, y_val = datos["val"]
    X_test, y_test = datos["test"]
    print("Train:", X_train.shape, y_train.shape)
    print("Val:  ", X_val.shape, y_val.shape)
    # print("Test: ", X_test.shape, y_test.shape)