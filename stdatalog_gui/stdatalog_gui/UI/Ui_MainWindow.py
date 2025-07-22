# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)
import stdatalog_gui.UI.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1102, 1062)
        MainWindow.setMinimumSize(QSize(0, 0))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        MainWindow.setPalette(palette)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/icons/ST16418_ST-Logo-Ico_3.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210, 210, 210);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
"QLineEdit {\n"
"	height: 25px;\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QLineEdit[text=\"\"]{\n"
"	color:rgb(90,90,90);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color: rgb(60,60,60);\n"
"	background-color: rgb(60, 60, 60);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(32, 178, 170);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-b"
                        "ottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(32, 178, 170);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-le"
                        "ft-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(27, 29, 35);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	"
                        "background-image: url(:/icons/icons/outline_check_white_18dp.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px rgb(27, 29, 35);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"	margin-top: 5px;\n"
"    margin-bottom: 5px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"QRadioButton::indicator:checked:hover {\n"
"    border: 3px solid rgb(68, 76, 91);\n"
"}\n"
"QRadioButton::indicator:unchecked {\n"
"    border: 3px solid rgb(27, 29, 35);\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:unchecked:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	"
                        "padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/icons/outline_arrow_bottom_white_18dp.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    b"
                        "ackground-color: rgb(32, 178, 170);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(32, 178, 170);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QScrollArea{\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(39, 44, 54)"
                        ";\n"
"}\n"
"\n"
"/* PROGRESS BAR */\n"
"QProgressBar {\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(32, 178, 170);\n"
"    margin: 4px;\n"
"    border-bottom-right-radius: 6px;\n"
"    border-bottom-left-radius: 6px;\n"
"    border-top-right-radius: 6px;\n"
"    border-top-left-radius: 6px;\n"
"}\n"
"\n"
"/* SPINBOX */\n"
"QSpinBox {\n"
"    color: rgb(255,255,255);\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding-left: 10px;\n"
"}\n"
"QSpinBox:hover {\n"
"    border: 2px solid rgb(58, 66, 81);\n"
"}\n"
"QSpinBox:focus {\n"
"    border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QSpinBox:disabled {\n"
"    color: rgb(60,60,60);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 16px;\n"
"    border: 1"
                        "px solid rgb(58, 66, 81);\n"
"}\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 16px;\n"
"    border: 1px solid rgb(58, 66, 81);\n"
"}\n"
"\n"
"QSpinBox::up-button:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSpinBox::down-button:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    image: url(:/icons/icons/outline_keyboard_arrow_up_white_18dp.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/icons/outline_keyboard_arrow_down_white_18dp.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QSpinBox::up-arrow:hover {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"QSpinBox::down-arrow:hover {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}")
        self.frame_main.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy1)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setMinimumSize(QSize(0, 0))
        self.frame_menus.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)
        self.menu_btn_connection = QPushButton(self.frame_menus)
        self.menu_btn_connection.setObjectName(u"menu_btn_connection")
        self.menu_btn_connection.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.menu_btn_connection.sizePolicy().hasHeightForWidth())
        self.menu_btn_connection.setSizePolicy(sizePolicy2)
        self.menu_btn_connection.setMinimumSize(QSize(0, 60))
        font1 = QFont()
        self.menu_btn_connection.setFont(font1)
        self.menu_btn_connection.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_btn_connection.setStyleSheet(u"QPushButton {	\n"
"	background-image: url(:/icons/icons/outline_settings_input_com_white_18dp.png);\n"
"	background-position: center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-right: 5px solid rgb(134, 26, 34);\n"
"	background-color: rgb(27, 29, 35);\n"
"	text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(32, 178, 170);\n"
"}")
        self.menu_btn_connection.setCheckable(False)

        self.layout_menus.addWidget(self.menu_btn_connection)

        self.menu_btn_device_conf = QPushButton(self.frame_menus)
        self.menu_btn_device_conf.setObjectName(u"menu_btn_device_conf")
        self.menu_btn_device_conf.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.menu_btn_device_conf.sizePolicy().hasHeightForWidth())
        self.menu_btn_device_conf.setSizePolicy(sizePolicy2)
        self.menu_btn_device_conf.setMinimumSize(QSize(0, 60))
        self.menu_btn_device_conf.setFont(font1)
        self.menu_btn_device_conf.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_btn_device_conf.setStyleSheet(u"QPushButton {	\n"
"	background-image: url(:/icons/icons/baseline_tune_white_18dp.png);\n"
"	background-position: center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"	text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(32, 178, 170);\n"
"}")

        self.layout_menus.addWidget(self.menu_btn_device_conf)

        self.menu_btn_experimental_features = QPushButton(self.frame_menus)
        self.menu_btn_experimental_features.setObjectName(u"menu_btn_experimental_features")
        self.menu_btn_experimental_features.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.menu_btn_experimental_features.sizePolicy().hasHeightForWidth())
        self.menu_btn_experimental_features.setSizePolicy(sizePolicy2)
        self.menu_btn_experimental_features.setMinimumSize(QSize(0, 60))
        self.menu_btn_experimental_features.setFont(font1)
        self.menu_btn_experimental_features.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_btn_experimental_features.setStyleSheet(u"QPushButton {	\n"
"	background-image: url(:/icons/icons/science_18dp_E8EAED.svg);\n"
"	background-position: center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"	text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(32, 178, 170);\n"
"}")

        self.layout_menus.addWidget(self.menu_btn_experimental_features)


        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy1.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy1)
        self.frame_extra_menus.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Shadow.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)
        self.menu_btn_about = QPushButton(self.frame_extra_menus)
        self.menu_btn_about.setObjectName(u"menu_btn_about")
        self.menu_btn_about.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.menu_btn_about.sizePolicy().hasHeightForWidth())
        self.menu_btn_about.setSizePolicy(sizePolicy2)
        self.menu_btn_about.setMinimumSize(QSize(0, 60))
        self.menu_btn_about.setFont(font1)
        self.menu_btn_about.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_btn_about.setStyleSheet(u"color: transparent;\n"
"border: none;\n"
"/*QPushButton {\n"
"	background-image: url(:/icons/icons/outline_info_white_18dp.png);\n"
"	background-position: center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"	text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(32, 178, 170);\n"
"}*/")

        self.layout_menu_bottom.addWidget(self.menu_btn_about)

        self.menu_btn_show_log_file = QPushButton(self.frame_extra_menus)
        self.menu_btn_show_log_file.setObjectName(u"menu_btn_show_log_file")
        self.menu_btn_show_log_file.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.menu_btn_show_log_file.sizePolicy().hasHeightForWidth())
        self.menu_btn_show_log_file.setSizePolicy(sizePolicy2)
        self.menu_btn_show_log_file.setMinimumSize(QSize(0, 60))
        self.menu_btn_show_log_file.setFont(font1)
        self.menu_btn_show_log_file.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_btn_show_log_file.setStyleSheet(u"QPushButton {	\n"
"	background-image: url(:/icons/icons/outline_description_white_18dp.png);\n"
"	background-position: center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"	text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(32, 178, 170);\n"
"}")

        self.layout_menu_bottom.addWidget(self.menu_btn_show_log_file)


        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        sizePolicy1.setHeightForWidth(self.frame_content.sizePolicy().hasHeightForWidth())
        self.frame_content.setSizePolicy(sizePolicy1)
        self.frame_content.setMinimumSize(QSize(0, 0))
        self.frame_content.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_content)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.stacked_widget = QStackedWidget(self.frame_content)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.stacked_widget.setMinimumSize(QSize(0, 0))
        self.stacked_widget.setStyleSheet(u"background: transparent;")
        self.page_connection = QWidget()
        self.page_connection.setObjectName(u"page_connection")
        self.page_connection_vlayout = QVBoxLayout(self.page_connection)
        self.page_connection_vlayout.setObjectName(u"page_connection_vlayout")
        self.additional_settings_frame = QFrame(self.page_connection)
        self.additional_settings_frame.setObjectName(u"additional_settings_frame")
        self.additional_settings_frame.setMinimumSize(QSize(0, 0))
        self.additional_settings_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.additional_settings_frame.setStyleSheet(u"QFrame {\n"
"	 border: transparent\n"
"}\n"
"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QLineEdit:disabled {\n"
"	background-color: rgb(36, 40, 48);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"QComboBox:disabled {\n"
"	background-color: rgb(36, 40, 48);\n"
"	border: 2px solid rgb(32"
                        ", 32, 32);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"")
        self.additional_settings_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.additional_settings_frame)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_log_file_options = QFrame(self.additional_settings_frame)
        self.frame_log_file_options.setObjectName(u"frame_log_file_options")
        self.frame_log_file_options.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_log_file_options.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_log_file_options)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_11.addWidget(self.frame_log_file_options, 0, Qt.AlignmentFlag.AlignRight)

        self.frame_dt_settings = QFrame(self.additional_settings_frame)
        self.frame_dt_settings.setObjectName(u"frame_dt_settings")
        self.frame_dt_settings.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_dt_settings.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_dt_settings)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.verticalLayout_11.addWidget(self.frame_dt_settings, 0, Qt.AlignmentFlag.AlignRight)


        self.page_connection_vlayout.addWidget(self.additional_settings_frame, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.page_connection_vlayout.addItem(self.verticalSpacer)

        self.frame_4 = QFrame(self.page_connection)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy3)
        self.frame_4.setMinimumSize(QSize(600, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 400))
        self.frame_4.setStyleSheet(u"border-radius: 5px;")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_4)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(24, 0, 24, 0)
        self.label_app_title = QLabel(self.frame_4)
        self.label_app_title.setObjectName(u"label_app_title")
        self.label_app_title.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(48)
        font2.setBold(True)
        self.label_app_title.setFont(font2)
        self.label_app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_app_title)


        self.page_connection_vlayout.addWidget(self.frame_4)

        self.stacked_widget.addWidget(self.page_connection)
        self.page_device_config = QWidget()
        self.page_device_config.setObjectName(u"page_device_config")
        self.page_device_config.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.page_device_config.sizePolicy().hasHeightForWidth())
        self.page_device_config.setSizePolicy(sizePolicy1)
        self.page_device_config.setMinimumSize(QSize(0, 0))
        self.verticalLayout_6 = QVBoxLayout(self.page_device_config)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_device_config = QFrame(self.page_device_config)
        self.frame_device_config.setObjectName(u"frame_device_config")
        self.frame_device_config.setEnabled(True)
        self.frame_device_config.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.frame_device_config)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_header = QWidget(self.frame_device_config)
        self.widget_header.setObjectName(u"widget_header")
        self.widget_header.setMinimumSize(QSize(0, 0))
        self.widget_header.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_header)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widget_header)

        self.splitter = QSplitter(self.frame_device_config)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.scrollArea_device_config = QScrollArea(self.splitter)
        self.scrollArea_device_config.setObjectName(u"scrollArea_device_config")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollArea_device_config.sizePolicy().hasHeightForWidth())
        self.scrollArea_device_config.setSizePolicy(sizePolicy4)
        self.scrollArea_device_config.setMinimumSize(QSize(500, 0))
        self.scrollArea_device_config.setMaximumSize(QSize(500, 16777215))
        self.scrollArea_device_config.setWidgetResizable(True)
        self.widget_device_config_main = QWidget()
        self.widget_device_config_main.setObjectName(u"widget_device_config_main")
        self.widget_device_config_main.setGeometry(QRect(0, 0, 496, 1003))
        self.verticalLayout_3 = QVBoxLayout(self.widget_device_config_main)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.widget_special_components = QWidget(self.widget_device_config_main)
        self.widget_special_components.setObjectName(u"widget_special_components")
        self.widget_special_components.setMinimumSize(QSize(0, 0))
        self.verticalLayout_13 = QVBoxLayout(self.widget_special_components)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.widget_special_components)

        self.line = QFrame(self.widget_device_config_main)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"color: rgb(27, 29, 35);")
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_3.addWidget(self.line)

        self.widget_device_config = QWidget(self.widget_device_config_main)
        self.widget_device_config.setObjectName(u"widget_device_config")
        self.widget_device_config.setMinimumSize(QSize(0, 0))
        self.verticalLayout_17 = QVBoxLayout(self.widget_device_config)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.select_all_frame = QFrame(self.widget_device_config)
        self.select_all_frame.setObjectName(u"select_all_frame")
        self.select_all_frame.setMinimumSize(QSize(0, 0))
        self.select_all_frame.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.select_all_frame.setStyleSheet(u"QFrame {\n"
"	 border: transparent\n"
"}\n"
"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QLineEdit:disabled {\n"
"	background-color: rgb(36, 40, 48);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"QComboBox:disabled {\n"
"	background-color: rgb(36, 40, 48);\n"
"	border: 2px solid rgb(32"
                        ", 32, 32);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"")
        self.select_all_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.select_all_frame)
        self.horizontalLayout_11.setSpacing(24)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 9, 9, 9)
        self.select_all_label = QLabel(self.select_all_frame)
        self.select_all_label.setObjectName(u"select_all_label")
        font3 = QFont()
        font3.setBold(True)
        self.select_all_label.setFont(font3)

        self.horizontalLayout_11.addWidget(self.select_all_label, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_17.addWidget(self.select_all_frame)


        self.verticalLayout_3.addWidget(self.widget_device_config)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.scrollArea_device_config.setWidget(self.widget_device_config_main)
        self.splitter.addWidget(self.scrollArea_device_config)
        self.scrollArea_plots = QScrollArea(self.splitter)
        self.scrollArea_plots.setObjectName(u"scrollArea_plots")
        self.scrollArea_plots.setWidgetResizable(True)
        self.widget_plots = QWidget()
        self.widget_plots.setObjectName(u"widget_plots")
        self.widget_plots.setGeometry(QRect(0, 0, 475, 1003))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_plots.sizePolicy().hasHeightForWidth())
        self.widget_plots.setSizePolicy(sizePolicy5)
        self.verticalLayout_7 = QVBoxLayout(self.widget_plots)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.scrollArea_plots.setWidget(self.widget_plots)
        self.splitter.addWidget(self.scrollArea_plots)

        self.verticalLayout_2.addWidget(self.splitter)


        self.verticalLayout_6.addWidget(self.frame_device_config)

        self.stacked_widget.addWidget(self.page_device_config)
        self.page_experimental_features = QWidget()
        self.page_experimental_features.setObjectName(u"page_experimental_features")
        self.verticalLayout_15 = QVBoxLayout(self.page_experimental_features)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label = QLabel(self.page_experimental_features)
        self.label.setObjectName(u"label")
        font4 = QFont()
        font4.setFamilies([u"Consolas"])
        self.label.setFont(font4)
        self.label.setStyleSheet(u"padding: 20;")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label.setWordWrap(True)

        self.verticalLayout_15.addWidget(self.label)

        self.tabWidget = QTabWidget(self.page_experimental_features)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::pane { /* The tab widget frame */\n"
"		border-top: 2px solid rgb(39, 44, 54);\n"
"        position: absolute;\n"
"    }\n"
"    QTabWidget::tab-bar {\n"
"        alignment: left;\n"
"    }\n"
"    QTabBar::tab {\n"
"        font: 700 12pt \"Segoe UI\";\n"
"        background-color: rgb(39, 44, 54);\n"
"		border-top: 2px solid rgb(39, 44, 54);\n"
"        border-top-left-radius: 4px;\n"
"        border-top-right-radius: 4px;\n"
"        min-width: 8ex;\n"
"		padding: 6px;\n"
"        padding-left: 12px;\n"
"		padding-right: 12px;\n"
"    }\n"
"    QTabBar::tab:selected, QTabBar::tab:hover {\n"
"       	background-color: rgb(57, 65, 80);\n"
"		border: 2px solid rgb(81, 81, 81);\n"
"		border-bottom: 2px solid rgb(57, 65, 80);\n"
"    }\n"
"    QTabBar::tab:selected {\n"
"		border: 2px solid rgb(81, 81, 81);\n"
"       	background-color: rgb(57, 65, 80);\n"
"		border-bottom: 2px solid rgb(57, 65, 80);\n"
"    }\n"
"    QTabBar::tab:!selected {\n"
"        margin-top: 2px; /* make non-selected tabs loo"
                        "k smaller */\n"
"    }\n"
"    QTabBar::tab:selected {\n"
"        /* expand/contract as needed */\n"
"        margin-left: -4px;\n"
"        margin-right: -4px;\n"
"    }\n"
"    QTabBar::tab:first:selected {\n"
"        margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"    }\n"
"    QTabBar::tab:last:selected {\n"
"        margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    }\n"
"    QTabBar::tab:only-one {\n"
"        margin: 0; /* if there is only one tab, we don't want overlapping margins */\n"
"    }")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.data_toolkit_tab = QWidget()
        self.data_toolkit_tab.setObjectName(u"data_toolkit_tab")
        self.verticalLayout_22 = QVBoxLayout(self.data_toolkit_tab)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_dt_settings = QScrollArea(self.data_toolkit_tab)
        self.scrollArea_dt_settings.setObjectName(u"scrollArea_dt_settings")
        sizePolicy1.setHeightForWidth(self.scrollArea_dt_settings.sizePolicy().hasHeightForWidth())
        self.scrollArea_dt_settings.setSizePolicy(sizePolicy1)
        self.scrollArea_dt_settings.setMinimumSize(QSize(0, 0))
        self.scrollArea_dt_settings.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea_dt_settings.setWidgetResizable(True)
        self.widget_data_toolkit = QWidget()
        self.widget_data_toolkit.setObjectName(u"widget_data_toolkit")
        self.widget_data_toolkit.setGeometry(QRect(0, 0, 980, 786))
        self.verticalLayout_16 = QVBoxLayout(self.widget_data_toolkit)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(3, 3, 3, 3)
        self.dt_settings_frame = QFrame(self.widget_data_toolkit)
        self.dt_settings_frame.setObjectName(u"dt_settings_frame")
        self.dt_settings_frame.setMinimumSize(QSize(300, 0))
        self.dt_settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.dt_settings_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.dt_settings_frame)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.dt_enabled_checkBox = QCheckBox(self.dt_settings_frame)
        self.dt_enabled_checkBox.setObjectName(u"dt_enabled_checkBox")
        self.dt_enabled_checkBox.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.dt_enabled_checkBox.sizePolicy().hasHeightForWidth())
        self.dt_enabled_checkBox.setSizePolicy(sizePolicy1)
        self.dt_enabled_checkBox.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"background-color: rgb(39, 44, 54);\n"
