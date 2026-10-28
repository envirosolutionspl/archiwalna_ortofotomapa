# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'archiwalna_ortofotomapa_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ArchiwalnaOrtofotomapaDockWidgetBase(object):
    def setupUi(self, ArchiwalnaOrtofotomapaDockWidgetBase):
        ArchiwalnaOrtofotomapaDockWidgetBase.setObjectName("ArchiwalnaOrtofotomapaDockWidgetBase")
        ArchiwalnaOrtofotomapaDockWidgetBase.resize(272, 187)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.lbl_pluginVersion = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_pluginVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_pluginVersion.setObjectName("lbl_pluginVersion")
        self.gridLayout.addWidget(self.lbl_pluginVersion, 14, 0, 1, 1)
        self.lbl_email = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_email.setTextFormat(QtCore.Qt.RichText)
        self.lbl_email.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_email.setOpenExternalLinks(True)
        self.lbl_email.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.lbl_email.setObjectName("lbl_email")
        self.gridLayout.addWidget(self.lbl_email, 19, 0, 1, 1)
        self.timeSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.timeSlider.setMaximum(2020)
        self.timeSlider.setSliderPosition(2020)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.timeSlider.setTickInterval(1)
        self.timeSlider.setObjectName("timeSlider")
        self.gridLayout.addWidget(self.timeSlider, 2, 0, 1, 1)
        self.timeLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_copyrights = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_copyrights.setTextFormat(QtCore.Qt.RichText)
        self.lbl_copyrights.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_copyrights.setOpenExternalLinks(True)
        self.lbl_copyrights.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.lbl_copyrights.setObjectName("lbl_copyrights")
        self.horizontalLayout_2.addWidget(self.lbl_copyrights)
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_5.setMaximumSize(QtCore.QSize(20, 20))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/plugins/archiwalna_ortofotomapa/icons/drzewiec.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.gridLayout.addLayout(self.horizontalLayout_2, 18, 0, 1, 1)
        ArchiwalnaOrtofotomapaDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(ArchiwalnaOrtofotomapaDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(ArchiwalnaOrtofotomapaDockWidgetBase)

    def retranslateUi(self, ArchiwalnaOrtofotomapaDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        ArchiwalnaOrtofotomapaDockWidgetBase.setWindowTitle(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "Archiwalna Ortofotomapa"))
        self.label_2.setText(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "Pasek Czasu"))
        self.lbl_pluginVersion.setText(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "Archiwalna Ortofotomapa 1.0"))
        self.lbl_email.setText(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "<a href=\"mailto:office@envirosolutions.pl\">office@envirosolutions.pl</a>"))
        self.timeLabel.setText(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "2020"))
        self.lbl_copyrights.setText(_translate("ArchiwalnaOrtofotomapaDockWidgetBase", "<html><head/><body><p>© 2020 <a href=\"http://www.envirosolutions.pl/\"><span style=\" text-decoration: underline; color:#0000ff;\">EnviroSolutions Sp. z o.o.</span></a></p></body></html>"))

