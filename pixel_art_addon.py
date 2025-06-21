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

import bpy

########## Creates Simple Default Material ##########
def single_material(context, defaultName = "PixelArt_Simple"):
    # Generate Bayer Matrix 2x2
    bayerMatrix = bpy.data.images.get("Bayer Matrix")

    if bayerMatrix == None:

        bayerMatrix = bpy.data.images.new("Bayer Matrix", 2, 2)
        bayerMatrix.use_fake_user = True
        bayerMatrix.pixels[0] = (0.75294)
        bayerMatrix.pixels[1] = (0.75294)
        bayerMatrix.pixels[2] = (0.75294)
        bayerMatrix.pixels[4] = (0.25098)
        bayerMatrix.pixels[5] = (0.25098)
        bayerMatrix.pixels[6] = (0.25098)
        bayerMatrix.pixels[12] = (0.50196)
        bayerMatrix.pixels[13] = (0.50196)
        bayerMatrix.pixels[14] = (0.50196)
        
        bayerMatrix.filepath_raw = "/tmp/bayerMatrix.png"
        bayerMatrix.file_format = 'PNG'
        bayerMatrix.save()        

    # Creates a material with the name if it doesn' exist already
    for material in bpy.data.materials:
        if material.name == defaultName:
            bpy.data.materials.remove(material)
    material = bpy.data.materials.new(name = defaultName)
    material.use_nodes = True
    material.use_fake_user = True

    materialOutput = None
    for node in material.node_tree.nodes:
        if node.type == 'OUTPUT_MATERIAL':
            materialOutput = node
            break

    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            material.node_tree.nodes.remove(node)
            break

    # Creates the emission shader node
    emissionNode = material.node_tree.nodes.new(type = "ShaderNodeEmission")
    emissionNode.location = (100,300)
    material.node_tree.links.new(emissionNode.outputs[0], materialOutput.inputs[0])

    # Creates the color ramp node
    colorRampNode = material.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    colorRampNode.location = (-250,300)
    material.node_tree.links.new(colorRampNode.outputs[0], emissionNode.inputs[0])
    colorRampNode.color_ramp.interpolation = 'CONSTANT'
    colorRampNode.color_ramp.elements.remove(colorRampNode.color_ramp.elements[1])
    colorRampNode.color_ramp.elements.new(0.075)
    colorRampNode.color_ramp.elements.new(0.225)
    colorRampNode.color_ramp.elements.new(0.450)
    colorRampNode.color_ramp.elements.new(0.800)
    colorRampNode.color_ramp.elements[0].color = [0.191202, 0.033105, 0.063010, 1.000000]
    colorRampNode.color_ramp.elements[1].color = [0.337164, 0.063010, 0.045186, 1.000000]
    colorRampNode.color_ramp.elements[2].color = [0.603828, 0.138432, 0.049707, 1.000000]
    colorRampNode.color_ramp.elements[3].color = [0.783538, 0.274677, 0.078187, 1.000000]
    colorRampNode.color_ramp.elements[4].color = [0.955974, 0.473532, 0.090842, 1.000000]

    # Creates the mixRGB soft light node
    mixSoftLightNode = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixSoftLightNode.location = (-500, 138)
    mixSoftLightNode.blend_type = 'SOFT_LIGHT'
    mixSoftLightNode.inputs[0].default_value = 0.2
    material.node_tree.links.new(mixSoftLightNode.outputs[0], colorRampNode.inputs[0])

    # Creates the shader to RGB node
    shaderToRgbNode = material.node_tree.nodes.new(type = "ShaderNodeShaderToRGB")
    shaderToRgbNode.location = (-750, 250)
    material.node_tree.links.new(shaderToRgbNode.outputs[0], mixSoftLightNode.inputs[1])

    # Creates the principled BSDF node
    bsdfNode = material.node_tree.nodes.new(type = "ShaderNodeBsdfPrincipled")
    bsdfNode.location = (-1100, 500)
    material.node_tree.links.new(bsdfNode.outputs[0], shaderToRgbNode.inputs[0])

    # Creates the bayer texture node
    bayerTexNode = material.node_tree.nodes.new(type = "ShaderNodeTexImage")
    bayerTexNode.location = (-850, -250)
    material.node_tree.links.new(bayerTexNode.outputs[0], mixSoftLightNode.inputs[2])
    bayerTexNode.image = bayerMatrix
    bayerTexNode.interpolation = 'Closest'

    # Creates the multiply node
    multiplyVector = material.node_tree.nodes.new(type = "ShaderNodeVectorMath")
    multiplyVector.location = (-1050, -450)
    multiplyVector.operation = 'MULTIPLY'
    material.node_tree.links.new(multiplyVector.outputs[0], bayerTexNode.inputs[0])

    # Creates the Texture Coordinate node
    texCoordNode = material.node_tree.nodes.new(type = "ShaderNodeTexCoord")
    texCoordNode.location = (-1250, -300)
    material.node_tree.links.new(texCoordNode.outputs[5], multiplyVector.inputs[0])

    # Creates the combineXYZ node
    combineXyzNode = material.node_tree.nodes.new(type = "ShaderNodeCombineXYZ")
    combineXyzNode.location = (-1250, -600)
    material.node_tree.links.new(combineXyzNode.outputs[0], multiplyVector.inputs[1])

    # Creates the Resolution nodes
    resolutionXnode = material.node_tree.nodes.new(type = "ShaderNodeValue")
    resolutionXnode.location = (-1450, -600)
    resolutionXnode.label = "ResolutionX / 2"
    material.node_tree.links.new(resolutionXnode.outputs[0], combineXyzNode.inputs[0])

    resolutionXdriver = resolutionXnode.outputs['Value'].driver_add("default_value")
    var1 = resolutionXdriver.driver.variables.new()
    var1.name = "resolutionX"
    var1.targets[0].id_type = 'SCENE'
    var1.targets[0].id = bpy.data.scenes["Scene"]
    var1.targets[0].data_path = "render.resolution_x"
    resolutionXdriver.driver.expression = "resolutionX / 2"

    resolutionYnode = material.node_tree.nodes.new(type = "ShaderNodeValue")
    resolutionYnode.location = (-1450, -700)
    resolutionYnode.label = "ResolutionY / 2"
    material.node_tree.links.new(resolutionYnode.outputs[0], combineXyzNode.inputs[1])

    resolutionYdriver = resolutionYnode.outputs['Value'].driver_add("default_value")
    var2 = resolutionYdriver.driver.variables.new()
    var2.name = "resolutionY"
    var2.targets[0].id_type = 'SCENE'
    var2.targets[0].id = bpy.data.scenes["Scene"]
    var2.targets[0].data_path = "render.resolution_y"
    resolutionYdriver.driver.expression = "resolutionY / 2"

    return material