"padding: 9;")
        self.dt_enabled_checkBox.setChecked(False)

        self.verticalLayout_19.addWidget(self.dt_enabled_checkBox)

        self.dt_frame_content = QFrame(self.dt_settings_frame)
        self.dt_frame_content.setObjectName(u"dt_frame_content")
        self.dt_frame_content.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.dt_frame_content.sizePolicy().hasHeightForWidth())
        self.dt_frame_content.setSizePolicy(sizePolicy1)
        self.dt_frame_content.setStyleSheet(u"border-radius: 5px;")
        self.dt_frame_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.dt_frame_content.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.dt_frame_content)
        self.verticalLayout_20.setSpacing(6)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 9, 0, 0)
        self.groupBox_dt_settings = QGroupBox(self.dt_frame_content)
        self.groupBox_dt_settings.setObjectName(u"groupBox_dt_settings")
        self.groupBox_dt_settings.setMinimumSize(QSize(0, 0))
        self.groupBox_dt_settings.setStyleSheet(u"QGroupBox {\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_dt_settings.setFlat(False)
        self.groupBox_dt_settings.setCheckable(False)
        self.verticalLayout_43 = QVBoxLayout(self.groupBox_dt_settings)
        self.verticalLayout_43.setSpacing(6)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(6, 18, 6, 9)
        self.inner_dt_hframe = QFrame(self.groupBox_dt_settings)
        self.inner_dt_hframe.setObjectName(u"inner_dt_hframe")
        self.inner_dt_hframe.setMinimumSize(QSize(0, 0))
        self.inner_dt_hframe.setStyleSheet(u"")
        self.inner_dt_hframe.setFrameShape(QFrame.Shape.StyledPanel)
        self.inner_dt_hframe.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.inner_dt_hframe)
        self.horizontalLayout_38.setSpacing(9)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(2, 0, 2, 0)
        self.dt_plugins_folder_lineEdit = QLineEdit(self.inner_dt_hframe)
        self.dt_plugins_folder_lineEdit.setObjectName(u"dt_plugins_folder_lineEdit")
        self.dt_plugins_folder_lineEdit.setMinimumSize(QSize(0, 30))
        self.dt_plugins_folder_lineEdit.setMaximumSize(QSize(16777215, 30))
        self.dt_plugins_folder_lineEdit.setStyleSheet(u"QLineEdit {\n"
"	height: 25px;\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QLineEdit[text=\"\"]{\n"
"	color:rgb(90,90,90);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color: rgb(60,60,60);\n"
"	background-color: rgb(60, 60, 60);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}")

        self.horizontalLayout_38.addWidget(self.dt_plugins_folder_lineEdit)

        self.dt_plugins_folder_button = QPushButton(self.inner_dt_hframe)
        self.dt_plugins_folder_button.setObjectName(u"dt_plugins_folder_button")
        sizePolicy1.setHeightForWidth(self.dt_plugins_folder_button.sizePolicy().hasHeightForWidth())
        self.dt_plugins_folder_button.setSizePolicy(sizePolicy1)
        self.dt_plugins_folder_button.setMinimumSize(QSize(80, 45))
        self.dt_plugins_folder_button.setMaximumSize(QSize(16777215, 16777215))
        self.dt_plugins_folder_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/baseline_folder_open_white_18dp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dt_plugins_folder_button.setIcon(icon1)

        self.horizontalLayout_38.addWidget(self.dt_plugins_folder_button)


        self.verticalLayout_43.addWidget(self.inner_dt_hframe)


        self.verticalLayout_20.addWidget(self.groupBox_dt_settings)

        self.groupBox_dt_plugin_list = QGroupBox(self.dt_frame_content)
        self.groupBox_dt_plugin_list.setObjectName(u"groupBox_dt_plugin_list")
        self.groupBox_dt_plugin_list.setMinimumSize(QSize(0, 0))
        self.groupBox_dt_plugin_list.setStyleSheet(u"QGroupBox {\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_dt_plugin_list.setFlat(False)
        self.groupBox_dt_plugin_list.setCheckable(False)
        self.verticalLayout_51 = QVBoxLayout(self.groupBox_dt_plugin_list)
        self.verticalLayout_51.setSpacing(6)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_51.setContentsMargins(9, 18, 9, 9)
        self.dt_plugin_listWidget = QListWidget(self.groupBox_dt_plugin_list)
        self.dt_plugin_listWidget.setObjectName(u"dt_plugin_listWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.dt_plugin_listWidget.sizePolicy().hasHeightForWidth())
        self.dt_plugin_listWidget.setSizePolicy(sizePolicy6)
        self.dt_plugin_listWidget.setTabKeyNavigation(False)
        self.dt_plugin_listWidget.setProperty(u"showDropIndicator", False)
        self.dt_plugin_listWidget.setDragEnabled(False)
        self.dt_plugin_listWidget.setDragDropOverwriteMode(False)
        self.dt_plugin_listWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.dt_plugin_listWidget.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.dt_plugin_listWidget.setAlternatingRowColors(False)
        self.dt_plugin_listWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.dt_plugin_listWidget.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.dt_plugin_listWidget.setMovement(QListView.Movement.Static)
        self.dt_plugin_listWidget.setResizeMode(QListView.ResizeMode.Fixed)
        self.dt_plugin_listWidget.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout_51.addWidget(self.dt_plugin_listWidget)


        self.verticalLayout_20.addWidget(self.groupBox_dt_plugin_list)


        self.verticalLayout_19.addWidget(self.dt_frame_content)

        self.label_2 = QLabel(self.dt_settings_frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"padding: 20;")
        self.label_2.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label_2.setWordWrap(True)

        self.verticalLayout_19.addWidget(self.label_2)


        self.verticalLayout_16.addWidget(self.dt_settings_frame)

        self.scrollArea_dt_settings.setWidget(self.widget_data_toolkit)

        self.verticalLayout_22.addWidget(self.scrollArea_dt_settings)

        self.tabWidget.addTab(self.data_toolkit_tab, "")
        self.staiotcraft_tab = QWidget()
        self.staiotcraft_tab.setObjectName(u"staiotcraft_tab")
        self.verticalLayout_14 = QVBoxLayout(self.staiotcraft_tab)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_acq_upload = QScrollArea(self.staiotcraft_tab)
        self.scrollArea_acq_upload.setObjectName(u"scrollArea_acq_upload")
        sizePolicy1.setHeightForWidth(self.scrollArea_acq_upload.sizePolicy().hasHeightForWidth())
        self.scrollArea_acq_upload.setSizePolicy(sizePolicy1)
        self.scrollArea_acq_upload.setWidgetResizable(True)
        self.widget_acq_upload = QWidget()
        self.widget_acq_upload.setObjectName(u"widget_acq_upload")
        self.widget_acq_upload.setGeometry(QRect(0, 0, 980, 786))
        sizePolicy1.setHeightForWidth(self.widget_acq_upload.sizePolicy().hasHeightForWidth())
        self.widget_acq_upload.setSizePolicy(sizePolicy1)
        self.verticalLayout_24 = QVBoxLayout(self.widget_acq_upload)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(3, 3, 3, 3)
        self.acq_upload_frame = QFrame(self.widget_acq_upload)
        self.acq_upload_frame.setObjectName(u"acq_upload_frame")
        sizePolicy6.setHeightForWidth(self.acq_upload_frame.sizePolicy().hasHeightForWidth())
        self.acq_upload_frame.setSizePolicy(sizePolicy6)
        self.acq_upload_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.acq_upload_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.acq_upload_frame)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_prj_name = QFrame(self.acq_upload_frame)
        self.frame_prj_name.setObjectName(u"frame_prj_name")
        self.frame_prj_name.setMaximumSize(QSize(16777215, 16777215))
        self.frame_prj_name.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.frame_prj_name.setStyleSheet(u"QFrame {\n"
"	border: transparent;\n"
"	background-color: rgb(39, 44, 54);\n"
"}")
        self.frame_prj_name.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_prj_name.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_prj_name)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 0, 9, 0)
        self.upload_acquisition_checkBox = QCheckBox(self.frame_prj_name)
        self.upload_acquisition_checkBox.setObjectName(u"upload_acquisition_checkBox")
        self.upload_acquisition_checkBox.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.upload_acquisition_checkBox.sizePolicy().hasHeightForWidth())
        self.upload_acquisition_checkBox.setSizePolicy(sizePolicy1)
        self.upload_acquisition_checkBox.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"background-color: rgb(39, 44, 54);\n"
