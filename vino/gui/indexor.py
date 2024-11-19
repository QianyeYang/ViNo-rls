# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'indexor.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Indexor(object):
    def setupUi(self, Indexor):
        if not Indexor.objectName():
            Indexor.setObjectName(u"Indexor")
        Indexor.resize(429, 237)
        self.verticalLayout = QVBoxLayout(Indexor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Indexor)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.csv_combobox = QComboBox(Indexor)
        self.csv_combobox.setObjectName(u"csv_combobox")

        self.verticalLayout.addWidget(self.csv_combobox)

        self.label_2 = QLabel(Indexor)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.path_label = QLabel(Indexor)
        self.path_label.setObjectName(u"path_label")

        self.verticalLayout.addWidget(self.path_label)

        self.select_folder_button = QPushButton(Indexor)
        self.select_folder_button.setObjectName(u"select_folder_button")

        self.verticalLayout.addWidget(self.select_folder_button)

        self.line = QFrame(Indexor)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.start_button = QPushButton(Indexor)
        self.start_button.setObjectName(u"start_button")

        self.verticalLayout.addWidget(self.start_button)

        self.progress = QProgressBar(Indexor)
        self.progress.setObjectName(u"progress")
        self.progress.setValue(0)

        self.verticalLayout.addWidget(self.progress)


        self.retranslateUi(Indexor)

        QMetaObject.connectSlotsByName(Indexor)
    # setupUi

    def retranslateUi(self, Indexor):
        Indexor.setWindowTitle(QCoreApplication.translate("Indexor", u"Indexor", None))
        self.label.setText(QCoreApplication.translate("Indexor", u"Choose CSV index file:", None))
        self.label_2.setText(QCoreApplication.translate("Indexor", u"Choose data root:", None))
        self.path_label.setText(QCoreApplication.translate("Indexor", u"Selected path........", None))
        self.select_folder_button.setText(QCoreApplication.translate("Indexor", u"Select Folder", None))
        self.start_button.setText(QCoreApplication.translate("Indexor", u"Start", None))
    # retranslateUi