def single_material_shine(self, context):
    single_material(context)

    mat = None

    for material in bpy.data.materials:
        if material.name == "PixelArt_Simple":
            mat = material

    if mat is None:
        self.report({'ERROR'}, "No PixelArt material found. This should not be possible... good luck")
        return
    
    nodes = mat.node_tree.nodes
    # Get pre-existing nodes
    material_output = nodes.get("Material Output")
    emission = nodes.get("Emission")
    color_ramp = nodes.get("Color Ramp")

    # Disconnect color ramp and emission nodes
    link = color_ramp.outputs[0].links[0]
    color_ramp.id_data.links.remove(link)

    # Move material output and emission nodes
    material_output.location = (585, 305)
    emission.location = (390, 285)

    # Create new nodes
    shine_group = nodes.new(type="ShaderNodeGroup")
    shine_group.node_tree = bpy.data.node_groups["Shine Reflection"]
    shine_group.location = (-105, 30)

    # Value nodes for rotation and scale of shine group
    value_rot = nodes.new(type="ShaderNodeValue")
    value_rot.location = (-315, -100)
    value_rot.label = "Shine Rotation"
    value_rot.outputs[0].default_value = 2.5

    value_scale = nodes.new(type="ShaderNodeValue")
    value_scale.location = (-315, -190)
    value_scale.label = "Shine Scale"
    value_scale.outputs[0].default_value = 1

    # Create color mixing node and set correct settings before use
    mix_node = nodes.new(type="ShaderNodeMixRGB")
    mix_node.location = (155, 200)
    mix_node.blend_type = 'ADD'

    # Connect nodes
    links = mat.node_tree.links

    links.new(value_rot.outputs[0], shine_group.inputs['Rotation'])
    links.new(value_scale.outputs[0], shine_group.inputs['Scale'])
    links.new(shine_group.outputs[0], mix_node.inputs['Color2'])
    links.new(color_ramp.outputs['Color'], mix_node.inputs['Color1'])
    links.new(mix_node.outputs[0], emission.inputs['Color'])

