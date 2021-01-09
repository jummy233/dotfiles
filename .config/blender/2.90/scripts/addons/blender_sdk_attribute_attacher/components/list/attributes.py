"""
List of all attributes provided by sdk.

Attribute popup list is a list on the popup window, it appears when
add_attribute button on the object list is clicked.
"""

from bpy.types import (Panel, Operator, UIList, AnyType)
from bl_ui.properties_paint_common import UnifiedPaintPanel
from bpy.props import (StringProperty)
import bpy
from ... import motive
from .ops import CUSTOM_OT_AddAttributeList, CUSTOM_OT_AddObjectList


class CUSTOM_UL_AttributeListPop(UIList):
    """
    List of all attributes available from sdk.
    This ulist keeps track of current focused object.
    If there are attributes already in the object's attribute list
    those attributes will not be displayed here.

    NOTE:
    {Attribute shown on object attribte list} +
    {attributes shown on all attributes list} = {all attributes list}
    """
    bl_label = "All Attributes"
    bl_idname = "CUSTOM_UL_attribute_list_pop"

    def draw_item(self, context, layout, data, item,
                  icon, active_data, active_propname, index):
        # TODO 2020-11-22
        # The icon here should change to RADIOBUT_OFF
        # if the attribute is already in current object's attribute list.
        icon = "RADIOBUT_ON"

        # https://docs.blender.org/api/current/bpy.types.UILayout.html?highlight=layout#bpy.types.UILayout.prop
        # be aware that the first parameter is an AnyType Object, and
        # the second parameter is name of attribute to show in the
        # first parameter.

        layout.row().prop(item, "attr_name",
                          text=f"{index}", emboss=False,
                          translate=False,
                          icon=icon)


class CUSTOM_OT_AddAttributeListPop(Operator, UnifiedPaintPanel):
    """
    Implementation of popup list.
    """
    # TODO 2020-10-26:Jimmy:nned more specific comments.
    bl_idname = "sub.attacher_all_attribute_list_add"
    bl_label = "Add Attribute"

    nrow = 10

    def execute(self, context: bpy.types.Context):
        attacher = context.scene.attacher

        # refresh the attributes every time the button is clicked.
        self.init_all_attributes(attacher)

        return context.window_manager.invoke_popup(self, width=300)

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        attacher = context.scene.attacher

        col = layout.column()
        col.separator()
        row = col.row(align=True)

        # attribute list
        row.template_list(
            listtype_name=CUSTOM_UL_AttributeListPop.bl_idname,
            list_id="AllAttributeList",
            dataptr=attacher,
            propname="all_attributes",
            active_dataptr=attacher,
            active_propname="active_all_attribute",
            rows=self.nrow)

        row = col.row(align=True)

        row.operator(CUSTOM_OT_AddAttributeList.bl_idname,
                     text="Add", icon="PLUS")

    def init_all_attributes(self, attacher):
        # initalize the attribute list.
        # Make sure only shows attributes not already in the
        # object's attribute list.

        attacher.all_attributes.clear()
        obj_idx = attacher.active_object

        if len(attacher.objects) > 0:
            focused_obj = attacher.objects[obj_idx]

            for n in motive.motive_attributes:
                if n not in [m.attr_name for m in focused_obj.attributes]:
                    o = attacher.all_attributes.add()
                    o.attr_name = n


attributes_classes = tuple(
    v for k, v in globals().items() if k.startswith("CUSTOM"))
