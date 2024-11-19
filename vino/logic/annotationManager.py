from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QGraphicsRectItem, QGraphicsPixmapItem, QRubberBand, QWidget, QGraphicsTextItem, QGraphicsItem, QPushButton, QLabel, QGraphicsEllipseItem, QGraphicsPathItem, QMessageBox, QGraphicsLineItem
from PySide6.QtGui import QPainter, QWheelEvent, QPen, QBrush, QImage, QPixmap, QColor, QFont, QPainterPath, QTransform, QCursor, QFocusEvent
from PySide6.QtCore import Qt, QPointF, Signal, QRect, QRectF, QPoint, QSizeF, QSize, QEvent, QLineF, Slot

from vino.logic.constants import ANNOTATION_TYPE
from vino.logic.globalVariables import GVar
from vino.logic.globalSignals import gSignal
from vino.logic import utils
from time import time
from icecream import ic
from loguru import logger
import os

class BboxAnnotation(object):
    def __init__(self, anno_type:ANNOTATION_TYPE) -> None:
        super().__init__()
        if anno_type is not None:
            self.__atype = anno_type
        else:
            self.__atype = ANNOTATION_TYPE.EMPTY
        self.__center:list = QPointF(300, 300)
        self.__radius:float = GVar.BBOX_RADIUS
        self.display_item = QGraphicsRectItem(
            self.__center.x(), 
            self.__center.y(), 
            2 * self.__radius, 
            2 * self.__radius
        )

    @property
    def atype(self) -> ANNOTATION_TYPE:
        return self.__atype
    
    def __repr__(self) -> str:
        return f"type:{self.__atype}, center:{self.__center}, radius:{self.__radius}, color:{self.color}, display_item:{self.display_item.pos()}"


    @property
    def center(self) -> list:
        return self.__center
    

    @property
    def radius(self) -> float:
        return self.__radius
    

    @property
    def color(self) -> QColor:
        if self.__atype == ANNOTATION_TYPE.START_BBOX:
            return QColor(255, 255, 0)
        elif self.__atype == ANNOTATION_TYPE.END_BBOX:
            return QColor(255, 0, 255)
        else:
            return QColor(255, 255, 255)
    

    def to_atype(self, atype:int):
        assert isinstance(atype, int), '>>> atype must be an integer.'
        self.__atype = atype


    def set_position(self, center:QPointF, radius: float) -> None:
        self.__center = center
        self.__radius = radius
        self.display_item.setRect(
            center.x() - radius,
            center.y() - radius,
            2 * radius,
            2 * radius
        )
        self.display_item.setPen(QPen(self.color))


    def set_radius(self, radius:float) -> None:
        self.__radius = radius
        self.display_item.setRect(
            self.__center.x() - radius,
            self.__center.y() - radius,
            2 * radius,
            2 * radius
        )
        self.display_item.setPen(QPen(self.color))


