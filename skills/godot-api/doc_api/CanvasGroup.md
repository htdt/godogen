## CanvasGroup <- Node2D

Child CanvasItem nodes of a CanvasGroup are drawn as a single object. It allows to e.g. draw overlapping translucent 2D nodes without causing the overlapping sections to be more opaque than intended (set the `CanvasItem.self_modulate` property on the CanvasGroup to achieve this effect). **Note:** The CanvasGroup uses a custom shader to read from the backbuffer to draw its children. Assigning a Material to the CanvasGroup overrides the built-in shader. To duplicate the behavior of the built-in shader in a custom Shader, use the following: **Note:** Since CanvasGroup and `CanvasItem.clip_children` both utilize the backbuffer, children of a CanvasGroup who have their `CanvasItem.clip_children` set to anything other than `CanvasItem.CLIP_CHILDREN_DISABLED` will not function correctly.

**Props:**
- clear_margin: float = 10.0
- fit_margin: float = 10.0
- use_mipmaps: bool = false

- **clear_margin**: Sets the size of the margin used to expand the clearing rect of this CanvasGroup. This expands the area of the backbuffer that will be used by the CanvasGroup. A smaller margin will reduce the area of the backbuffer used which can increase performance, however if `use_mipmaps` is enabled, a small margin may result in mipmap errors at the edge of the CanvasGroup. Accordingly, this should be left as small as possible, but should be increased if artifacts appear along the edges of the canvas group.
- **fit_margin**: Sets the size of a margin used to expand the drawable rect of this CanvasGroup. The size of the CanvasGroup is determined by fitting a rect around its children then expanding that rect by `fit_margin`. This increases both the backbuffer area used and the area covered by the CanvasGroup both of which can reduce performance. This should be kept as small as possible and should only be expanded when an increased size is needed (e.g. for custom shader effects).
- **use_mipmaps**: If `true`, calculates mipmaps for the backbuffer before drawing the CanvasGroup so that mipmaps can be used in a custom ShaderMaterial attached to the CanvasGroup. Generating mipmaps has a performance cost so this should not be enabled unless required.

