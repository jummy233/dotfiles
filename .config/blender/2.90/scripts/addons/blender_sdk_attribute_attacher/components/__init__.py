from .attacher import attacher_classes
from .export import export_classes
from .list import list_classes

from .. import config


"""
component_classes export a tuple of classes that needs to be registered by
blender.
All classes under `components/` that inherit from bpy need to appear here.
"""


component_classes = (attacher_classes
                     + list_classes
                     + export_classes
                     )

# for debug only
if config.DEBUG:
    from .debug import debug_classes
    component_classes += debug_classes