"padding: 9;")
        self.upload_acquisition_checkBox.setChecked(False)

        self.horizontalLayout_9.addWidget(self.upload_acquisition_checkBox)

        self.howto_button = QPushButton(self.frame_prj_name)
        self.howto_button.setObjectName(u"howto_button")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.howto_button.sizePolicy().hasHeightForWidth())
        self.howto_button.setSizePolicy(sizePolicy7)
        self.howto_button.setMinimumSize(QSize(80, 30))
        self.howto_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(255, 210, 0);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(255, 221, 64);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"	color: rgb(3, 35, 75);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(255, 232, 128);\n"
"	border: 2px solid rgb(255, 210, 0);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: (255, 210, 0);\n"
"	border: 2px solid rgb(255, 232, 128);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/lightbulb_18dp_03234B.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.howto_button.setIcon(icon2)

        self.horizontalLayout_9.addWidget(self.howto_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.login_button = QPushButton(self.frame_prj_name)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setEnabled(True)
        sizePolicy7.setHeightForWidth(self.login_button.sizePolicy().hasHeightForWidth())
        self.login_button.setSizePolicy(sizePolicy7)
        self.login_button.setMinimumSize(QSize(80, 30))
        self.login_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51, 71, 51);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(51, 71, 51);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 81, 57);\n"
