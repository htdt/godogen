## MultiMeshInstance2D <- Node2D

MultiMeshInstance2D is a specialized node to instance a MultiMesh resource in 2D. This can be faster to render compared to displaying many Sprite2D nodes with large transparent areas, especially if the nodes take up a lot of space on screen at high viewport resolutions. This is because using a mesh designed to fit the sprites' opaque areas will reduce GPU fill rate utilization (at the cost of increased vertex processing utilization). Usage is the same as MultiMeshInstance3D.

**Props:**
- multimesh: MultiMesh
- texture: Texture2D

- **multimesh**: The MultiMesh that will be drawn by the MultiMeshInstance2D.
- **texture**: The Texture2D that will be used if using the default CanvasItemMaterial. Can be accessed as `TEXTURE` in CanvasItem shader.

**Signals:**
- texture_changed - Emitted when the `texture` is changed.

