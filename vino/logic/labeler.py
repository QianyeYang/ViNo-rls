from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon

from vino.gui.labeler import Ui_Labeler
from vino.logic.constants import SAMPLE_STATE
from vino.logic.flyout import FlyoutBubble
from vino.logic.globalSignals import gSignal
from vino.logic.annotationManager import VideoAnnotationManager
from vino.logic import utils
from vino.logic.globalVariables import GVar
from vino.logic.globalSignals import gSignal
import vino.resources_rc

from loguru import logger
from icecream import ic
import os


class LabelerScanListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(LabelerScanListModel, self).__init__(parent)

        self.__data = parent.index_dict
        self.__scan_uids = sorted(list(self.__data.keys()))


    def data(self, index, role):
        scan_uid = self.__scan_uids[index.row()]
        scan_state = self.__data[scan_uid]['state']

        if role == QtCore.Qt.DisplayRole:
            return scan_uid
        elif role == QtCore.Qt.DecorationRole:
            if scan_state == SAMPLE_STATE.LABELED:
                return QIcon(':/icons/check.png')
            elif scan_state == SAMPLE_STATE.ERROR:
                return QIcon(':/icons/error.png')
            else: pass
        else: pass            
            

    def rowCount(self, index):
        return len(self.__data)


class Labeler(QWidget):
    def __init__(self, master_module:QWidget, init_data:dict) -> None:
        super().__init__()
        self.ui = Ui_Labeler()
        self.ui.setupUi(self)
        self.flyout = FlyoutBubble(self)
        
        
        self.__index_dict:dict = {}
        self.__current_scan_uid:str = ''

        self.__master_module = master_module
        self.__init_data(data=init_data)
        self.__update_progress()
        
        self.ui.scan_list.doubleClicked.connect(self.listview_double_click_event)
        self.ui.frame_slider.valueChanged.connect(self.frame_index_changed)
        self.ui.radius_spin_box.valueChanged.connect(self.radius_value_changed)
        self.ui.fps_inputline.textChanged.connect(self.fps_changed)
        self.ui.depth_inputline.textChanged.connect(self.depth_changed)
        gSignal.videoFrameIndexMoveBackward.connect(self.video_move_backward)
        gSignal.videoFrameIndexMoveForward.connect(self.video_move_forward)
        gSignal.saveRequested.connect(self.on_save_button_clicked)
        
        self.annotation_manager = VideoAnnotationManager()
        self.annotation_manager.set_slicer(self.slicer)

        GVar.BBOX_RADIUS = self.ui.radius_spin_box.value()


    @Slot()
    def fps_changed(self):
        GVar.FPS = self.ui.fps_inputline.text()


    @Slot()
    def depth_changed(self):
        GVar.DEPTH = self.ui.depth_inputline.text()


    @Slot()
    def video_move_backward(self):
        self.ui.frame_slider.setValue(
            max(0, self.slicer.current_frame_index-1)
            )
        
    
    @Slot()
    def video_move_forward(self):
        self.ui.frame_slider.setValue(
            min(self.ui.frame_slider.maximum(), self.slicer.current_frame_index+1)
            )

    
    @Slot()
    def frame_index_changed(self):
        gSignal.videoFrameIndexChanged.emit(self.ui.frame_slider.value())

       
    def __init_data(self, data) -> None:
        '''
        Initialize the data.
        '''
        self.__index_dict = data['index']
        self.ui.scan_list.setModel(LabelerScanListModel(self))


    @property
    def index_dict(self) -> dict:
        return self.__index_dict
    

    @property
    def slicer(self):
        return self.ui.slicer


    @Slot()
    def __update_progress(self):
        p = sum(
            [i['state']==SAMPLE_STATE.LABELED for i in self.index_dict.values()]
            )
        self.ui.progressBar.setValue(
            int(100*p/len(self.index_dict))
        )
        

    @Slot()
    def on_save_button_clicked(self):
        '''
        Slot for the save button clicked.
        '''
        logger.info('>>> Validating save data...')
        
        depth_text = self.ui.depth_inputline.text()
        fps = self.ui.fps_inputline.text()
        radius = self.ui.radius_spin_box.value()

        if depth_text == '' or fps == '':
            utils.warning_box('>>> depth/fps info is missing.')
            return
        
        if utils.is_convertible_to_float(depth_text) and \
            utils.is_convertible_to_float(fps):
            depth = float(depth_text)
            fps = float(fps)
        else:
            utils.warning_box('>>> depth/fps must be numbers.')
            return
        
        if depth < 0 or fps < 0:
            utils.warning_box('>>> depth/fps must be 0 or positive.')
            return
        
        logger.info('>>> Save data validated. Saving...')

        ic(self.__current_scan_uid)
        save_path = self.index_dict[self.__current_scan_uid]['save_path']

        try:
            self.annotation_manager.save(save_path)
        except Exception as e:
            logger.error(f'>>> Error saving: {e}')
            utils.warning_box(
                f'>>> Error saving on scan {self.__current_scan_uid}. Please check.'
                )
            return

        if os.path.isfile(save_path):
            self.flyout.show_flyout(f"Scan {self.__current_scan_uid} saving done!")
            self.__index_dict[self.__current_scan_uid]['state'] = SAMPLE_STATE.LABELED
            self.__update_scan_list()

        self.__update_progress()


    def __update_scan_list(self):
        self.ui.scan_list.model().dataChanged.emit(
                self.ui.scan_list.model().index(0, 0),
                self.ui.scan_list.model().index(self.ui.scan_list.model().rowCount(None)-1, 0)
            )


    @Slot()
    def on_interpolate_button_clicked(self):
        '''
        Slot for the interpolate button clicked.
        '''
        try:
            self.annotation_manager.interpolate()
            self.flyout.show_flyout(f"Interpolation done!")
        except Exception as e:
            logger.error(f'>>> Error interpolating: {e}')
            utils.warning_box(
                f'>>> Error interpolating on scan {self.__current_scan_uid}. Please check.'
                )
        

    @Slot()
    def on_delete_button_clicked(self):
        '''
        Slot for the delete button clicked.
        '''
        saved_path = self.index_dict[self.__current_scan_uid]['save_path']
        if os.path.isfile(saved_path):
            os.remove(saved_path)
            logger.info(f'>>> Annotation file {saved_path} removed.')
        self.index_dict[self.__current_scan_uid]['state'] = SAMPLE_STATE.UNLABELED
        self.annotation_manager.delete_all()
        self.__update_scan_list()
        self.__update_progress()


    @Slot()
    def on_previous_button_clicked(self):
        '''
        Slot for self.ui.previous_button.
        '''
        selected_index = self.ui.scan_list.selectedIndexes()
        if not selected_index:
            logger.info('>>> Need to selecte a scan first.')
            return
        
        # check if it is the first scan
        if selected_index[0].row() == 0:
            logger.info('>>> This is the first scan.')
            return
        
        # move to select previous scan
        previous_index = self.ui.scan_list.model().index(selected_index[0].row()-1, 0)
        self.ui.scan_list.setCurrentIndex(previous_index)

        self.load_scan(previous_index.data())


    @Slot()
    def on_next_button_clicked(self):
        '''
        Slot for self.ui.next_button.
        '''
        selected_index = self.ui.scan_list.selectedIndexes()
        if not selected_index:
            logger.info('>>> Need to selecte a scan first.')
            return
        
        # check if it is the last scan
        if selected_index[0].row() == self.ui.scan_list.model().rowCount(None)-1:
            logger.info('>>> This is the last scan.')
            return
        
        # move to select next scan
        next_index = self.ui.scan_list.model().index(selected_index[0].row()+1, 0)
        self.ui.scan_list.setCurrentIndex(next_index)

        self.load_scan(next_index.data())


    @Slot()
    def listview_double_click_event(self, index):
        self.load_scan(index.data())


    @Slot()
    def radius_value_changed(self):
        GVar.BBOX_RADIUS = self.ui.radius_spin_box.value()
        gSignal.annotationBBoxRadiusUpdateRequest.emit(GVar.BBOX_RADIUS)


    def load_scan(self, scan_uid:str) -> None:
        '''
        Load the scan with the given scan_uid.
        '''
        logger.info(f'>>> Loading scan: {scan_uid}')
        self.__current_scan_uid = scan_uid

        self.ui.frame_slider.setValue(0)

        frame_paths = self.index_dict[scan_uid]['paths']
        self.slicer.load_frames(frame_paths)
        self.ui.frame_slider.setMaximum(len(frame_paths)-1)
        self.annotation_manager.delete_all()
        self.annotation_manager.init(len(frame_paths))
        
        if self.index_dict[scan_uid]['state'] == SAMPLE_STATE.LABELED:
            anno_path = self.index_dict[scan_uid]['save_path']
            self.annotation_manager.load(anno_path)
            logger.info(f'>>> Annotation file {anno_path} loaded.')

            # display the fps and depth
            saved_sample = utils.load_yaml(anno_path)[0]
            self.ui.fps_inputline.setText(str(saved_sample['fps']))
            self.ui.depth_inputline.setText(str(saved_sample['depth']))
            self.ui.radius_spin_box.setValue(saved_sample['radius'])
        else:
            self.ui.fps_inputline.setText('')
            self.ui.depth_inputline.setText('')
            self.ui.radius_spin_box.setValue(112)

        self.annotation_manager.update_current_index(0)


    def closeEvent(self, event) -> None:
        '''
        Override the close event.
        '''
        self.__master_module.show()
        event.accept()
