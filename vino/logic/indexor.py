from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PySide6.QtCore import QObject, Signal, Qt, Slot, QCoreApplication
from PySide6.QtStateMachine import QState, QStateMachine
from PySide6.QtGui import QKeyEvent
from icecream import ic
from glob import glob
from loguru import logger
from typing import Union
import os, vino
from vino.gui.indexor import Ui_Indexor
from vino.logic.labeler import Labeler
from vino.logic import utils
from vino.logic.constants import SAMPLE_STATE

class Indexor(QWidget):
    def __init__(self) -> None:
        super().__init__()

# state.entered.connect(enter_function)
# state.exited.connect(exit_function)

class StateTransitionSignals(QObject):
    state_trans_1_to_2 = Signal()
    state_trans_2_to_1 = Signal()
    

class CocheDataIndexor(Indexor):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Indexor()
        self.ui.setupUi(self)

        # self.__data_folder: str = ''
        self.ui.csv_combobox.currentIndexChanged.connect(self.state_transfering_checker)
        self.__set_statemachine()

        self.__load_config()
        
        self.csv_folder = os.path.join(
            vino.DIR_PROJECT, 'projects', 'coche', 'index_csv')
        self.csv_list = glob(os.path.join(self.csv_folder, '*.csv'))
        self.ui.csv_combobox.addItems([os.path.basename(csv) for csv in self.csv_list])

        self.__target_module = None
        QCoreApplication.processEvents()  # force the update of the ui
        self.state_transfering_checker()


    def __load_config(self) -> None:
        '''
        Load the configuration.
        '''
        if not os.path.isfile(vino.DIR_CONFIG):
            logger.info('>>> No init configuration file found.')
        config = utils.load_yaml(vino.DIR_CONFIG)

        data_folder: str = config['data_folder']
        if data_folder and os.path.isdir(data_folder):
            self.__data_folder = data_folder
            self.ui.path_label.setText(self.__data_folder)


    def __set_statemachine(self) -> None:
        '''
        Set the state machine for the indexor.
        '''
        self.state_trans_signals = StateTransitionSignals()

        self.__state_machine = QStateMachine(self)
        self.__state_setting_L_1 = QState(self.__state_machine)
        self.__state_complete_L_2= QState(self.__state_machine)
        self.__state_machine.setInitialState(self.__state_setting_L_1)

        self.__state_setting_L_1.entered.connect(self.state_setting_L_1_entered)
        self.__state_complete_L_2.entered.connect(self.state_complete_L_2_entered)

        self.__state_setting_L_1.addTransition(
            self.state_trans_signals.state_trans_1_to_2, self.__state_complete_L_2
            )
        self.__state_complete_L_2.addTransition(
            self.state_trans_signals.state_trans_2_to_1, self.__state_setting_L_1
            )
        self.__state_machine.start()


    @property
    def progress(self) -> int:
        return self.ui.progress.value()
    @progress.setter
    def progress(self, value:Union[int, float]) -> None:
        value = int(min(100, max(0, value)))
        self.ui.progress.setValue(value)
        QCoreApplication.processEvents()


    @Slot()
    def state_setting_L_1_entered(self) -> None:
        '''
        Slot for the state_setting_L_1.entered signal.
        '''
        self.ui.start_button.setEnabled(False)
        self.progress = 0


    @Slot()
    def state_complete_L_2_entered(self) -> None:
        '''
        Slot for the state_complete_L_2.entered signal.
        '''
        logger.info('>>> State complete L_2 entered.')
        self.ui.start_button.setEnabled(True)
        

    @property
    def selected_csv(self) -> str:
        return os.path.join(self.csv_folder, self.ui.csv_combobox.currentText())
    

    @Slot()
    def on_start_button_clicked(self) -> None:
        '''
        Slot for self.ui.start_button.clicked signal.
        '''
        index_data = self.extract_data()
        
        if isinstance(index_data, str):
            utils.warning_box(index_data)
            return
        
        self.labeler_window = Labeler(
            master_module=self, 
            init_data={
                'index': index_data,
                'save_path': os.path.join(
                    vino.DIR_PROJECT, 'projects', 'coche', 'annotation'
                )
            }
        )
        self.hide()
        self.labeler_window.show()

    
    @Slot()
    def on_select_folder_button_clicked(self) -> None:
        '''
        Slot for self.ui.select_folder_button.clicked signal.
        '''
        print('Selected folder button clicked')
        folder = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder and os.path.isdir(folder):
            self.__data_folder = folder
            self.ui.path_label.setText(folder)
            self.state_transfering_checker()


    @Slot()
    def state_transfering_checker(self) -> None:
        '''
        Check the state transfering.
        '''
        logger.info('>>> Checking the state transfering...')
        if self.ui.csv_combobox.currentText() and \
            os.path.isdir(self.ui.path_label.text()):
            self.state_trans_signals.state_trans_1_to_2.emit()
        else:
            self.state_trans_signals.state_trans_2_to_1.emit()


    def extract_data(self) -> Union[dict, str]:
        '''
        Extract data from the selected csv file, meanwhile do the validation.
        '''
        logger.info(f'>>> Extracting data from {self.selected_csv}...')
        save_root = os.path.join(
            vino.DIR_PROJECT, 'projects', 'coche', 'annotation'
        )
        data_root = self.__data_folder
        df = utils.load_csv(self.selected_csv)

        scan_uid_list = df['scan'].unique().tolist()
        if len(scan_uid_list) == 0: return "No scan_uid in the csv file."

        data = {}
        for idx, scan_uid in enumerate(scan_uid_list):
            pid = df[df['scan'] == scan_uid]['participantFull'].tolist()[0]

            self.progress = (idx + 1) / len(scan_uid_list) * 100

            if os.path.isfile(
                os.path.join(save_root, f'[{pid}]{scan_uid}.yaml')
            ):
                state = SAMPLE_STATE.LABELED
            else:
                state = SAMPLE_STATE.UNLABELED
            
            paths = df[df['scan'] == scan_uid]['path'].tolist()
            paths = [
                os.path.join(data_root, path[1:]).replace('.tif','.jpg') for path in paths
                ]
            paths_exist = list(map(os.path.isfile, paths))
            
            if not all(paths_exist):
                logger.warning(f'>>> Missing files for scan {scan_uid}.')
                state = SAMPLE_STATE.ERROR

            
            save_path = os.path.join(
                vino.DIR_PROJECT, 
                f'projects/coche/annotation/[{pid}]{scan_uid}.yaml'
                )
            
            data[str(scan_uid)] = {
                'paths': paths,
                'df_key': scan_uid,  # preserve the data type in df
                'state': state,
                'save_path': save_path
            }
        return data
    

    def keyPressEvent(self, event: QKeyEvent) -> None:
        return
    
        
        
            
        
