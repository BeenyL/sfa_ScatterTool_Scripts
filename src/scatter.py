import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.OpenMaya as om
import random
from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance



def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter UI")
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)
        self.setMinimumHeight(200)
        self.setMaximumHeight(400)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.defaultSubDiv = DefaultSubDiv()
        self.create_ui()
        self.create_connections()


    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: Bold 20px")
        self.create_obj_lay = self.create_obj_layout_ui()
        self.sct_cnl_lay = self.sct_cnl_layout_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.create_obj_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.sct_cnl_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_object)
        self.cancel_btn.clicked.connect(self.cancel)
        self.shape_btn.clicked.connect(self.create_shape)
        self.sub_ax_sbx.valueChanged.connect(self.update_sub_val_ax)
        self.sub_hgt_sbx.valueChanged.connect(self.update_sub_val_hgt)
        self.sub_bas_sbx.valueChanged.connect(self.update_sub_val_bas)
        self.shape_cmb.currentIndexChanged.connect(self.update_div)

    def update_sub_val_ax(self):
        self.defaultSubDiv.cur_sub_ax = self.sub_ax_sbx.value()

    def update_sub_val_hgt(self):
        self.defaultSubDiv.cur_sub_hgt = self.sub_hgt_sbx.value()

    def update_sub_val_bas(self):
        self.defaultSubDiv.cur_sub_bas = self.sub_bas_sbx.value()

    @QtCore.Slot()
    def create_shape(self):
        if self.shape_cmb.currentText() == "Cube":
            cmds.polyCube(name="Cube",
                          sw=self.defaultSubDiv.cur_sub_ax,
                          sh=self.defaultSubDiv.cur_sub_hgt,
                          sd=self.defaultSubDiv.cur_sub_bas)
        if self.shape_cmb.currentText() == "Sphere":
            cmds.polySphere(name="Sphere",
                            sa=self.defaultSubDiv.cur_sub_ax,
                            sh=self.defaultSubDiv.cur_sub_hgt)
        if self.shape_cmb.currentText() == "Cylinder":
            cmds.polyCylinder(name="Cylinder",
                              sa=self.defaultSubDiv.cur_sub_ax,
                              sh=self.defaultSubDiv.cur_sub_hgt,
                              sc=self.defaultSubDiv.cur_sub_bas)
        if self.shape_cmb.currentText() == "Cone":
            cmds.polyCone(name="Cone",
                          sa=self.defaultSubDiv.cur_sub_ax,
                          sh=self.defaultSubDiv.cur_sub_hgt,
                          sc=self.defaultSubDiv.cur_sub_bas)

    @QtCore.Slot()
    def scatter_object(self):
        """scatter an Object"""
        vertList = cmds.ls(selection=True, fl=True)
        scatter_grp = cmds.group(n='scatter_grp')
        object_to_instance = vertList[0]
        if cmds.objectType(object_to_instance) == 'transform':

            for vert in vertList:
                vertexPos = cmds.xform(vert, q=True, ws=True, t=True)
                new_instance = cmds.instance(object_to_instance)

                cmds.move(vertexPos[0], vertexPos[1], vertexPos[2],
                          new_instance)

                cmds.rotate(vertexPos[0], vertexPos[1], vertexPos[2],
                            new_instance, relative=True, objectSpace=True)

                cmds.scale(vertexPos[0], vertexPos[1], vertexPos[2],
                          new_instance, relative=True)

    @QtCore.Slot()
    def update_div(self):
        """update subdivision"""
        if self.shape_cmb.currentText() == "Cube":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cb_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cb_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cb_sub_bas
        if self.shape_cmb.currentText() == "Sphere":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.s_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.s_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.s_sub_bas
        if self.shape_cmb.currentText() == "Cylinder":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cyl_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cyl_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cyl_sub_bas
        if self.shape_cmb.currentText() == "Cone":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cn_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cn_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cn_sub_bas

        self.sub_ax_sbx.setValue(self.defaultSubDiv.cur_sub_ax)
        self.sub_hgt_sbx.setValue(self.defaultSubDiv.cur_sub_hgt)
        self.sub_bas_sbx.setValue(self.defaultSubDiv.cur_sub_bas)

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    def create_obj_layout_ui(self):
        self.shape_cmb = QtWidgets.QComboBox()
        self.shape_cmb.setFixedWidth(100)
        self.shape_cmb.addItems(['Cube', 'Sphere', 'Cylinder', 'Cone'])
        self.shape_btn = QtWidgets.QPushButton("Create Shape")

        self.sub_ax_sbx = QtWidgets.QSpinBox()
        self.sub_ax_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_ax_sbx.setFixedWidth(50)
        self.sub_ax_sbx.setValue(self.defaultSubDiv.cur_sub_ax)

        self.sub_hgt_sbx = QtWidgets.QSpinBox()
        self.sub_hgt_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_hgt_sbx.setFixedWidth(50)
        self.sub_hgt_sbx.setValue(self.defaultSubDiv.cur_sub_hgt)

        self.sub_bas_sbx = QtWidgets.QSpinBox()
        self.sub_bas_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_bas_sbx.setFixedWidth(50)
        self.sub_bas_sbx.setValue(self.defaultSubDiv.cur_sub_bas)

        self.sub_ax = QtWidgets.QLabel("Sub Axis")
        self.sub_ax.setFixedWidth(100)
        self.sub_hgt = QtWidgets.QLabel("Sub Height")
        self.sub_hgt.setFixedWidth(100)
        self.sub_bas = QtWidgets.QLabel("Sub Base")
        self.sub_bas.setFixedWidth(100)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.shape_cmb, 0, 0)
        layout.addWidget(self.shape_btn, 0, 1)
        layout.addWidget(self.sub_ax, 0, 3)
        layout.addWidget(self.sub_ax_sbx, 0, 4)
        layout.addWidget(self.sub_hgt, 0, 5)
        layout.addWidget(self.sub_hgt_sbx, 0, 6)
        layout.addWidget(self.sub_bas, 0, 7)
        layout.addWidget(self.sub_bas_sbx, 0, 8)
        return layout

    def sct_cnl_layout_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter Object")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_btn, 0, 0)
        layout.addWidget(self.cancel_btn, 0, 1)
        return layout


class DefaultSubDiv(object):

    def __init__(self):
        self.cur_sub_ax = 0
        self.cur_sub_hgt = 0
        self.cur_sub_bas = 0
        self.cb_sub_ax = 1
        self.cb_sub_hgt = 1
        self.cb_sub_bas = 1
        self.s_sub_ax = 8
        self.s_sub_hgt = 8
        self.s_sub_bas = 0
        self.cyl_sub_ax = 8
        self.cyl_sub_hgt = 4
        self.cyl_sub_bas = 0
        self.cn_sub_ax = 8
        self.cn_sub_hgt = 3
        self.cn_sub_bas = 0
