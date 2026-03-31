## ThemeDB <- Object

This singleton provides access to static information about Theme resources used by the engine and by your projects. You can fetch the default engine theme, as well as your project configured theme. ThemeDB also contains fallback values for theme properties.

**Props:**
- fallback_base_scale: float = 1.0
- fallback_font: Font
- fallback_font_size: int = 16
- fallback_icon: Texture2D
- fallback_stylebox: StyleBox

- **fallback_base_scale**: The fallback base scale factor of every Control node and Theme resource. Used when no other value is available to the control. See also `Theme.default_base_scale`.
- **fallback_font**: The fallback font of every Control node and Theme resource. Used when no other value is available to the control. See also `Theme.default_font`.
- **fallback_font_size**: The fallback font size of every Control node and Theme resource. Used when no other value is available to the control. See also `Theme.default_font_size`.
- **fallback_icon**: The fallback icon of every Control node and Theme resource. Used when no other value is available to the control.
- **fallback_stylebox**: The fallback stylebox of every Control node and Theme resource. Used when no other value is available to the control.

**Methods:**
- get_default_theme() -> Theme - Returns a reference to the default engine Theme. This theme resource is responsible for the out-of-the-box look of Control nodes and cannot be overridden.
- get_project_theme() -> Theme - Returns a reference to the custom project Theme. This theme resources allows to override the default engine theme for every control node in the project. To set the project theme, see `ProjectSettings.gui/theme/custom`.

**Signals:**
- fallback_changed - Emitted when one of the fallback values had been changed. Use it to refresh the look of controls that may rely on the fallback theme items.