"	border: 2px solid rgb(61, 87, 61);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(34, 48, 34);\n"
"	border: 2px solid rgb(42, 60, 42);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.horizontalLayout_9.addWidget(self.login_button)


        self.verticalLayout_18.addWidget(self.frame_prj_name)

        self.login_error_label = QLabel(self.acq_upload_frame)
        self.login_error_label.setObjectName(u"login_error_label")
        self.login_error_label.setStyleSheet(u"font: 700 11pt \"Consolas\";\n"
"color: red;")

        self.verticalLayout_18.addWidget(self.login_error_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.acq_upload_frame_content = QFrame(self.acq_upload_frame)
        self.acq_upload_frame_content.setObjectName(u"acq_upload_frame_content")
        sizePolicy1.setHeightForWidth(self.acq_upload_frame_content.sizePolicy().hasHeightForWidth())
        self.acq_upload_frame_content.setSizePolicy(sizePolicy1)
        self.acq_upload_frame_content.setStyleSheet(u"border-radius: 5px;")
        self.acq_upload_frame_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.acq_upload_frame_content.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.acq_upload_frame_content)
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.userLogin_frame = QFrame(self.acq_upload_frame_content)
        self.userLogin_frame.setObjectName(u"userLogin_frame")
        sizePolicy.setHeightForWidth(self.userLogin_frame.sizePolicy().hasHeightForWidth())
        self.userLogin_frame.setSizePolicy(sizePolicy)
        self.userLogin_frame.setMinimumSize(QSize(0, 0))
        self.userLogin_frame.setStyleSheet(u"")
        self.userLogin_frame.setFrameShape(QFrame.Shape.Panel)
        self.userLogin_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.userLogin_frame)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 9)
        self.groupBox_datasets_list = QGroupBox(self.userLogin_frame)
        self.groupBox_datasets_list.setObjectName(u"groupBox_datasets_list")
        sizePolicy6.setHeightForWidth(self.groupBox_datasets_list.sizePolicy().hasHeightForWidth())
        self.groupBox_datasets_list.setSizePolicy(sizePolicy6)
        self.groupBox_datasets_list.setMinimumSize(QSize(0, 0))
        self.groupBox_datasets_list.setStyleSheet(u"QGroupBox {\n"
"	border-radius: 5px;\n"
"    border: transparent;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_datasets_list.setFlat(False)
        self.groupBox_datasets_list.setCheckable(False)
        self.verticalLayout_50 = QVBoxLayout(self.groupBox_datasets_list)
        self.verticalLayout_50.setSpacing(6)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.verticalLayout_50.setContentsMargins(9, 9, 9, 9)
        self.label_3 = QLabel(self.groupBox_datasets_list)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)

        self.verticalLayout_50.addWidget(self.label_3)

        self.datasets_listWidget = QListWidget(self.groupBox_datasets_list)
        self.datasets_listWidget.setObjectName(u"datasets_listWidget")
        sizePolicy.setHeightForWidth(self.datasets_listWidget.sizePolicy().hasHeightForWidth())
        self.datasets_listWidget.setSizePolicy(sizePolicy)
        self.datasets_listWidget.setStyleSheet(u"")
        self.datasets_listWidget.setTabKeyNavigation(False)
        self.datasets_listWidget.setProperty(u"showDropIndicator", False)
        self.datasets_listWidget.setDragEnabled(False)
        self.datasets_listWidget.setDragDropOverwriteMode(False)
        self.datasets_listWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.datasets_listWidget.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.datasets_listWidget.setAlternatingRowColors(False)
        self.datasets_listWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.datasets_listWidget.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.datasets_listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.datasets_listWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.datasets_listWidget.setMovement(QListView.Movement.Static)
        self.datasets_listWidget.setProperty(u"isWrapping", False)
        self.datasets_listWidget.setResizeMode(QListView.ResizeMode.Fixed)
        self.datasets_listWidget.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout_50.addWidget(self.datasets_listWidget)


        self.verticalLayout_21.addWidget(self.groupBox_datasets_list)

        self.frame_new_dataset = QFrame(self.userLogin_frame)
        self.frame_new_dataset.setObjectName(u"frame_new_dataset")
        self.frame_new_dataset.setMinimumSize(QSize(0, 0))
        self.frame_new_dataset.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_new_dataset.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_new_dataset)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 9, 0, 0)
        self.create_new_dataset_button = QPushButton(self.frame_new_dataset)
        self.create_new_dataset_button.setObjectName(u"create_new_dataset_button")
        self.create_new_dataset_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.create_new_dataset_button.sizePolicy().hasHeightForWidth())
        self.create_new_dataset_button.setSizePolicy(sizePolicy1)
        self.create_new_dataset_button.setMinimumSize(QSize(0, 30))
        self.create_new_dataset_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51, 71, 51);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(51, 71, 51);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 81, 57);\n"