class VideoAnnotationManager(object):
    def __init__(self) -> None:
        self.__data = []
        gSignal.annotationPostionUpdateRequest.connect(self.update_annotation)
        gSignal.annotationIndexUpdateRequest.connect(self.update_current_index)
        gSignal.annotationBBoxRadiusUpdateRequest.connect(self.update_radius)
        self.__slicer = None


    def set_slicer(self, slicer) -> None:
        self.__slicer = slicer


    @property
    def scene(self) -> QGraphicsScene:
        return self.__slicer.scene

    
    def load(self, savefile_path:str) -> None:
        assert os.path.isfile(savefile_path), '>>> savefile_path does not exist.'
        save_data = utils.load_yaml(savefile_path)
        for frame_data in save_data:
            pixmap_center = QPointF(frame_data['center'][0], frame_data['center'][1])
            scene_center = self.__slicer.pixmap_item.mapToScene(pixmap_center)

            self.update_annotation(
                index = frame_data['frame_index'],
                annotation_type = frame_data['type'],
                position = scene_center,
                radius = frame_data['radius']
            )
                

    def save(self, save_path:str) -> list:
        # need mapping back to scene coordinates
        save_data = []
        timestamp = time()
        radius = GVar.BBOX_RADIUS
        fps = int(GVar.FPS)
        depth = float(GVar.DEPTH)
        frame_shape = list(self.__slicer.frame_shape)

        for index, anno in enumerate(self.__data):
            if anno.atype == ANNOTATION_TYPE.EMPTY:
                continue
            center_on_pixmap = self.__slicer.pixmap_item.mapFromScene(anno.center)
            center = [
                center_on_pixmap.x(), 
                center_on_pixmap.y()
                ]
            save_data.append({
                "frame_index": index,
                "frame_shape": frame_shape,
                "type": anno.atype,
                "center": center,
                "radius": radius,
                "fps": fps, 
                "depth": depth,
                "timestamp": timestamp
            })

        utils.save_yaml(
            data=save_data, yaml_path=save_path
            )


    def init(self, video_length:int) -> None:
        assert video_length > 0, '>>> video_length must be greater than 0.'
        assert isinstance(video_length, int), '>>> video_length must be an integer.'
        self.__data = [
            BboxAnnotation(ANNOTATION_TYPE.EMPTY) for _ in range(video_length)
            ]
        
        for anno in self.__data:
            self.scene.addItem(anno.display_item)


    def delete_all(self):
        for anno in self.__data:
            self.scene.removeItem(anno.display_item)
            anno.to_atype(ANNOTATION_TYPE.EMPTY)
        
        

    @Slot(int, int, QPointF, int)
    def update_annotation(
        self, 
        index:int,
        annotation_type:int, 
        position:QPointF,
        radius:float
        ) -> None:
        anno = self.__data[index]
        anno.to_atype(annotation_type)
        anno.set_position(position, radius)


    @Slot(int)
    def update_current_index(self, index:int) -> None:
        for idx, anno in enumerate(self.__data):
            if idx == index:
                anno.display_item.setVisible(True)
            else:
                anno.display_item.setVisible(False)


    @Slot(int)
    def update_radius(self, radius:int) -> None:
        for anno in self.__data:
            anno.set_radius(radius)


    @Slot()
    def interpolate(self) -> None:
        ## think if additional sanity checks are needed....
        # print('>>> in Interpolating...')
        # 1. get each segment
        end_indices = []
        for idx, anno in enumerate(self.__data):
            if anno.atype == ANNOTATION_TYPE.END_BBOX:
                end_indices.append(idx)
        end_indices.insert(0, 0)
        # ic(end_indices)
        segments = []
        for i in range(len(end_indices)-1):
            if i==0:
                segments.append(self.__data[end_indices[i]:end_indices[i+1]+1])
            else:
                segments.append(self.__data[end_indices[i]+1:end_indices[i+1]+1])
        
        temp = []
        for seg in segments:
            start_idx = 0
            for idx, f in enumerate(seg):
                if f.atype == ANNOTATION_TYPE.START_BBOX:
                    start_idx = idx
                    break
            temp.append(seg[start_idx:])
                
        segments = [i for i in temp if len(i)>2]

        # 2. interpolate each segment
        for seg in segments:
            coords = [
                [anno.center.x(), anno.center.y()] \
                    if anno.atype != ANNOTATION_TYPE.EMPTY else [] \
                        for anno in seg
                ]
            
            valid_indices = [i for i, point in enumerate(coords) if point]

            # Interpolate for missing data between valid points
            for i in range(1, len(valid_indices)):
                start_idx = valid_indices[i - 1]
                end_idx = valid_indices[i]
                
                x1, y1 = coords[start_idx]
                x2, y2 = coords[end_idx]
                
                num_missing = end_idx - start_idx - 1
                
                if num_missing > 0:
                    for j in range(1, num_missing + 1):
                        interpolated_x = x1 + (j / (num_missing + 1)) * (x2 - x1)
                        interpolated_y = y1 + (j / (num_missing + 1)) * (y2 - y1)
                        
                        coords[start_idx + j] = [interpolated_x, interpolated_y]
            
            for anno in seg:
                if anno.atype == ANNOTATION_TYPE.EMPTY:
                    anno.to_atype(ANNOTATION_TYPE.START_BBOX)
                    anno.set_position(
                        QPointF(coords[seg.index(anno)][0], coords[seg.index(anno)][1]), 
                        GVar.BBOX_RADIUS
                        )