########## Creates Multiple Lights Default Material ##########
def multiple_material(context):
    
    # Generate Bayer Matrix 2x2
    bayerMatrix = bpy.data.images.get("Bayer Matrix")

    if bayerMatrix == None:

        bayerMatrix = bpy.data.images.new("Bayer Matrix", 2, 2)
        bayerMatrix.use_fake_user = True
        bayerMatrix.pixels[0] = (0.75294)
        bayerMatrix.pixels[1] = (0.75294)
        bayerMatrix.pixels[2] = (0.75294)
        bayerMatrix.pixels[4] = (0.25098)
        bayerMatrix.pixels[5] = (0.25098)
        bayerMatrix.pixels[6] = (0.25098)
        bayerMatrix.pixels[12] = (0.50196)
        bayerMatrix.pixels[13] = (0.50196)
        bayerMatrix.pixels[14] = (0.50196)
        
        bayerMatrix.filepath_raw = "/tmp/bayerMatrix.png"
        bayerMatrix.file_format = 'PNG'
        bayerMatrix.save()

    # Creates a material with the name if it doesn' exist already
    for material in bpy.data.materials:
        if material.name == "PixelArt_MultipleLights":
            bpy.data.materials.remove(material)
        
    material = bpy.data.materials.new(name = "PixelArt_MultipleLights")

    material.use_nodes = True
    material.use_fake_user = True

    materialOutput = None
    for node in material.node_tree.nodes:
        if node.type == 'OUTPUT_MATERIAL':
            materialOutput = node
            break

    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            material.node_tree.nodes.remove(node)
            break

    # Creates a group for the dithering part
    for group in bpy.data.node_groups:
        if group.name == 'Dithering':
            bpy.data.node_groups.remove(group)

    ditherGroup = bpy.data.node_groups.new('Dithering', 'ShaderNodeTree')
    ditherGroup.interface.new_socket("Color", in_out='OUTPUT', socket_type="NodeSocketColor")

    outputNode = ditherGroup.nodes.new("NodeGroupOutput")
    outputNode.location = (0, 0)

    # Creates the bayer texture node
    bayerTexNode = ditherGroup.nodes.new(type = "ShaderNodeTexImage")
    bayerTexNode.location = (-300, 0)
    ditherGroup.links.new(bayerTexNode.outputs[0], outputNode.inputs[0])
    bayerTexNode.image = bayerMatrix
    bayerTexNode.interpolation = 'Closest'

    # Creates the multiply node
    multiplyVector = ditherGroup.nodes.new(type = "ShaderNodeVectorMath")
    multiplyVector.location = (-500, -210)
    multiplyVector.operation = 'MULTIPLY'
    ditherGroup.links.new(multiplyVector.outputs[0], bayerTexNode.inputs[0])

    # Creates the Texture Coordinate node
    texCoordNode = ditherGroup.nodes.new(type = "ShaderNodeTexCoord")
    texCoordNode.location = (-700, -100)
    ditherGroup.links.new(texCoordNode.outputs[5], multiplyVector.inputs[0])

    # Creates the combineXYZ node
    combineXyzNode = ditherGroup.nodes.new(type = "ShaderNodeCombineXYZ")
    combineXyzNode.location = (-700, -400)
    ditherGroup.links.new(combineXyzNode.outputs[0], multiplyVector.inputs[1])

    # Creates the Resolution nodes
    resolutionXnode = ditherGroup.nodes.new(type = "ShaderNodeValue")
    resolutionXnode.location = (-900, -400)
    resolutionXnode.label = "ResolutionX / 2"
    ditherGroup.links.new(resolutionXnode.outputs[0], combineXyzNode.inputs[0])

    resolutionXdriver = resolutionXnode.outputs['Value'].driver_add("default_value")
    var1 = resolutionXdriver.driver.variables.new()
    var1.name = "resolutionX"
    var1.targets[0].id_type = 'SCENE'
    var1.targets[0].id = bpy.data.scenes["Scene"]
    var1.targets[0].data_path = "render.resolution_x"
    resolutionXdriver.driver.expression = "resolutionX / 2"

    resolutionYnode = ditherGroup.nodes.new(type = "ShaderNodeValue")
    resolutionYnode.location = (-900, -500)
    resolutionYnode.label = "ResolutionY / 2"
    ditherGroup.links.new(resolutionYnode.outputs[0], combineXyzNode.inputs[1])

    resolutionYdriver = resolutionYnode.outputs['Value'].driver_add("default_value")
    var2 = resolutionYdriver.driver.variables.new()
    var2.name = "resolutionY"
    var2.targets[0].id_type = 'SCENE'
    var2.targets[0].id = bpy.data.scenes["Scene"]
    var2.targets[0].data_path = "render.resolution_y"
    resolutionYdriver.driver.expression = "resolutionY / 2"

    # Creates the two mix RGB
    emissionOutputNode = material.node_tree.nodes.new(type = "ShaderNodeEmission")
    emissionOutputNode.location = (100, 300)
    material.node_tree.links.new(emissionOutputNode.outputs[0], materialOutput.inputs[0])

    mixShaderNode1 = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixShaderNode1.location = (-150, 300)
    mixShaderNode1.blend_type = 'LIGHTEN'
    material.node_tree.links.new(mixShaderNode1.outputs[0], emissionOutputNode.inputs[0])

    mixShaderNode2 = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixShaderNode2.location = (-400, 100)
    mixShaderNode2.blend_type = 'LIGHTEN'    
    material.node_tree.links.new(mixShaderNode2.outputs[0], mixShaderNode1.inputs[2])

    ### RED CHANNEL ###
    # Creates the color ramp node
    colorRampNode = material.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    colorRampNode.location = (-850,600)
    material.node_tree.links.new(colorRampNode.outputs[0], mixShaderNode1.inputs[1])
    colorRampNode.color_ramp.interpolation = 'CONSTANT'
    colorRampNode.color_ramp.elements.remove(colorRampNode.color_ramp.elements[1])
    colorRampNode.color_ramp.elements.new(0.01)
    colorRampNode.color_ramp.elements.new(0.075)
    colorRampNode.color_ramp.elements.new(0.225)
    colorRampNode.color_ramp.elements.new(0.450)
    colorRampNode.color_ramp.elements.new(0.800)

    colorRampNode.color_ramp.elements[0].color = [0, 0, 0, 1.000000]
    colorRampNode.color_ramp.elements[1].color = [0.191202, 0.033105, 0.063010, 1.000000]
    colorRampNode.color_ramp.elements[2].color = [0.337164, 0.063010, 0.045186, 1.000000]
    colorRampNode.color_ramp.elements[3].color = [0.603828, 0.138432, 0.049707, 1.000000]
    colorRampNode.color_ramp.elements[4].color = [0.783538, 0.274677, 0.078187, 1.000000]
    colorRampNode.color_ramp.elements[5].color = [0.955974, 0.473532, 0.090842, 1.000000]

    # Creates the mixRGB soft light node
    mixSoftLightNode = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixSoftLightNode.location = (-1100, 600)
    mixSoftLightNode.blend_type = 'SOFT_LIGHT'
    mixSoftLightNode.inputs[0].default_value = 0.2
    material.node_tree.links.new(mixSoftLightNode.outputs[0], colorRampNode.inputs[0])

    # Adds the dithering node group to the tree
    ditherGroupNode = material.node_tree.nodes.new("ShaderNodeGroup")
    ditherGroupNode.node_tree = ditherGroup
    ditherGroupNode.location = (-1300, 600)
    material.node_tree.links.new(ditherGroupNode.outputs[0], mixSoftLightNode.inputs[2])

    ### GREEN CHANNEL ###
    # Creates the color ramp node
    colorRampNodeG = material.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    colorRampNodeG.location = (-850,200)
    material.node_tree.links.new(colorRampNodeG.outputs[0], mixShaderNode2.inputs[1])
    colorRampNodeG.color_ramp.interpolation = 'CONSTANT'
    colorRampNodeG.color_ramp.elements.remove(colorRampNodeG.color_ramp.elements[1])
    colorRampNodeG.color_ramp.elements.new(0.01)
    colorRampNodeG.color_ramp.elements.new(0.075)
    colorRampNodeG.color_ramp.elements.new(0.225)
    colorRampNodeG.color_ramp.elements.new(0.450)
    colorRampNodeG.color_ramp.elements.new(0.800)

    colorRampNodeG.color_ramp.elements[0].color = [0, 0, 0, 1.000000]
    colorRampNodeG.color_ramp.elements[1].color = [0.011612, 0.102242, 0.074214, 1.000000]
    colorRampNodeG.color_ramp.elements[2].color = [0.011612, 0.102242, 0.074214, 1.000000]
    colorRampNodeG.color_ramp.elements[3].color = [0.016807, 0.496933, 0.168269, 1.000000]
    colorRampNodeG.color_ramp.elements[4].color = [0.278894, 0.701102, 0.141263, 1.000000]
    colorRampNodeG.color_ramp.elements[5].color = [0.603828, 0.730461, 0.149960, 1.000000]

    # Creates the mixRGB soft light node
    mixSoftLightNodeG = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixSoftLightNodeG.location = (-1100, 200)
    mixSoftLightNodeG.blend_type = 'SOFT_LIGHT'
    mixSoftLightNodeG.inputs[0].default_value = 0.2
    material.node_tree.links.new(mixSoftLightNodeG.outputs[0], colorRampNodeG.inputs[0])

    # Adds the dithering node group to the tree
    ditherGroupNodeG = material.node_tree.nodes.new("ShaderNodeGroup")
    ditherGroupNodeG.node_tree = ditherGroup
    ditherGroupNodeG.location = (-1300, 200)
    material.node_tree.links.new(ditherGroupNodeG.outputs[0], mixSoftLightNodeG.inputs[2])

    ### BLUE CHANNEL ###
    # Creates the color ramp node
    colorRampNodeB = material.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    colorRampNodeB.location = (-850,-100)
    material.node_tree.links.new(colorRampNodeB.outputs[0], mixShaderNode2.inputs[2])
    colorRampNodeB.color_ramp.interpolation = 'CONSTANT'
    colorRampNodeB.color_ramp.elements.remove(colorRampNodeB.color_ramp.elements[1])
    colorRampNodeB.color_ramp.elements.new(0.01)
    colorRampNodeB.color_ramp.elements.new(0.075)
    colorRampNodeB.color_ramp.elements.new(0.225)
    colorRampNodeB.color_ramp.elements.new(0.450)
    colorRampNodeB.color_ramp.elements.new(0.800)

    colorRampNodeB.color_ramp.elements[0].color = [0, 0, 0, 1.000000]
    colorRampNodeB.color_ramp.elements[1].color = [0.035601, 0.036889, 0.088656, 1.000000]
    colorRampNodeB.color_ramp.elements[2].color = [0.068478, 0.070360, 0.181164, 1.000000]
    colorRampNodeB.color_ramp.elements[3].color = [0.076185, 0.130137, 0.450786, 1.000000]
    colorRampNodeB.color_ramp.elements[4].color = [0.076185, 0.323143, 0.783538, 1.000000]
    colorRampNodeB.color_ramp.elements[5].color = [0.270498, 0.644480, 1.000000, 1.000000]

    # Creates the mixRGB soft light node
    mixSoftLightNodeB = material.node_tree.nodes.new(type = "ShaderNodeMixRGB")
    mixSoftLightNodeB.location = (-1100, -100)
    mixSoftLightNodeB.blend_type = 'SOFT_LIGHT'
    mixSoftLightNodeB.inputs[0].default_value = 0.2
    material.node_tree.links.new(mixSoftLightNodeB.outputs[0], colorRampNodeB.inputs[0])

    # Adds the dithering node group to the tree
    ditherGroupNodeB = material.node_tree.nodes.new("ShaderNodeGroup")
    ditherGroupNodeB.node_tree = ditherGroup
    ditherGroupNodeB.location = (-1300, -100)
    material.node_tree.links.new(ditherGroupNodeB.outputs[0], mixSoftLightNodeB.inputs[2])

    # Creates the shader to RGB node
    shaderToRgbNode = material.node_tree.nodes.new(type = "ShaderNodeShaderToRGB")
    shaderToRgbNode.location = (-2200, 0)

    # Creates the separate color node
    separateColorNode = material.node_tree.nodes.new(type = "ShaderNodeSeparateColor")
    separateColorNode.location = (-2000, 0)
    material.node_tree.links.new(shaderToRgbNode.outputs[0], separateColorNode.inputs[0])
    material.node_tree.links.new(separateColorNode.outputs[0], mixSoftLightNode.inputs[1])
    material.node_tree.links.new(separateColorNode.outputs[1], mixSoftLightNodeG.inputs[1])
    material.node_tree.links.new(separateColorNode.outputs[2], mixSoftLightNodeB.inputs[1])

    # Creates the principled BSDF node
    bsdfNode = material.node_tree.nodes.new(type = "ShaderNodeBsdfPrincipled")
    bsdfNode.location = (-2500, 0)
    material.node_tree.links.new(bsdfNode.outputs[0], shaderToRgbNode.inputs[0])

