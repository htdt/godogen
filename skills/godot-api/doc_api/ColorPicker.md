## ColorPicker <- VBoxContainer

A widget that provides an interface for selecting or modifying a color. It can optionally provide functionalities like a color sampler (eyedropper), color modes, and presets. **Note:** This control is the color picker widget itself. You can use a ColorPickerButton instead if you need a button that brings up a ColorPicker in a popup.

**Props:**
- can_add_swatches: bool = true
- color: Color = Color(1, 1, 1, 1)
- color_mode: int (ColorPicker.ColorModeType) = 0
- color_modes_visible: bool = true
- deferred_mode: bool = false
- edit_alpha: bool = true
- edit_intensity: bool = true
- hex_visible: bool = true
- picker_shape: int (ColorPicker.PickerShapeType) = 0
- presets_visible: bool = true
- sampler_visible: bool = true
- sliders_visible: bool = true

- **can_add_swatches**: If `true`, it's possible to add presets under Swatches. If `false`, the button to add presets is disabled.
- **color**: The currently selected color.
- **color_mode**: The currently selected color mode.
- **color_modes_visible**: If `true`, the color mode buttons are visible.
- **deferred_mode**: If `true`, the color will apply only after the user releases the mouse button, otherwise it will apply immediately even in mouse motion event (which can cause performance issues).
- **edit_alpha**: If `true`, shows an alpha channel slider (opacity).
- **edit_intensity**: If `true`, shows an intensity slider. The intensity is applied as follows: convert the color to linear encoding, multiply it by `2 ** intensity`, and then convert it back to nonlinear sRGB encoding.
- **hex_visible**: If `true`, the hex color code input field is visible.
- **picker_shape**: The shape of the color space view.
- **presets_visible**: If `true`, the Swatches and Recent Colors presets are visible.
- **sampler_visible**: If `true`, the color sampler and color preview are visible.
- **sliders_visible**: If `true`, the color sliders are visible.

**Methods:**
- add_preset(color: Color) - Adds the given color to a list of color presets. The presets are displayed in the color picker and the user will be able to select them. **Note:** The presets list is only for *this* color picker.
- add_recent_preset(color: Color) - Adds the given color to a list of color recent presets so that it can be picked later. Recent presets are the colors that were picked recently, a new preset is automatically created and added to recent presets when you pick a new color. **Note:** The recent presets list is only for *this* color picker.
- erase_preset(color: Color) - Removes the given color from the list of color presets of this color picker.
- erase_recent_preset(color: Color) - Removes the given color from the list of color recent presets of this color picker.
- get_presets() -> PackedColorArray - Returns the list of colors in the presets of the color picker.
- get_recent_presets() -> PackedColorArray - Returns the list of colors in the recent presets of the color picker.

**Signals:**
- color_changed(color: Color) - Emitted when the color is changed.
- preset_added(color: Color) - Emitted when a preset is added.
- preset_removed(color: Color) - Emitted when a preset is removed.

**Enums:**
**ColorModeType:** MODE_RGB=0, MODE_HSV=1, MODE_RAW=2, MODE_LINEAR=2, MODE_OKHSL=3
  - MODE_RGB: Allows editing the color with Red/Green/Blue sliders in sRGB color space.
  - MODE_HSV: Allows editing the color with Hue/Saturation/Value sliders.
  - MODE_LINEAR: Allows editing the color with Red/Green/Blue sliders in linear color space.
  - MODE_OKHSL: Allows editing the color with Hue/Saturation/Lightness sliders. OKHSL is a new color space similar to HSL but that better match perception by leveraging the Oklab color space which is designed to be simple to use, while doing a good job at predicting perceived lightness, chroma and hue.
**PickerShapeType:** SHAPE_HSV_RECTANGLE=0, SHAPE_HSV_WHEEL=1, SHAPE_VHS_CIRCLE=2, SHAPE_OKHSL_CIRCLE=3, SHAPE_NONE=4, SHAPE_OK_HS_RECTANGLE=5, SHAPE_OK_HL_RECTANGLE=6
  - SHAPE_HSV_RECTANGLE: HSV Color Model rectangle color space.
  - SHAPE_HSV_WHEEL: HSV Color Model rectangle color space with a wheel.
  - SHAPE_VHS_CIRCLE: HSV Color Model circle color space. Use Saturation as a radius.
  - SHAPE_OKHSL_CIRCLE: HSL OK Color Model circle color space.
  - SHAPE_NONE: The color space shape and the shape select button are hidden. Can't be selected from the shapes popup.
  - SHAPE_OK_HS_RECTANGLE: OKHSL Color Model rectangle with constant lightness.
  - SHAPE_OK_HL_RECTANGLE: OKHSL Color Model rectangle with constant saturation.

