from typing import Any
import json, hashlib, yaml
import pandas as pd
import numpy as np
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QImage


def save_yaml(data: Any, yaml_path: str) -> None:
    '''
    Save data to a yaml file.

    :param data: The data to save.
    :type data: Any
    :param yaml_path: The path to the yaml file.
    :type yaml_path: str

    :return: None
    :rtype: None
    '''
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f)


def load_yaml(yaml_path: str) -> Any:
    '''
    Load a yaml file.

    :param yaml_path: The path to the yaml file.
    :type yaml_path: str

    :return: The data from the yaml file.
    :rtype: Any
    '''
    with open(yaml_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data


def compute_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
    '''
    '''
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_json(json_path: str) -> Any:
    '''
    Load a json file.

    :param json_path: The path to the json file.
    :type json_path: str

    :return: The data from the json file.
    :rtype: Any
    '''
    f = open(json_path, 'r')
    data = json.load(f)
    f.close()
    # with open(json_path, 'r') as f:
    #     data = json.load(f)

    return data


def save_json(data: Any, json_path: str) -> None:
    '''
    Save data to a json file.

    :param data: The data to save.
    :type data: Any
    :param json_path: The path to the json file.
    :type json_path: str

    :return: None
    :rtype: None
    '''
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)


def load_csv(csv_path: str) -> pd.DataFrame:
    '''
    Load a csv file.

    :param csv_path: The path to the csv file.
    :type csv_path: str

    :return: The data from the csv file.
    :rtype: pd.DataFrame
    '''
    return pd.read_csv(csv_path)


def warning_box(warning: str) -> None:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Warning")
    msg.setInformativeText(warning)
    msg.setWindowTitle("Warning")
    msg.exec_()


def numpy_to_pixmap(array:np.ndarray) -> QPixmap:
    '''Converts a numpy array to a QPixmap'''
    array = np.ascontiguousarray(array)
    height, width, _ = array.shape
    bytes_per_line = width
    qimage = QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    return QPixmap.fromImage(qimage)


def is_convertible_to_float(s:str) -> bool:
    '''
    Check if a string can be converted to a float. 

    :param s: The string to check.
    :type s: str

    :return: True if the string can be converted to a float, False otherwise.
    '''
    try:
        float(s)  # Try to convert the string to a float
        return True
    except ValueError:
        return False