def multiple_material_shine(self, context):
    multiple_material(context)

    mat = None

    for material in bpy.data.materials:
        if material.name == "PixelArt_MultipleLights":
            mat = material

    if mat is None:
        self.report({'ERROR'}, "No PixelArt material found. This should not be possible... good luck")
        return
    
    nodes = mat.node_tree.nodes
    # Get pre-existing nodes
    material_output = nodes.get("Material Output")
    emission = nodes.get("Emission")
    # Could either be Mix (Legacy) or Mix (Legacy).003
    legacy_mix = nodes.get("Mix (Legacy)")

    # Disconnect mix legacy (lighten) and emission nodes
    link = legacy_mix.outputs[0].links[0]
    legacy_mix.id_data.links.remove(link)

    # Move material output and emission nodes
    material_output.location = (600, 300)
    emission.location = (400, 300)

    # Create new nodes
    shine_group = nodes.new(type="ShaderNodeGroup")
    shine_group.node_tree = bpy.data.node_groups["Shine Reflection"]
    shine_group.location = (-45, 95)

    # Value nodes for rotation and scale of shine group
    value_rot = nodes.new(type="ShaderNodeValue")
    value_rot.location = (-235, -35)
    value_rot.label = "Shine Rotation"
    value_rot.outputs[0].default_value = 2.5

    value_scale = nodes.new(type="ShaderNodeValue")
    value_scale.location = (-235, -125)
    value_scale.label = "Shine Scale"
    value_scale.outputs[0].default_value = 1

    # Create color mixing node and set correct settings before use
    mix_node = nodes.new(type="ShaderNodeMixRGB")
    mix_node.location = (165, 265)
    mix_node.blend_type = 'ADD'

    # Connect nodes
    links = mat.node_tree.links

    links.new(value_rot.outputs[0], shine_group.inputs['Rotation'])
    links.new(value_scale.outputs[0], shine_group.inputs['Scale'])
    links.new(shine_group.outputs[0], mix_node.inputs['Color2'])
    links.new(legacy_mix.outputs['Color'], mix_node.inputs['Color1'])
    links.new(mix_node.outputs[0], emission.inputs['Color'])

