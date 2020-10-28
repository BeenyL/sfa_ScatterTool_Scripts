import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel
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
        self.defaultRot = DefaultRot()

        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: Bold 20px")
        self.create_poly = QtWidgets.QLabel("Create a Polygon")
        self.create_poly.setStyleSheet("font: Bold 10px")
        self.scatter_rot_lbl = QtWidgets.QLabel("Scatter Rotation")
        self.scatter_rot_lbl.setStyleSheet("font: Bold 10px")
        self.scatter_scl_lbl = QtWidgets.QLabel("Scatter Scale")
        self.scatter_scl_lbl.setStyleSheet("font: Bold 10px")
        self.create_obj_lay = self.create_obj_layout_ui()
        self.sct_cnl_lay = self.sct_cnl_layout_ui()
        self.rnd_rotation_lay = self.rnd_rotation_ui()

        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.create_poly)
        self.main_lay.addLayout(self.create_obj_lay)
        self.main_lay.addWidget(self.scatter_rot_lbl)
        self.main_lay.addLayout(self.rnd_rotation_lay)
        self.main_lay.addWidget(self.scatter_scl_lbl)

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

        self.min_x_rot_sbx.valueChanged.connect(self.update_rot_min_val_x)
        self.min_y_rot_sbx.valueChanged.connect(self.update_rot_min_val_y)
        self.min_z_rot_sbx.valueChanged.connect(self.update_rot_min_val_z)
        self.max_x_rot_sbx.valueChanged.connect(self.update_rot_max_val_x)
        self.max_y_rot_sbx.valueChanged.connect(self.update_rot_max_val_y)
        self.max_z_rot_sbx.valueChanged.connect(self.update_rot_max_val_z)



    def update_sub_val_ax(self):
        self.defaultSubDiv.cur_sub_ax = self.sub_ax_sbx.value()

    def update_sub_val_hgt(self):
        self.defaultSubDiv.cur_sub_hgt = self.sub_hgt_sbx.value()

    def update_sub_val_bas(self):
        self.defaultSubDiv.cur_sub_bas = self.sub_bas_sbx.value()

    def update_rot_min_val_x(self):
        self.defaultRot.min_rot_x = self.min_x_rot_sbx.value()

    def update_rot_min_val_y(self):
        self.defaultRot.min_rot_y = self.min_y_rot_sbx.value()

    def update_rot_min_val_z(self):
        self.defaultRot.min_rot_z = self.min_z_rot_sbx.value()

    def update_rot_max_val_x(self):
        self.defaultRot.max_rot_x = self.max_x_rot_sbx.value()

    def update_rot_max_val_y(self):
        self.defaultRot.max_rot_y = self.max_y_rot_sbx.value()

    def update_rot_max_val_z(self):
        self.defaultRot.max_rot_z = self.max_z_rot_sbx.value()

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
        vert_list = cmds.ls(selection=True, fl=True)
        scatter_grp = cmds.group(n='scatter_grp')
        object_to_instance = vert_list[0]
        if cmds.objectType(object_to_instance) == 'transform':

            for vert in vert_list:
                vertex_pos = cmds.xform(vert, q=True, ws=True, t=True)
                new_instance = cmds.instance(object_to_instance)

                cmds.move(vertex_pos[0], vertex_pos[1], vertex_pos[2],
                          new_instance)

                cmds.scale(vertex_pos[0], vertex_pos[1], vertex_pos[2],
                           new_instance, relative=True)

    @QtCore.Slot()
    def scatter_rot_object(self):
        """scatter an Object"""
        vert_list = cmds.ls(selection=True, fl=True)
        scatter_grp = cmds.group(n='scatter_grp')
        object_to_instance = vert_list[0]
        if cmds.objectType(object_to_instance) == 'transform':

            for vert in vert_list:
                vertex_pos = cmds.xform(vert, q=True, ws=True, t=True)
                new_instance = cmds.instance(object_to_instance)

                cmds.rotate(vertex_pos[0],
                            vertex_pos[1],
                            vertex_pos[2],
                            new_instance, relative=True, objectSpace=True)

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
        self.create_shape_cmb()
        self.sub_div_ax_sbx()
        self.sub_div_hgt_sbx()
        self.sub_div_bas_sbx()

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

    def sub_div_ax_sbx(self):
        self.sub_ax_sbx = QtWidgets.QSpinBox()
        self.sub_ax_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_ax_sbx.setFixedWidth(50)
        self.sub_ax_sbx.setValue(self.defaultSubDiv.cur_sub_ax)

        self.sub_ax = QtWidgets.QLabel("Sub Axis")
        self.sub_ax.setFixedWidth(60)
        self.sub_ax.setIndent(15)

    def sub_div_hgt_sbx(self):
        self.sub_hgt_sbx = QtWidgets.QSpinBox()
        self.sub_hgt_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_hgt_sbx.setFixedWidth(50)
        self.sub_hgt_sbx.setValue(self.defaultSubDiv.cur_sub_hgt)

        self.sub_hgt = QtWidgets.QLabel("Sub Height")
        self.sub_hgt.setFixedWidth(65)
        self.sub_hgt.setIndent(5)

    def sub_div_bas_sbx(self):
        self.sub_bas_sbx = QtWidgets.QSpinBox()
        self.sub_bas_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_bas_sbx.setFixedWidth(50)
        self.sub_bas_sbx.setValue(self.defaultSubDiv.cur_sub_bas)

        self.sub_bas = QtWidgets.QLabel("Sub Base")
        self.sub_bas.setFixedWidth(60)
        self.sub_bas.setIndent(15)

    def create_shape_cmb(self):
        self.shape_cmb = QtWidgets.QComboBox()
        self.shape_cmb.setFixedWidth(100)
        self.shape_cmb.addItems(['Cube', 'Sphere', 'Cylinder', 'Cone'])
        self.shape_btn = QtWidgets.QPushButton("Create Shape")

    def sct_cnl_layout_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter Object")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_btn, 0, 0)
        layout.addWidget(self.cancel_btn, 0, 1)
        return layout

    def rnd_rotation_ui(self):
        self.rot_btn = QtWidgets.QPushButton("Randomize Rotation")
        self.x_rot_sbx()
        self.y_rot_sbx()
        self.z_rot_sbx()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rot_btn, 0, 0)
        layout.addWidget(self.rotX_lbl, 0, 1)
        layout.addWidget(self.min_x_rot_sbx, 0, 2)
        layout.addWidget(self.x_rot_space, 0, 3)
        layout.addWidget(self.max_x_rot_sbx, 0, 4)
        layout.addWidget(self.rotY_lbl, 0, 5)
        layout.addWidget(self.min_y_rot_sbx, 0, 6)
        layout.addWidget(self.y_rot_space, 0, 7)
        layout.addWidget(self.max_y_rot_sbx, 0, 8)
        layout.addWidget(self.rotZ_lbl, 0, 9)
        layout.addWidget(self.min_z_rot_sbx, 0, 10)
        layout.addWidget(self.z_rot_space, 0, 11)
        layout.addWidget(self.max_z_rot_sbx, 0, 12)
        return layout

    def x_rot_sbx(self):
        self.min_x_rot_sbx = QtWidgets.QSpinBox()
        self.min_x_rot_sbx.setMaximum(360)
        self.min_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_rot_sbx.setFixedWidth(50)
        self.min_x_rot_sbx.setValue(self.defaultRot.min_rot_x)

        self.rotX_lbl = QtWidgets.QLabel("X")
        self.rotX_lbl.setFixedWidth(60)
        self.rotX_lbl.setIndent(54)
        self.x_rot_space = QtWidgets.QLabel("-")
        self.x_rot_space.setStyleSheet("font: 20px")

        self.max_x_rot_sbx = QtWidgets.QSpinBox()
        self.max_x_rot_sbx.setMaximum(360)
        self.max_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_rot_sbx.setFixedWidth(50)
        self.max_x_rot_sbx.setValue(self.defaultRot.max_rot_x)

    def y_rot_sbx(self):
        self.min_y_rot_sbx = QtWidgets.QSpinBox()
        self.min_y_rot_sbx.setMaximum(360)
        self.min_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_rot_sbx.setFixedWidth(50)
        self.min_y_rot_sbx.setValue(self.defaultRot.min_rot_y)

        self.rotY_lbl = QtWidgets.QLabel("Y")
        self.rotY_lbl.setFixedWidth(65)
        self.rotY_lbl.setIndent(54)
        self.y_rot_space = QtWidgets.QLabel("-")
        self.y_rot_space.setStyleSheet("font: 20px")

        self.max_y_rot_sbx = QtWidgets.QSpinBox()
        self.max_y_rot_sbx.setMaximum(360)
        self.max_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_rot_sbx.setFixedWidth(50)
        self.max_y_rot_sbx.setValue(self.defaultRot.max_rot_y)

    def z_rot_sbx(self):
        self.min_z_rot_sbx = QtWidgets.QSpinBox()
        self.min_z_rot_sbx.setMaximum(360)
        self.min_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_rot_sbx.setFixedWidth(50)
        self.min_z_rot_sbx.setValue(self.defaultRot.min_rot_z)

        self.rotZ_lbl = QtWidgets.QLabel("Z")
        self.rotZ_lbl.setFixedWidth(60)
        self.rotZ_lbl.setIndent(54)
        self.z_rot_space = QtWidgets.QLabel("-")
        self.z_rot_space.setStyleSheet("font: 20px")

        self.max_z_rot_sbx = QtWidgets.QSpinBox()
        self.max_z_rot_sbx.setMaximum(360)
        self.max_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_rot_sbx.setFixedWidth(50)
        self.max_z_rot_sbx.setValue(self.defaultRot.max_rot_z)


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


class DefaultRot(object):

    def __init__(self):
        self.min_rot_x = 0
        self.min_rot_y = 0
        self.min_rot_z = 0
        self.max_rot_x = 360
        self.max_rot_y = 360
        self.max_rot_z = 360


class DefaultScl(object):

    def __init__(self):
        self.min_scl_x = 0.8
        self.min_scl_y = 0.8
        self.min_scl_z = 0.8
        self.max_scl_x = 1.2
        self.max_scl_y = 1.2
        self.max_scl_z = 1.2