"	border: 2px solid rgb(61, 87, 61);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(34, 48, 34);\n"
"	border: 2px solid rgb(42, 60, 42);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")

        self.verticalLayout_25.addWidget(self.create_new_dataset_button)


        self.verticalLayout_21.addWidget(self.frame_new_dataset, 0, Qt.AlignmentFlag.AlignRight)


        self.horizontalLayout_10.addWidget(self.userLogin_frame)

        self.groupBox_base_acquisition_selection = QFrame(self.acq_upload_frame_content)
        self.groupBox_base_acquisition_selection.setObjectName(u"groupBox_base_acquisition_selection")
        self.groupBox_base_acquisition_selection.setEnabled(True)
        self.groupBox_base_acquisition_selection.setMinimumSize(QSize(0, 0))
        self.groupBox_base_acquisition_selection.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.groupBox_base_acquisition_selection.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"QComboBox:disabled{\n"
"	color: rgb(60,60,60);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}")
        self.groupBox_base_acquisition_selection.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.groupBox_base_acquisition_selection)
        self.horizontalLayout_34.setSpacing(3)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.groupBox_inner_base_acquisition_selection = QGroupBox(self.groupBox_base_acquisition_selection)
        self.groupBox_inner_base_acquisition_selection.setObjectName(u"groupBox_inner_base_acquisition_selection")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.groupBox_inner_base_acquisition_selection.sizePolicy().hasHeightForWidth())
        self.groupBox_inner_base_acquisition_selection.setSizePolicy(sizePolicy8)
        self.groupBox_inner_base_acquisition_selection.setMinimumSize(QSize(500, 0))
        self.groupBox_inner_base_acquisition_selection.setMaximumSize(QSize(500, 16777215))
        self.groupBox_inner_base_acquisition_selection.setStyleSheet(u"QGroupBox {\n"
"	background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center; /* position at the top left */\n"
"        padding: 6 3px;\n"
"        color: white;              /* Text color of the title */\n"
"    }\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_inner_base_acquisition_selection.setFlat(False)
        self.groupBox_inner_base_acquisition_selection.setCheckable(False)
        self.verticalLayout_41 = QVBoxLayout(self.groupBox_inner_base_acquisition_selection)
        self.verticalLayout_41.setSpacing(9)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(9, 24, 9, 9)
        self.inner_hframe = QFrame(self.groupBox_inner_base_acquisition_selection)
        self.inner_hframe.setObjectName(u"inner_hframe")
        sizePolicy3.setHeightForWidth(self.inner_hframe.sizePolicy().hasHeightForWidth())
        self.inner_hframe.setSizePolicy(sizePolicy3)
        self.inner_hframe.setMinimumSize(QSize(0, 0))
        self.inner_hframe.setStyleSheet(u"")
        self.inner_hframe.setFrameShape(QFrame.Shape.StyledPanel)
        self.inner_hframe.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.inner_hframe)
        self.horizontalLayout_36.setSpacing(9)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(2, 0, 2, 0)
        self.base_acq_folder_textEdit = QLineEdit(self.inner_hframe)
        self.base_acq_folder_textEdit.setObjectName(u"base_acq_folder_textEdit")
        self.base_acq_folder_textEdit.setMinimumSize(QSize(0, 30))
        self.base_acq_folder_textEdit.setMaximumSize(QSize(16777215, 30))
        self.base_acq_folder_textEdit.setStyleSheet(u"QLineEdit {\n"
"	height: 25px;\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"QLineEdit[text=\"\"]{\n"
"	color:rgb(90,90,90);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color: rgb(60,60,60);\n"
"	background-color: rgb(60, 60, 60);\n"
"	border: 2px solid rgb(32, 32, 32);\n"
"}")

        self.horizontalLayout_36.addWidget(self.base_acq_folder_textEdit)

        self.base_acq_folder_button = QPushButton(self.inner_hframe)
        self.base_acq_folder_button.setObjectName(u"base_acq_folder_button")
        self.base_acq_folder_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.base_acq_folder_button.sizePolicy().hasHeightForWidth())
        self.base_acq_folder_button.setSizePolicy(sizePolicy1)
        self.base_acq_folder_button.setMinimumSize(QSize(80, 45))
        self.base_acq_folder_button.setMaximumSize(QSize(16777215, 16777215))
        self.base_acq_folder_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"	font: 700 9pt \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.base_acq_folder_button.setIcon(icon1)

        self.horizontalLayout_36.addWidget(self.base_acq_folder_button)


        self.verticalLayout_41.addWidget(self.inner_hframe)

        self.groupBox_acquisitions_list = QGroupBox(self.groupBox_inner_base_acquisition_selection)
        self.groupBox_acquisitions_list.setObjectName(u"groupBox_acquisitions_list")
        sizePolicy1.setHeightForWidth(self.groupBox_acquisitions_list.sizePolicy().hasHeightForWidth())
        self.groupBox_acquisitions_list.setSizePolicy(sizePolicy1)
        self.groupBox_acquisitions_list.setMinimumSize(QSize(0, 0))
        self.groupBox_acquisitions_list.setStyleSheet(u"QGroupBox {\n"
"	border-radius: 5px;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top left; /* position at the top left */\n"
"        margin: 6 6 3px;\n"
"        color: white;              /* Text color of the title */\n"
"    }\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_acquisitions_list.setFlat(False)
        self.groupBox_acquisitions_list.setCheckable(False)
        self.verticalLayout_47 = QVBoxLayout(self.groupBox_acquisitions_list)
        self.verticalLayout_47.setSpacing(6)
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(9, 9, 9, 9)
        self.label_4 = QLabel(self.groupBox_acquisitions_list)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)

        self.verticalLayout_47.addWidget(self.label_4)

        self.acquisitions_listWidget = QListWidget(self.groupBox_acquisitions_list)
        self.acquisitions_listWidget.setObjectName(u"acquisitions_listWidget")
        sizePolicy.setHeightForWidth(self.acquisitions_listWidget.sizePolicy().hasHeightForWidth())
        self.acquisitions_listWidget.setSizePolicy(sizePolicy)
        self.acquisitions_listWidget.setStyleSheet(u"QListWidget::item:hover {\n"
"	border-radius: 5px;\n"
"	background-color: (255, 210, 0);\n"
"	border: 2px solid rgb(255, 232, 128);\n"
"}")
        self.acquisitions_listWidget.setTabKeyNavigation(False)
        self.acquisitions_listWidget.setProperty(u"showDropIndicator", False)
        self.acquisitions_listWidget.setDragEnabled(False)
        self.acquisitions_listWidget.setDragDropOverwriteMode(False)
        self.acquisitions_listWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.acquisitions_listWidget.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.acquisitions_listWidget.setAlternatingRowColors(False)
        self.acquisitions_listWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.acquisitions_listWidget.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.acquisitions_listWidget.setMovement(QListView.Movement.Static)
        self.acquisitions_listWidget.setResizeMode(QListView.ResizeMode.Fixed)
        self.acquisitions_listWidget.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout_47.addWidget(self.acquisitions_listWidget)


        self.verticalLayout_41.addWidget(self.groupBox_acquisitions_list)


        self.horizontalLayout_34.addWidget(self.groupBox_inner_base_acquisition_selection)


        self.horizontalLayout_10.addWidget(self.groupBox_base_acquisition_selection)


        self.verticalLayout_18.addWidget(self.acq_upload_frame_content)


        self.verticalLayout_24.addWidget(self.acq_upload_frame)

        self.groupBox_upload_settings = QGroupBox(self.widget_acq_upload)
        self.groupBox_upload_settings.setObjectName(u"groupBox_upload_settings")
        self.groupBox_upload_settings.setMinimumSize(QSize(0, 0))
        self.groupBox_upload_settings.setStyleSheet(u"QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center; /* position at the top center */\n"
"        padding: 6 3px;\n"
"        color: white;              /* Text color of the title */\n"
"    }\n"
"\n"
"QGroupBox {\n"
"	border-radius: 5px;\n"
"	background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}")
        self.groupBox_upload_settings.setFlat(False)
        self.groupBox_upload_settings.setCheckable(False)
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_upload_settings)
        self.verticalLayout_23.setSpacing(6)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(9, 24, 9, 18)
        self.acq_upload_error_label = QLabel(self.groupBox_upload_settings)
        self.acq_upload_error_label.setObjectName(u"acq_upload_error_label")
        self.acq_upload_error_label.setStyleSheet(u"font: 700 11pt \"Consolas\";\n"
"color: red;")

        self.verticalLayout_23.addWidget(self.acq_upload_error_label)

        self.upload_acquisition_button = QPushButton(self.groupBox_upload_settings)
        self.upload_acquisition_button.setObjectName(u"upload_acquisition_button")
        self.upload_acquisition_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.upload_acquisition_button.sizePolicy().hasHeightForWidth())
        self.upload_acquisition_button.setSizePolicy(sizePolicy1)
        self.upload_acquisition_button.setMinimumSize(QSize(80, 45))
        self.upload_acquisition_button.setMaximumSize(QSize(16777215, 30))
