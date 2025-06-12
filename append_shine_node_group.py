import bpy
import os

SHINE_GROUP = "Shine Reflection"

def is_shine_group_missing():
    return SHINE_GROUP not in bpy.data.node_groups

def append_from_asset():
    if not is_shine_group_missing():
        return
    
    addon_dir = os.path.dirname(__file__)
    blend_path = os.path.join(addon_dir, "assets/pixel art addon_assets.blend")
    
    # Load in pixelation node group from .blend file to current .blend file.
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if SHINE_GROUP in data_from.node_groups:
            data_to.node_groups = [SHINE_GROUP]