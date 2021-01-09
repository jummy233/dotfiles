from bpy.types import (UIList, Operator)
import bpy


class CUSTOM_UL_ObjectList(UIList):
    """
    List of objects. Each element of the list corresponds to an attrbute list.
    ref:
        https://sinestesia.co/blog/tutorials/using-uilists-in-blender/
    """

    def draw_item(self, context, layout, data, item,
                  icon, active_data, active_propname, index):
        icon = f"OUTLINER_OB_{item.ref.type}"
        layout.row().prop(item.ref, "name",
                          text=f"{index}",
                          emboss=False,
                          translate=False, icon=icon)

    def invoke(self, context, event):
        pass


class CUSTOM_UL_AttributeList(UIList):
    """
    List of attributes attached to objects.
    """

    def draw_item(self, context, layout, data, item,
                  icon, active_data, active_propname, index):
        print(item)
        print(item.attr_name)

        # TODO
        split = layout.split(factor=0.6)
        split.prop(item,
                   "attr_name",
                   text=f"{index}",
                   emboss=False,
                   translate=False, icon="HEART")

        # split.label(text="Attr: {data.name}")