#if QT_CONFIG(tooltip)
        self.upload_acquisition_button.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.upload_acquisition_button.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51, 71, 51);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(51, 71, 51);\n"
"	font: 700 12pt \"Segoe UI\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 81, 57);\n"
"	border: 2px solid rgb(61, 87, 61);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(34, 48, 34);\n"
"	border: 2px solid rgb(42, 60, 42);\n"
"}\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/outline_cloud_upload_white_18dp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.upload_acquisition_button.setIcon(icon3)

        self.verticalLayout_23.addWidget(self.upload_acquisition_button)


        self.verticalLayout_24.addWidget(self.groupBox_upload_settings)

        self.scrollArea_acq_upload.setWidget(self.widget_acq_upload)

        self.verticalLayout_14.addWidget(self.scrollArea_acq_upload)

        self.tabWidget.addTab(self.staiotcraft_tab, "")

        self.verticalLayout_15.addWidget(self.tabWidget)

        self.stacked_widget.addWidget(self.page_experimental_features)
        self.page_app_log_file = QWidget()
        self.page_app_log_file.setObjectName(u"page_app_log_file")
        self.verticalLayout_10 = QVBoxLayout(self.page_app_log_file)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame = QFrame(self.page_app_log_file)
        self.frame.setObjectName(u"frame")
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setStyleSheet(u"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.log_file_title = QLabel(self.frame)
        self.log_file_title.setObjectName(u"log_file_title")
        self.log_file_title.setMinimumSize(QSize(0, 0))
        self.log_file_title.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"background-color: rgb(39, 44, 54);")
        self.log_file_title.setMargin(9)
        self.log_file_title.setIndent(3)

        self.verticalLayout_8.addWidget(self.log_file_title)

        self.log_file_textEdit = QTextEdit(self.frame)
        self.log_file_textEdit.setObjectName(u"log_file_textEdit")
        self.log_file_textEdit.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.log_file_textEdit)


        self.verticalLayout_10.addWidget(self.frame)

        self.stacked_widget.addWidget(self.page_app_log_file)

        self.verticalLayout_9.addWidget(self.stacked_widget)


        self.verticalLayout_4.addWidget(self.frame_content)

        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font1)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")

        self.horizontalLayout_7.addWidget(self.label_credits)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        self.label_version.setFont(font1)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_version)


        self.horizontalLayout_6.addWidget(self.frame_label_bottom)


        self.verticalLayout_4.addWidget(self.frame_grip)


        self.horizontalLayout_2.addWidget(self.frame_content_right)


        self.verticalLayout.addWidget(self.frame_center)


        self.horizontalLayout.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stacked_widget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ST DTDL GUI", None))
        self.menu_btn_connection.setText("")
        self.menu_btn_device_conf.setText("")