########## Creates Tri Lights Setup ##########
def lights_setup(context):
    
    # Deletes previous light sources with the same name
    for obj in bpy.data.objects:
        if obj.name.startswith("PixelArt_Light_"):
            bpy.data.objects.remove(obj, do_unlink = True)

    for light in bpy.data.lights:
        if light.name.startswith("PixelArt_Light_"):
            bpy.data.lights.remove(light, do_unlink = True)

    # Creates the red light
    lightR = bpy.data.lights.new(name = "PixelArt_Light_R", type = 'POINT')
    lightR.color = (1,0,0)
    lightR.energy = 250
    lightR_object = bpy.data.objects.new(name = "PixelArt_Light_R", object_data = lightR)
    bpy.context.collection.objects.link(lightR_object)
    lightR_object.location = (3.46, -0.41, 1.04)

    # Creates the green light
    lightG = bpy.data.lights.new(name = "PixelArt_Light_G", type = 'POINT')
    lightG.color = (0,1,0)
    lightG.energy = 250
    lightG_object = bpy.data.objects.new(name = "PixelArt_Light_G", object_data = lightG)
    bpy.context.collection.objects.link(lightG_object)
    lightG_object.location = (-2.1, 2, 1.37)

    # Creates the blue light
    lightB = bpy.data.lights.new(name = "PixelArt_Light_B", type = 'POINT')
    lightB.color = (0,0,1)
    lightB.energy = 150
    lightB_object = bpy.data.objects.new(name = "PixelArt_Light_B", object_data = lightB)
    bpy.context.collection.objects.link(lightB_object)
    lightB_object.location = (-0.06, -1.46, 2.18)

    # Removes world light
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0

