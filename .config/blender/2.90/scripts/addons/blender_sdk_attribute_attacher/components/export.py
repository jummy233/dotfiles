"""
Sub panel for exporting.
"""

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import (Panel,
                       Menu,
                       Operator
                       )
import json
import logging
import base64
import os
from .. import config
from .. import util


class CUSTOM_OT_AttacherExport(Operator, ExportHelper):
    """
    Send the current state of the object list as message to the
    unity side client.
    """
    bl_label = "Export"
    bl_idname = "custom.attacher_export"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ''

    def execute(self, context: bpy.types.Context):
        # blender api doesn't directly return the glb data.
        # to work around we dump the glb data to a tempory file,
        # read it back and base64 encode it to fit into a json
        # file.

        temp_filepath = self.file_path + "-tmp"

        if config.DEBUG:
            logging.info("path to save: " + self.filepath)

        pkgpath: str = self.filepath + ".glb" + ".json"
        glbpath: str = temp_filepath + ".glb"

        bpy.ops.export_scene.gltf(filepath=glbpath)

        with open(glbpath, 'rb') as glb:
            byte_data = glb.read()
            encoded = base64.encodebytes(byte_data).decode('utf-8')
            package = util.Package(glb_base64_payload=encoded,
                                   attribute_list=[])

            with open(pkgpath, 'w') as pkg:
                pkg.write(json.dumps(package.toJson()))

        os.remove(glbpath)

        return {"FINISHED"}


class CUSTOM_OT_AttacherSave(Operator, ExportHelper):
    """
    Save the current state of the object list as json format in
    a local file.
    """
    bl_label = "Save"
    bl_idname = "custom.attacher_save"
    bl_options = {'PRESET', 'UNDO'}

    # # ExportHelper specific
    filename_ext = ''

    def execute(self, context: bpy.types.Context):
        bpy.ops.export_scene.gltf(filepath=self.filepath)
        return {"FINISHED"}


class CUSTOM_PT_AttacherExport(Panel):
    bl_label = "Export"
    bl_idname = "OBJECT_PT_attacher_export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Attacher"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.operator(CUSTOM_OT_AttacherSave.bl_idname)
        row.operator(CUSTOM_OT_AttacherExport.bl_idname)


export_classes = tuple(
    v for k, v in globals().items() if k.startswith("CUSTOM"))