#if QT_CONFIG(tooltip)
        self.menu_btn_experimental_features.setToolTip(QCoreApplication.translate("MainWindow", u"Experimental Features", None))
#endif // QT_CONFIG(tooltip)
        self.menu_btn_experimental_features.setText("")
        self.menu_btn_about.setText("")
#if QT_CONFIG(tooltip)
        self.menu_btn_show_log_file.setToolTip(QCoreApplication.translate("MainWindow", u"Show Application Log File", None))
#endif // QT_CONFIG(tooltip)
        self.menu_btn_show_log_file.setText("")
        self.label_app_title.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.select_all_label.setText(QCoreApplication.translate("MainWindow", u"Select all:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24px; color:#ffffff;\">Welcome to the<br/></span><span style=\" font-size:36px; font-weight:700; color:#ffffff;\">Experimental Features page<br/></span><span style=\" font-size:14pt; color:#ffffff;\">Here, you can explore and activate new functionalities that are currently in development, giving you an exclusive preview of upcoming innovations and enhancements</span></p></body></html>", None))
        self.dt_enabled_checkBox.setText(QCoreApplication.translate("MainWindow", u"Data Toolkit *", None))
        self.groupBox_dt_settings.setTitle(QCoreApplication.translate("MainWindow", u"Data Toolkit plugins folder", None))
        self.dt_plugins_folder_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.groupBox_dt_plugin_list.setTitle(QCoreApplication.translate("MainWindow", u"Selected Plugins List", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">*</span>By enabling this feature, the data streams acquired from the sensors of a connected board pass through a data pipeline composed of a series of plugins. Along with the PythonSDK, in the examples folder, we provide a folder named <span style=\" font-weight:700; text-decoration: underline;\">data_toolkit_plugins</span> that contains three example plugins. Each plugin must implement a function named <span style=\" font-weight:700;\">process</span>, which processes the data received from the previous plugin and passes it to the next plugin. Additionally, each plugin can implement a function named <span style=\" font-weight:700;\">create_plot_widget</span>, which should return a QWidget that is automatically inserted into a dedicated section of this GUI (on the acquisition management page).</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_toolkit_tab), QCoreApplication.translate("MainWindow", u"Data Toolkit", None))
        self.upload_acquisition_checkBox.setText(QCoreApplication.translate("MainWindow", u"ST AIoT Craft Acquisitions upload", None))
        self.howto_button.setText(QCoreApplication.translate("MainWindow", u"HOW-TO", None))
        self.login_button.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.login_error_label.setText(QCoreApplication.translate("MainWindow", u"Error label", None))
        self.groupBox_datasets_list.setTitle("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"My Datasets", None))
        self.create_new_dataset_button.setText(QCoreApplication.translate("MainWindow", u"Create new Dataset", None))
        self.groupBox_inner_base_acquisition_selection.setTitle(QCoreApplication.translate("MainWindow", u"Acquisitions Base Folder", None))
        self.base_acq_folder_textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select a folder containing valid HSDatalog acquisitions folders", None))
        self.base_acq_folder_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.groupBox_acquisitions_list.setTitle("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Acquisitions List", None))
        self.groupBox_upload_settings.setTitle(QCoreApplication.translate("MainWindow", u"The following button will be enabled only once a Dataset and at least one Acquisition Folder are selected.", None))
        self.acq_upload_error_label.setText(QCoreApplication.translate("MainWindow", u"Error label", None))
        self.upload_acquisition_button.setText(QCoreApplication.translate("MainWindow", u" Upload Acquisitions", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.staiotcraft_tab), QCoreApplication.translate("MainWindow", u"ST AIoT Craft - Acquisitions Upload", None))
        self.log_file_title.setText(QCoreApplication.translate("MainWindow", u"Log file Title:", None))
        self.label_credits.setText(QCoreApplication.translate("MainWindow", u"ST DTDL GUI v1.0.0", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

