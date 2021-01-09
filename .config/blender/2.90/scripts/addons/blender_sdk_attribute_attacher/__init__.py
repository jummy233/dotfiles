"""
Classes started with CUSTOM_ are top level classes,
need to be registered.

Classes stated with SUB_ is used by other CUSTOM_ classes, shoule not
be registered in register()

Note: If you are defining a operator be care of the blender2.8 operator
bl_idname naming convention!
"""

# auto reload
import logging
from . import config

if config.DEBUG:
    logging.basicConfig(level=logging.DEBUG)

if "bpy" in locals():
    logging.debug("reloading modules")
    import importlib
    from . import components
    from . import properties
    importlib.reload(components)
    importlib.reload(properties)
else:
    logging.debug("first time ")
    from . import components
    from . import properties

import sys
import bpy


bl_info = {
    "name": "Unity SDK Attribute attacher",
    "description": " Attach unity sdk attributes to blender object, and talk with unity client direclty ",
    "author": "Motive B",
    "version": (0, 0, 3),
    "blender": (2, 80, 0),
    "location": "3D View > Attacher",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_rl": "",
    "tracker_url": "",
    "category": "Development"
}


sys.setrecursionlimit(10000)


class CUSTOM_INIT(bpy.types.Operator):
    """
    Initialize states on registration.
    """

    def __init__(self):
        pass

    def execute(self, context):
        pass


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


# All blender addon classes.
classes = components.component_classes + \
    properties.property_classes + \
    (properties.CUSTOM_AttacherProperties,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # attacher is the Top level properties
    bpy.types.Scene.attacher = bpy.props.PointerProperty(
        type=properties.CUSTOM_AttacherProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        del cls

    del bpy.types.Scene.attacher


if __name__ == "__main__":
    register()
