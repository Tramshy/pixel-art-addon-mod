"""
Copyright (C) 2023-2025 Lucas Roedel
    https://lucasroedel.com
    contato@lucasroedel.com

Created by Lucas Roedel Ribeiro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "Pixel Art Rendering (Eevee, Modified)",
    "author": "Lucas Roedel (Modified by Trashy aka Simon)",
    "version": (3, 0),
    "blender": (4, 1, 0),
    "location": "3D Viewport > Side panel",
    "description": "Pixel Art rendering addon using eevee. Based on the work of Mezaka",
    "category": "Render",
}

import bpy
from bpy.utils import register_class, unregister_class
from . import pixel_art_addon
from .append_assets import append_shine_from_asset

########## Set Render Settings ##########
def render_settings(context):
    scene = bpy.context.scene

    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except:
        scene.render.engine = 'BLENDER_EEVEE'

    scene.eevee.taa_render_samples = 1
    scene.eevee.taa_samples = 1
    scene.eevee.use_taa_reprojection = False
    scene.eevee.use_gtao = True
    scene.render.filter_size = 0.00
    scene.render.use_freestyle = False
    scene.render.line_thickness = 0.1
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'Standard'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_depth = '16'
    scene.render.film_transparent = True
    scene.render.image_settings.compression = 100

    scene.render.resolution_x = 256
    scene.render.resolution_y = 256

    bpy.ops.scene.freestyle_color_modifier_add(type='MATERIAL')
    bpy.data.linestyles["LineStyle"].thickness_position = 'INSIDE'

class PIXEL_ART_OT_render_settings(bpy.types.Operator):
    """Sets up blender with the correct settings for pixel art rendering"""
    bl_idname = "render.render_settings"
    bl_label = "Render Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        render_settings(context)
        return {'FINISHED'}

class PIXEL_ART_OT_single_material(bpy.types.Operator):
    """Creates default pixel art material. If material with name 'PixelArt_Simple' already exists, resets it to default"""
    bl_idname = "render.single_material"
    bl_label = "Create/Reset Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.single_material(context)
        return {'FINISHED'}

class PIXEL_ART_OT_single_material_shine(bpy.types.Operator):
    """Creates default pixel art material and a stylized shine effect. If material with name 'PixelArt_Simple' already exists, resets it to default and adds shine"""
    bl_idname = "render.single_material_shine"
    bl_label = "Create/Add Material (Shine)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.single_material_shine(self, context)
        return {'FINISHED'}

class PIXEL_ART_OT_multiple_material(bpy.types.Operator):
    """Creates pixel art material with multiple lights setup. If material with name 'PixelArt_MultipleLights' already exists, resets it to default"""
    bl_idname = "render.multiple_material"
    bl_label = "Create/Reset Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.multiple_material(context)
        return {'FINISHED'}

class PIXEL_ART_OT_multiple_material_shine(bpy.types.Operator):
    """Creates pixel art material with multiple lights setup and a stylized shine effect. If material with name 'PixelArt_MultipleLights' already exists, resets it to default and adds shine"""
    bl_idname = "render.multiple_material_shine"
    bl_label = "Create/Add Shine)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.multiple_material_shine(self, context)
        return {'FINISHED'}

class PIXEL_ART_OT_lights_setup(bpy.types.Operator):
    """Creates a setup of three point lights to work with the multiple lights pixel art material"""
    bl_idname = "render.lights_setup"
    bl_label = "Tri Light Setup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.lights_setup(context)
        return {'FINISHED'}

class new_smoke_particle_system(bpy.types.Operator):
    """Creates a new emitter with a new particle object that can be manipulated"""
    bl_idname = "render.smoke_particle_dupli"
    bl_label = "Create Particle System"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.create_smoke()
        return {'FINISHED'}

class new_smoke_emitter(bpy.types.Operator):
    """Creates a new emitter, but not a new smoke particle. You will have to manually set the smoke particle to the emitter. This is useful if you only want to use one particle object instance"""
    bl_idname = "render.smoke_particle"
    bl_label = "Create Emitter"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pixel_art_addon.create_emitter()
        return {'FINISHED'}

class PIXEL_RENDER_PT_pixel_render_panel(bpy.types.Panel):
    """Creates a Panel for Pixel Rendering in the UI Panels"""
    bl_label = "Pixel Render"
    bl_idname = "PIXEL_RENDER_PT_pixel_render_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Pixel Render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene     
        
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'          
        row.label(text="Render Settings for Pixel Art", icon = "RESTRICT_RENDER_OFF")
        row = box.row()
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.render_settings")
        row = box.row()
        row = layout.row()

        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'          
        row.label(text="Default Pixel Art Material", icon = "MATERIAL")
        row = box.row()
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.single_material")
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.single_material_shine")
        row = box.row()
        row = layout.row()
        
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'          
        row.label(text="Multiple Lights Material", icon = "NODE_MATERIAL")
        row = box.row()
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.multiple_material")
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.multiple_material_shine")
        row = box.row()
        row.scale_y = 1
        row.operator("render.lights_setup")

        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'          
        row.label(text="Smoke Particle System", icon = "PARTICLE_POINT")
        row = box.row()
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.smoke_particle_dupli")
        row = box.row()
        row.scale_y = 1.5
        row.operator("render.smoke_particle")
        row = box.row()
        row = layout.row()

classes = [
    PIXEL_ART_OT_render_settings,
    PIXEL_ART_OT_single_material,
    PIXEL_ART_OT_single_material_shine,
    PIXEL_ART_OT_multiple_material,
    PIXEL_ART_OT_multiple_material_shine,
    PIXEL_ART_OT_lights_setup,
    PIXEL_RENDER_PT_pixel_render_panel,
    new_smoke_particle_system,
    new_smoke_emitter
]

def register():
    for cls in classes:
        register_class(cls)

    # Wait to let main Blender thread load node_groups in bpy.data.
    bpy.app.timers.register(append_shine_from_asset)

def unregister():
    for cls in classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()