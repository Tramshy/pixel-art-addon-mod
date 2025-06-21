import bpy
import os

SHINE_GROUP = "Shine Reflection"
SMOKE_PARTICLE = "Smoke Particle (Will render)"
ADDON_DIR = os.path.dirname(__file__)
BLEND_PATH = os.path.join(ADDON_DIR, "assets/pixel art addon_assets.blend")

def is_shine_group_missing():
    return SHINE_GROUP not in bpy.data.node_groups

def is_particle_asset_missing():
    SMOKE_PARTICLE not in bpy.data.objects

# Note to self:
# Proabbly didn't need to make the node group an asset and all of that stuff.
def append_shine_from_asset():
    if not is_shine_group_missing():
        return
    
    # Load in shine node group from .blend file to current .blend file.
    with bpy.data.libraries.load(BLEND_PATH, link=False) as (data_from, data_to):
        if SHINE_GROUP in data_from.node_groups:
            data_to.node_groups = [SHINE_GROUP]

# def append_smoke_particle_from_asset():
#     with bpy.data.libraries.load(BLEND_PATH, link=False) as (data_from, data_to):
#         data_to.objects = [SMOKE_PARTICLE]

#     particle = data_to.objects[0]
#     copy = particle.copy()
#     bpy.context.scene.collection.objects.link(copy)
#     copy.location = (0, 0, 0)

#     return copy