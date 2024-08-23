# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        if not mainwindow.objectName():
            mainwindow.setObjectName(u"mainwindow")
        mainwindow.resize(300, 600)
        mainwindow.setMinimumSize(QSize(300, 600))
        mainwindow.setMaximumSize(QSize(300, 600))
        palette = QPalette()
        mainwindow.setPalette(palette)
        icon = QIcon()
        icon.addFile(u":/assets/empty.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        mainwindow.setWindowIcon(icon)
        mainwindow.setAutoFillBackground(True)
        mainwindow.setStyleSheet(u"/* Start and Resume buttons */\n"
"QPushButton#btn_start,\n"
"QPushButton#btn_resume{\n"
"	background-color: #1b381e;\n"
"	color: #6dba75;\n"
"	border: 2px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#btn_start:hover,\n"
"QPushButton#btn_resume:hover{\n"
"	background-color: #2c5531;\n"
"}\n"
"\n"
"\n"
"/* Lap button */\n"
"QPushButton#btn_lap{\n"
"	background-color: #332002;\n"
"	color: #ea9209;\n"
"	border: 2px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#btn_lap:hover{\n"
"	background-color: #4a3006;\n"
"}\n"
"\n"
"QPushButton#btn_lap:disabled{\n"
"	color: #bdbdbd;\n"
"	background-color: #333333;\n"
"}\n"
"\n"
"/* Reset button */\n"
"QPushButton[text=Reset]{\n"
"	background-color: #332002;\n"
"	color: #ea9209;\n"
"	border: 2px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton[text=Reset]:hover{\n"
"	background-color: #4a3006;\n"
"}\n"
"\n"
"/* Stop button */\n"
"QPushButton[text=Stop]{\n"
"	background-color: #331412;\n"
"	color: #e5423d"
                        ";\n"
"	border: 2px solid transparent;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton[text=Stop]:hover{\n"
"	background-color: #451e1c;\n"
"}\n"
"\n"
"/* Clock */\n"
"QFrame#frm_clock{\n"
"	image: url(:/assets/clock_project.png);\n"
"}\n"
"\n"
"/* Clock handle */\n"
"QLabel#lbl_clock_handle{\n"
"background-color: transparent\n"
"}\n"
"\n"
"\n"
"/* time label */\n"
"QLabel#lbl_time{\n"
"	color: #ff0000;\n"
"}\n"
"\n"
"QPushButton[text=Stop]:hover{\n"
"	background-color: #451e1c;\n"
"}\n"
"\n"
"/*Widgets background*/\n"
"QFrame{\n"
"	background-color: black\n"
"}\n"
"QWidget#scrollAreaWidgetContents{\n"
"	background-color: black\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(mainwindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.frm_clock = QFrame(mainwindow)
        self.frm_clock.setObjectName(u"frm_clock")
        self.frm_clock.setFrameShape(QFrame.Shape.NoFrame)
        self.frm_clock.setFrameShadow(QFrame.Shadow.Plain)
        self.frm_clock.setLineWidth(0)
        self.lbl_time = QLabel(self.frm_clock)
        self.lbl_time.setObjectName(u"lbl_time")
        self.lbl_time.setGeometry(QRect(84, 180, 121, 51))
        font = QFont()
        font.setFamilies([u"JetBrains Mono"])
        font.setPointSize(24)
        font.setBold(True)
        self.lbl_time.setFont(font)
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_clock_handle = QLabel(self.frm_clock)
        self.lbl_clock_handle.setObjectName(u"lbl_clock_handle")
        self.lbl_clock_handle.setGeometry(QRect(47, 49, 200, 200))

        self.verticalLayout.addWidget(self.frm_clock)

        self.frm_buttons = QFrame(mainwindow)
        self.frm_buttons.setObjectName(u"frm_buttons")
        self.frm_buttons.setAutoFillBackground(False)
        self.frm_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frm_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frm_buttons)
        self.horizontalLayout.setSpacing(18)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.stacked_widget_left = QStackedWidget(self.frm_buttons)
        self.stacked_widget_left.setObjectName(u"stacked_widget_left")
        palette1 = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.stacked_widget_left.setPalette(palette1)
        self.stacked_widget_left.setAutoFillBackground(False)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_lap = QPushButton(self.page)
        self.btn_lap.setObjectName(u"btn_lap")
        self.btn_lap.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_lap.sizePolicy().hasHeightForWidth())
        self.btn_lap.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Helvetica"])
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        font1.setHintingPreference(QFont.PreferNoHinting)
        self.btn_lap.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_lap)

        self.stacked_widget_left.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_reset = QPushButton(self.page_2)
        self.btn_reset.setObjectName(u"btn_reset")
        sizePolicy.setHeightForWidth(self.btn_reset.sizePolicy().hasHeightForWidth())
        self.btn_reset.setSizePolicy(sizePolicy)
        self.btn_reset.setFont(font1)

        self.verticalLayout_5.addWidget(self.btn_reset)

        self.stacked_widget_left.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stacked_widget_left)

        self.stacked_widget_right = QStackedWidget(self.frm_buttons)
        self.stacked_widget_right.setObjectName(u"stacked_widget_right")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_4 = QVBoxLayout(self.page_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_start = QPushButton(self.page_3)
        self.btn_start.setObjectName(u"btn_start")
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setFont(font1)

        self.verticalLayout_4.addWidget(self.btn_start)

        self.stacked_widget_right.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_6 = QVBoxLayout(self.page_4)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.btn_resume = QPushButton(self.page_4)
        self.btn_resume.setObjectName(u"btn_resume")
        sizePolicy.setHeightForWidth(self.btn_resume.sizePolicy().hasHeightForWidth())
        self.btn_resume.setSizePolicy(sizePolicy)
        self.btn_resume.setFont(font1)

        self.verticalLayout_6.addWidget(self.btn_resume)

        self.stacked_widget_right.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_7 = QVBoxLayout(self.page_5)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.btn_stop = QPushButton(self.page_5)
        self.btn_stop.setObjectName(u"btn_stop")
        sizePolicy.setHeightForWidth(self.btn_stop.sizePolicy().hasHeightForWidth())
        self.btn_stop.setSizePolicy(sizePolicy)
        self.btn_stop.setFont(font1)

        self.verticalLayout_7.addWidget(self.btn_stop)

        self.stacked_widget_right.addWidget(self.page_5)

        self.horizontalLayout.addWidget(self.stacked_widget_right)


        self.verticalLayout.addWidget(self.frm_buttons)

        self.frm_laps = QFrame(mainwindow)
        self.frm_laps.setObjectName(u"frm_laps")
        self.frm_laps.setFrameShape(QFrame.Shape.StyledPanel)
        self.frm_laps.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frm_laps)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.frm_laps)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 286, 236))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.verticalLayout.addWidget(self.frm_laps)

        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 4)

        self.retranslateUi(mainwindow)

        self.stacked_widget_left.setCurrentIndex(1)
        self.stacked_widget_right.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(mainwindow)
    # setupUi

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle("")
        self.lbl_time.setText(QCoreApplication.translate("mainwindow", u"00.00", None))
        self.lbl_clock_handle.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.btn_lap.setText(QCoreApplication.translate("mainwindow", u"Lap", None))
        self.btn_reset.setText(QCoreApplication.translate("mainwindow", u"Reset", None))
        self.btn_start.setText(QCoreApplication.translate("mainwindow", u"Start", None))
        self.btn_resume.setText(QCoreApplication.translate("mainwindow", u"Resume", None))
        self.btn_stop.setText(QCoreApplication.translate("mainwindow", u"Stop", None))
    # retranslateUi

