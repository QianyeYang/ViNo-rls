from PySide6.QtCore import QObject, Signal, Qt, Slot
from PySide6.QtCore import QPointF

class globalSignal(QObject):

    videoFrameIndexChanged = Signal(int)
    videoFrameIndexMoveForward = Signal()
    videoFrameIndexMoveBackward = Signal()
    saveRequested = Signal()
    annotationPostionUpdateRequest = Signal(int, int, QPointF, int)
    annotationIndexUpdateRequest = Signal(int)
    annotationBBoxRadiusUpdateRequest = Signal(int)
    updateDisplayRequest = Signal()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(globalSignal, cls).__new__(cls, *args, **kwargs)
        return cls._instance

gSignal = globalSignal()