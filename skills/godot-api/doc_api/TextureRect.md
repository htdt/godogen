## TextureRect <- Control

A control that displays a texture, for example an icon inside a GUI. The texture's placement can be controlled with the `stretch_mode` property. It can scale, tile, or stay centered inside its bounding rectangle.

**Props:**
- expand_mode: int (TextureRect.ExpandMode) = 0
- flip_h: bool = false
- flip_v: bool = false
- mouse_filter: int (Control.MouseFilter) = 1
- stretch_mode: int (TextureRect.StretchMode) = 0
- texture: Texture2D

- **expand_mode**: Defines how minimum size is determined based on the texture's size.
- **flip_h**: If `true`, texture is flipped horizontally.
- **flip_v**: If `true`, texture is flipped vertically.
- **stretch_mode**: Controls the texture's behavior when resizing the node's bounding rectangle.
- **texture**: The node's Texture2D resource.

**Enums:**
**ExpandMode:** EXPAND_KEEP_SIZE=0, EXPAND_IGNORE_SIZE=1, EXPAND_FIT_WIDTH=2, EXPAND_FIT_WIDTH_PROPORTIONAL=3, EXPAND_FIT_HEIGHT=4, EXPAND_FIT_HEIGHT_PROPORTIONAL=5
  - EXPAND_KEEP_SIZE: The minimum size will be equal to texture size, i.e. TextureRect can't be smaller than the texture.
  - EXPAND_IGNORE_SIZE: The size of the texture won't be considered for minimum size calculation, so the TextureRect can be shrunk down past the texture size.
  - EXPAND_FIT_WIDTH: The height of the texture will be ignored. Minimum width will be equal to the current height. Useful for horizontal layouts, e.g. inside HBoxContainer.
  - EXPAND_FIT_WIDTH_PROPORTIONAL: Same as `EXPAND_FIT_WIDTH`, but keeps texture's aspect ratio.
  - EXPAND_FIT_HEIGHT: The width of the texture will be ignored. Minimum height will be equal to the current width. Useful for vertical layouts, e.g. inside VBoxContainer.
  - EXPAND_FIT_HEIGHT_PROPORTIONAL: Same as `EXPAND_FIT_HEIGHT`, but keeps texture's aspect ratio.
**StretchMode:** STRETCH_SCALE=0, STRETCH_TILE=1, STRETCH_KEEP=2, STRETCH_KEEP_CENTERED=3, STRETCH_KEEP_ASPECT=4, STRETCH_KEEP_ASPECT_CENTERED=5, STRETCH_KEEP_ASPECT_COVERED=6
  - STRETCH_SCALE: Scale to fit the node's bounding rectangle.
  - STRETCH_TILE: Tile inside the node's bounding rectangle. **Note:** `STRETCH_TILE` mode is not supported for `texture` set to an AtlasTexture with non-zero `AtlasTexture.margin`.
  - STRETCH_KEEP: The texture keeps its original size and stays in the bounding rectangle's top-left corner.
  - STRETCH_KEEP_CENTERED: The texture keeps its original size and stays centered in the node's bounding rectangle.
  - STRETCH_KEEP_ASPECT: Scale the texture to fit the node's bounding rectangle, but maintain the texture's aspect ratio.
  - STRETCH_KEEP_ASPECT_CENTERED: Scale the texture to fit the node's bounding rectangle, center it and maintain its aspect ratio.
  - STRETCH_KEEP_ASPECT_COVERED: Scale the texture so that the shorter side fits the bounding rectangle. The other side clips to the node's limits.

