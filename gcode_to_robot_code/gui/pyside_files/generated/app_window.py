# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStatusBar,
    QTableView,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_GcodeToRobotCodeWindow(object):
    def setupUi(self, GcodeToRobotCodeWindow):
        if not GcodeToRobotCodeWindow.objectName():
            GcodeToRobotCodeWindow.setObjectName("GcodeToRobotCodeWindow")
        GcodeToRobotCodeWindow.resize(1362, 833)
        self.centralwidget = QWidget(GcodeToRobotCodeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.select_gcode_file_button = QPushButton(self.centralwidget)
        self.select_gcode_file_button.setObjectName("select_gcode_file_button")

        self.horizontalLayout_4.addWidget(self.select_gcode_file_button)

        self.gcode_filepath_lineedit = QLineEdit(self.centralwidget)
        self.gcode_filepath_lineedit.setObjectName("gcode_filepath_lineedit")

        self.horizontalLayout_4.addWidget(self.gcode_filepath_lineedit)

        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.read_gcode_button = QPushButton(self.centralwidget)
        self.read_gcode_button.setObjectName("read_gcode_button")

        self.verticalLayout_6.addWidget(self.read_gcode_button)

        self.optimize_straight_line_button = QPushButton(self.centralwidget)
        self.optimize_straight_line_button.setObjectName(
            "optimize_straight_line_button"
        )

        self.verticalLayout_6.addWidget(self.optimize_straight_line_button)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.module_name_label = QLabel(self.centralwidget)
        self.module_name_label.setObjectName("module_name_label")

        self.horizontalLayout_5.addWidget(self.module_name_label)

        self.module_name_lineedit = QLineEdit(self.centralwidget)
        self.module_name_lineedit.setObjectName("module_name_lineedit")

        self.horizontalLayout_5.addWidget(self.module_name_lineedit)

        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.procedure_name_label = QLabel(self.centralwidget)
        self.procedure_name_label.setObjectName("procedure_name_label")

        self.horizontalLayout_6.addWidget(self.procedure_name_label)

        self.procedure_name_lineedit = QLineEdit(self.centralwidget)
        self.procedure_name_lineedit.setObjectName("procedure_name_lineedit")

        self.horizontalLayout_6.addWidget(self.procedure_name_lineedit)

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.generate_abb_code_button = QPushButton(self.centralwidget)
        self.generate_abb_code_button.setObjectName("generate_abb_code_button")

        self.verticalLayout_6.addWidget(self.generate_abb_code_button)

        self.save_filepath_lineedit = QLineEdit(self.centralwidget)
        self.save_filepath_lineedit.setObjectName("save_filepath_lineedit")

        self.verticalLayout_6.addWidget(self.save_filepath_lineedit)

        self.save_module_button = QPushButton(self.centralwidget)
        self.save_module_button.setObjectName("save_module_button")

        self.verticalLayout_6.addWidget(self.save_module_button)

        self.plot_options_grid_layout = QGridLayout()
        self.plot_options_grid_layout.setSpacing(6)
        self.plot_options_grid_layout.setObjectName("plot_options_grid_layout")
        self.plot_options_grid_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.three_dimension_radio_button = QRadioButton(self.centralwidget)
        self.three_dimension_radio_button.setObjectName("three_dimension_radio_button")

        self.plot_options_grid_layout.addWidget(
            self.three_dimension_radio_button, 1, 2, 1, 1
        )

        self.projection_mode_label = QLabel(self.centralwidget)
        self.projection_mode_label.setObjectName("projection_mode_label")

        self.plot_options_grid_layout.addWidget(self.projection_mode_label, 0, 1, 1, 1)

        self.two_dimension_radio_button = QRadioButton(self.centralwidget)
        self.two_dimension_radio_button.setObjectName("two_dimension_radio_button")

        self.plot_options_grid_layout.addWidget(
            self.two_dimension_radio_button, 0, 2, 1, 1
        )

        self.plot_path_button = QPushButton(self.centralwidget)
        self.plot_path_button.setObjectName("plot_path_button")

        self.plot_options_grid_layout.addWidget(self.plot_path_button, 1, 1, 1, 1)

        self.verticalLayout_6.addLayout(self.plot_options_grid_layout)

        self.verticalLayout_3.addLayout(self.verticalLayout_6)

        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.toolpath_data_tab = QWidget()
        self.toolpath_data_tab.setObjectName("toolpath_data_tab")
        self.gridLayout_9 = QGridLayout(self.toolpath_data_tab)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.toolpath_data_table = QTableView(self.toolpath_data_tab)
        self.toolpath_data_table.setObjectName("toolpath_data_table")

        self.gridLayout_8.addWidget(self.toolpath_data_table, 0, 0, 1, 1)

        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.tabWidget.addTab(self.toolpath_data_tab, "")
        self.path_plot_tab = QWidget()
        self.path_plot_tab.setObjectName("path_plot_tab")
        self.gridLayout_5 = QGridLayout(self.path_plot_tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.path_plot_tab, "")
        self.robtargets_tab = QWidget()
        self.robtargets_tab.setObjectName("robtargets_tab")
        self.gridLayout_7 = QGridLayout(self.robtargets_tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.robtargets_text = QTextBrowser(self.robtargets_tab)
        self.robtargets_text.setObjectName("robtargets_text")
        self.robtargets_text.setLineWrapMode(QTextEdit.NoWrap)

        self.gridLayout_6.addWidget(self.robtargets_text, 0, 0, 1, 1)

        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.robtargets_tab, "")
        self.move_commands_tab = QWidget()
        self.move_commands_tab.setObjectName("move_commands_tab")
        self.gridLayout_10 = QGridLayout(self.move_commands_tab)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.move_commands_text = QTextBrowser(self.move_commands_tab)
        self.move_commands_text.setObjectName("move_commands_text")
        self.move_commands_text.setLineWrapMode(QTextEdit.NoWrap)

        self.gridLayout_2.addWidget(self.move_commands_text, 0, 0, 1, 1)

        self.gridLayout_10.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.move_commands_tab, "")
        self.module_preview_tab = QWidget()
        self.module_preview_tab.setObjectName("module_preview_tab")
        self.gridLayout_11 = QGridLayout(self.module_preview_tab)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.module_preview_text = QTextBrowser(self.module_preview_tab)
        self.module_preview_text.setObjectName("module_preview_text")
        self.module_preview_text.setLineWrapMode(QTextEdit.NoWrap)

        self.gridLayout_11.addWidget(self.module_preview_text, 0, 0, 1, 1)

        self.tabWidget.addTab(self.module_preview_tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        GcodeToRobotCodeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(GcodeToRobotCodeWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1362, 22))
        self.toolbar_file = QMenu(self.menubar)
        self.toolbar_file.setObjectName("toolbar_file")
        GcodeToRobotCodeWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(GcodeToRobotCodeWindow)
        self.statusbar.setObjectName("statusbar")
        GcodeToRobotCodeWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.toolbar_file.menuAction())

        self.retranslateUi(GcodeToRobotCodeWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(GcodeToRobotCodeWindow)

    # setupUi

    def retranslateUi(self, GcodeToRobotCodeWindow):
        GcodeToRobotCodeWindow.setWindowTitle(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "GCode To Robot Code by ZC", None
            )
        )
        self.select_gcode_file_button.setText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Select Gcode File", None
            )
        )
        self.gcode_filepath_lineedit.setPlaceholderText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Enter Gcode Filepath", None
            )
        )
        self.read_gcode_button.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Parse Gcode", None)
        )
        self.optimize_straight_line_button.setText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Optimize Straight Lines", None
            )
        )
        self.module_name_label.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Module Name: ", None)
        )
        self.procedure_name_label.setText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Procedure Name: ", None
            )
        )
        self.generate_abb_code_button.setText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Generate ABB RAPID", None
            )
        )
        self.save_filepath_lineedit.setPlaceholderText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Enter Save Filepath", None
            )
        )
        self.save_module_button.setText(
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Save ABB Module", None
            )
        )
        self.three_dimension_radio_button.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "3D", None)
        )
        self.projection_mode_label.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Plot Path", None)
        )
        self.two_dimension_radio_button.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "2D", None)
        )
        self.plot_path_button.setText(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Show Plot", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.toolpath_data_tab),
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Toolpath Data", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.path_plot_tab),
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Path Plot", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.robtargets_tab),
            QCoreApplication.translate("GcodeToRobotCodeWindow", "RobTargets", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.move_commands_tab),
            QCoreApplication.translate("GcodeToRobotCodeWindow", "Move Commands", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.module_preview_tab),
            QCoreApplication.translate(
                "GcodeToRobotCodeWindow", "Module Preview", None
            ),
        )
        self.toolbar_file.setTitle(
            QCoreApplication.translate("GcodeToRobotCodeWindow", "File", None)
        )

    # retranslateUi
