from . import *
import os


DIR_PROJECT = os.path.dirname(os.path.dirname(__file__))
DIR_CONFIG = os.path.join(DIR_PROJECT, 'config.yaml')
DIR_PACKAGE = os.path.dirname(__file__)
DIR_GUI = os.path.join(DIR_PACKAGE, 'gui')
DIR_UI_FILES = os.path.join(DIR_PACKAGE, 'ui_files')
DIR_MATERIAL = os.path.join(os.path.dirname(__file__), 'materials')
DIR_DATABASE = os.path.join(DIR_MATERIAL, 'database')

FILE_UI_HASH_RECORD = os.path.join(DIR_MATERIAL, 'database', 'ui_records.json')
FILE_RESOURCE = os.path.join(DIR_PACKAGE, 'resources.qrc')