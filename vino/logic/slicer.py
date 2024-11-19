from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QGraphicsPixmapItem, QRubberBand, QWidget, QGraphicsTextItem, QGraphicsItem, QPushButton, QLabel, QGraphicsEllipseItem, QGraphicsPathItem, QMessageBox, QGraphicsLineItem
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPainter, QWheelEvent, QPen, QBrush, QImage, QPixmap, QColor, QFont, QPainterPath, QTransform, QCursor, QFocusEvent
from PySide6.QtCore import Qt, QPointF, Signal, QRect, QRectF, QPoint, QSizeF, QSize, QEvent, QLineF, Slot, QTimer
import cv2 
import numpy as np 
from loguru import logger
from icecream import ic
from vino.logic.globalSignals import gSignal
from vino.logic import utils
from vino.logic.constants import ANNOTATION_TYPE
from vino.logic.globalVariables import GVar


class VideoSlicer(QGraphicsView):
    def __init__(
            self, 
            *args, 
            **kwargs
            ):
        super().__init__(*args, **kwargs)

        self.__scene = QGraphicsScene(self)
        self.__scene.setBackgroundBrush(QBrush(QColor("black")))
        self.setScene(self.__scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setRenderHint(QPainter.TextAntialiasing)

        self.__scene.setSceneRect(QRectF(0, 0, 2000, 2000))
        self.__current_frame_index = 0
        self.setScene(self.__scene)
        self.__pixmap_item = QGraphicsPixmapItem()
        self.__scene.addItem(self.__pixmap_item)

        self.__video_array = np.zeros([5, 100, 100, 3])
        
        self.__init_key_states()

        gSignal.videoFrameIndexChanged.connect(self.video_frame_index_changed)


    def __init_key_states(self) -> None:
        self.__key_timer = QTimer()
        self.__hold_key = None
        self.__key_timer.setInterval(20)
        self.__key_timer.timeout.connect(self.__key_press_timeout)


    @property
    def frame_shape(self):
        return self.__video_array.shape[1:3]


    @Slot(int)
    def video_frame_index_changed(self, index:int)->None:
        self.current_frame_index = index


    @property
    def pixmap_item(self):
        return self.__pixmap_item

    
    @property
    def scene_width(self):
        return int(self.__scene.width())
    

    @property
    def scene_height(self):
        return int(self.__scene.height())
    

    @property
    def item_width(self):
        return self.pixmap_item.sceneBoundingRect().width()
    
    
    @property
    def item_height(self):
        '''
        Same to the mechanism in item_width.
        '''
        return self.pixmap_item.sceneBoundingRect().height()


    @property
    def current_frame_index(self)->int:
        return self.__current_frame_index
    @current_frame_index.setter
    def current_frame_index(self, value:int)->None:
        value = min(self.__video_array.shape[0]-1, max(0, value))
        self.__current_frame_index = value
        self.update_display()

    
    @property
    def scene(self)->QGraphicsScene:
        return self.__scene
    
    
    def load_frames(self, frame_paths: list[str]) -> None:
        frames = []
        for i, frame_path in enumerate(frame_paths):
            frame = cv2.imread(frame_path)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            height, width, channel = frame.shape
        self.__video_array = np.stack(frames, axis=0)
        
        self.update_display()
        logger.info(f'>>> Video array shape: {self.__video_array.shape}')


    @Slot()
    def update_display(self) -> None:
        frame = self.__video_array[self.__current_frame_index]
        self.__pixmap_item.setPixmap(
            QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888))
            )
        gSignal.annotationIndexUpdateRequest.emit(self.__current_frame_index)
        self.__pixmap_item.setPos(
            self.scene_width/2 - self.item_width/2,
            self.scene_height/2 - self.item_height/2
        )
        self.fitInView(self.__pixmap_item, Qt.KeepAspectRatio)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            gSignal.annotationPostionUpdateRequest.emit(
                self.current_frame_index,
                ANNOTATION_TYPE.START_BBOX,
                self.mapToScene(event.pos()), 
                GVar.BBOX_RADIUS
            )
            ic(GVar.BBOX_RADIUS)
        elif event.button() == Qt.RightButton:
            gSignal.annotationPostionUpdateRequest.emit(
                self.current_frame_index,
                ANNOTATION_TYPE.END_BBOX,
                self.mapToScene(event.pos()),
                GVar.BBOX_RADIUS
            )
        else: pass


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            gSignal.saveRequested.emit()
        elif event.key() == Qt.Key_Q:
            gSignal.videoFrameIndexMoveBackward.emit()
        elif event.key() == Qt.Key_E:
            gSignal.videoFrameIndexMoveForward.emit()
        else: pass

        if event.key() in [Qt.Key_A, Qt.Key_D]:
            self.__hold_key = event.key()
            self.__key_timer.start()


    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() in [Qt.Key_A, Qt.Key_D]:
            self.__hold_key = None
            self.__key_timer.stop()


    def enterEvent(self, event: QEvent) -> None:
        self.setFocus()
        super().enterEvent(event)


    Slot()
    def __key_press_timeout(self):
        if self.__hold_key == Qt.Key_A:
            gSignal.videoFrameIndexMoveBackward.emit()
        elif self.__hold_key == Qt.Key_D:
            gSignal.videoFrameIndexMoveForward.emit()

            

    
        

        