def create_emitter():
    verts = [(-2, -2, 0), (-2, 2, 0), (2, 2, 0), (2, -2, 0)]
    faces = [(0, 1, 2, 3)]
    
    mesh = bpy.data.meshes.new("Emitter (Won't render)")
    emitter = bpy.data.objects.new("Emitter (Won't render)", mesh)
    bpy.context.collection.objects.link(emitter)

    mesh.from_pydata(verts,[],faces)

    emitter.modifiers.new("ParticleSystem", type='PARTICLE_SYSTEM')
    ps = emitter.particle_systems[0]
    pss = ps.settings

    pss.lifetime = 60
    pss.lifetime_random = 0.5
    pss.object_align_factor = (0, 0, 10)
    pss.effector_weights.gravity = 0
    pss.render_type = 'OBJECT'
    pss.particle_size = 1
    pss.use_scale_instance = True
    pss.size_random = 1

    emitter.show_instancer_for_render = False

    return pss

def create_smoke():
    emitter = create_emitter()

    mat = None

    for material in bpy.data.materials:
        if material.name == "PixelSmoke_material":
            mat = material

    if mat is None:
        mat = single_material(bpy.context, "PixelSmoke_material")

    color_ramp_node = mat.node_tree.nodes.get("Color Ramp")
    mix_node = mat.node_tree.nodes.get("Mix (Legacy)")

    # Set dither fac
    mix_node.inputs[0].default_value = 1

    # Remove last two elements
    color_ramp_node.color_ramp.elements.remove(color_ramp_node.color_ramp.elements[4])
    color_ramp_node.color_ramp.elements.remove(color_ramp_node.color_ramp.elements[3])
    
    # Set new colors
    color_ramp_node.color_ramp.elements[0].color = [0.14, 0.15, 0.175, 1.000000]
    color_ramp_node.color_ramp.elements[1].color = [0.266, 0.301, 0.283, 1.000000]
    color_ramp_node.color_ramp.elements[2].color = [0.6, 0.52, 0.52, 1.000000]

    # Set correct positions
    color_ramp_node.color_ramp.elements[1].position = 0.255
    color_ramp_node.color_ramp.elements[2].position = 0.795

    # Set material to the particle
    particle = bpy.ops.object.metaball_add(type='BALL')
    particle = bpy.context.active_object
    bpy.ops.object.material_slot_add()
    particle.material_slots[0].material = mat

    emitter.instance_object = particle