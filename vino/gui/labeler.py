# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labeler.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListView, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

from vino.logic.slicer import VideoSlicer
import vino.resources_rc

class Ui_Labeler(object):
    def setupUi(self, Labeler):
        if not Labeler.objectName():
            Labeler.setObjectName(u"Labeler")
        Labeler.resize(1218, 719)
        self.horizontalLayout_7 = QHBoxLayout(Labeler)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(Labeler)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.scan_list = QListView(Labeler)
        self.scan_list.setObjectName(u"scan_list")

        self.verticalLayout_2.addWidget(self.scan_list)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.interpolate_button = QToolButton(Labeler)
        self.interpolate_button.setObjectName(u"interpolate_button")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpolate_button.sizePolicy().hasHeightForWidth())
        self.interpolate_button.setSizePolicy(sizePolicy)
        self.interpolate_button.setMinimumSize(QSize(32, 32))
        icon = QIcon()
        icon.addFile(u":/icons/interpolate.png", QSize(), QIcon.Normal, QIcon.Off)
        self.interpolate_button.setIcon(icon)
        self.interpolate_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.interpolate_button)

        self.delete_button = QToolButton(Labeler)
        self.delete_button.setObjectName(u"delete_button")
        sizePolicy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy)
        self.delete_button.setMinimumSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addFile(u":/icons/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_button.setIcon(icon1)
        self.delete_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.delete_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(Labeler)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.radius_spin_box = QSpinBox(Labeler)
        self.radius_spin_box.setObjectName(u"radius_spin_box")
        self.radius_spin_box.setMaximum(400)
        self.radius_spin_box.setValue(112)

        self.horizontalLayout_3.addWidget(self.radius_spin_box)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(Labeler)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.depth_inputline = QLineEdit(Labeler)
        self.depth_inputline.setObjectName(u"depth_inputline")

        self.horizontalLayout_2.addWidget(self.depth_inputline)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Labeler)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.fps_inputline = QLineEdit(Labeler)
        self.fps_inputline.setObjectName(u"fps_inputline")

        self.horizontalLayout.addWidget(self.fps_inputline)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.save_button = QPushButton(Labeler)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout_2.addWidget(self.save_button)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.previous_button = QPushButton(Labeler)
        self.previous_button.setObjectName(u"previous_button")

        self.horizontalLayout_5.addWidget(self.previous_button)

        self.next_button = QPushButton(Labeler)
        self.next_button.setObjectName(u"next_button")

        self.horizontalLayout_5.addWidget(self.next_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(Labeler)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.progressBar = QProgressBar(Labeler)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_6.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.slicer = VideoSlicer(Labeler)
        self.slicer.setObjectName(u"slicer")

        self.verticalLayout.addWidget(self.slicer)

        self.frame_slider = QSlider(Labeler)
        self.frame_slider.setObjectName(u"frame_slider")
        self.frame_slider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.frame_slider)


        self.horizontalLayout_7.addLayout(self.verticalLayout)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 5)

        self.retranslateUi(Labeler)

        QMetaObject.connectSlotsByName(Labeler)
    # setupUi

    def retranslateUi(self, Labeler):
        Labeler.setWindowTitle(QCoreApplication.translate("Labeler", u"Video Labeler", None))
        self.label.setText(QCoreApplication.translate("Labeler", u"Scan list:", None))
        self.interpolate_button.setText(QCoreApplication.translate("Labeler", u"...", None))
        self.delete_button.setText(QCoreApplication.translate("Labeler", u"...", None))
        self.label_4.setText(QCoreApplication.translate("Labeler", u"Radius:", None))
        self.label_3.setText(QCoreApplication.translate("Labeler", u"Depth:", None))
        self.label_2.setText(QCoreApplication.translate("Labeler", u"FPS:", None))
        self.save_button.setText(QCoreApplication.translate("Labeler", u"Save", None))
        self.previous_button.setText(QCoreApplication.translate("Labeler", u"Previous", None))
        self.next_button.setText(QCoreApplication.translate("Labeler", u"Next", None))
        self.label_5.setText(QCoreApplication.translate("Labeler", u"Progress:", None))
    # retranslateUi

