# Pixel Art Rendering Addon (Mod)
Modified version of Lucas Roedel's Pixel Art Rendering Addon

## Features
* Easily pixelates 3D renders
* Supports interaction between multiple lights
* Stylized shine effect

## Installation
1. Press the `Code` drop-down button
2. Press `Download ZIP` and store wherever you want
3. Open Blender and press `Edit (in the top left) -> Preferences -> Add-ons -> Install`
4. Find the `ZIP` file and double click it
5. Click on the checkbox next to the add-on

## Usage
This [video](https://www.youtube.com/watch?v=vzIVn3G1Z2U&t=8s) explains the basic usage of the tool. Below are more details on the newly added features and advanced use cases.

### New additions
A stylized, anime-like shine effect has been added. Two new buttons allow you to easily add this effect to pixel materials—compatible with both single- and multi-light setups.
* Adjust the `Fac` value on the final `Add` node to control the opacity of the shine. A higher `Fac` value makes the shine more opaque.
* Use the `Shine Reflection` node to tweak the shine’s color, rotation, scale, and screen position. These values often require tuning per object. To fine-tune further, try disconnecting the `Shine Scale` and/or `Shine Rotation` inputs.

### Advanced Use
#### Reflections
To get reflections to work with this add-on, you will need to use `Light Probe Planes`. Based on testing in Blender 4.1, no other method produces accurate reflections with pixel materials.
* Set `Roughness` low and `Metallic` high on the reflective object.
* Adding subtle backlighting can help make reflections more visible.

#### Textures
Using an image texture as the base color on the `Principled BSDF` node is supported. However, detailed textures tend to clutter the pixelated result.
* Prefer simple or stylized textures.
* Alternatively, add texture overlays in post using external software.

`Normal Maps` also work for this add-on. However, regular `Normal Maps` will most likely result in a cluttered result.
* Creating new maps with a pixel art software, like `Aseprite`, with no anti-aliasing, can give a good result.
* Alternatively, maps with less details may also work.

#### Translucency
Pixel materials do not support translucency. To create effects like glass:
* Use a basic Blender material instead.
* To match the pixel style, you can:
  - Add the `Shine Reflection` node group.
  - Use a pixelated texture that blends into the scene. You can use [this](https://github.com/Tramshy/tex-pixelation-baking) Blender addon to achieve a pixelated look on textures.

## IMPORTANT:
This is a modified version of Lucas Roedel's original add-on. It includes bug fixes and improvements aimed at making the code more readable and easier to extend.
You can find the original code [here](https://lucasroedel.gumroad.com/l/pixel_art) — I highly recommend checking it out and leaving him a tip if you find it useful.

## License
This add-on is licensed under the GNU GPLv3 License. For more information read: `LICENSE`.
