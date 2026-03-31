## Material <- Resource

Material is a base resource used for coloring and shading geometry. All materials inherit from it and almost all VisualInstance3D derived nodes carry a Material. A few flags and parameters are shared between all material types and are configured here. Importantly, you can inherit from Material to create your own custom material type in script or in GDExtension.

**Props:**
- next_pass: Material
- render_priority: int

- **next_pass**: Sets the Material to be used for the next pass. This renders the object again using a different material. **Note:** `next_pass` materials are not necessarily drawn immediately after the source Material. Draw order is determined by material properties, `render_priority`, and distance to camera. **Note:** This only applies to StandardMaterial3Ds and ShaderMaterials with type "Spatial".
- **render_priority**: Sets the render priority for objects in 3D scenes. Higher priority objects will be sorted in front of lower priority objects. In other words, all objects with `render_priority` `1` will render on top of all objects with `render_priority` `0`. **Note:** This only applies to StandardMaterial3Ds and ShaderMaterials with type "Spatial". **Note:** This will not impact how transparent objects are sorted relative to opaque objects or how dynamic meshes will be sorted relative to other opaque meshes. This is because all transparent objects are drawn after all opaque objects and all dynamic opaque meshes are drawn before other opaque meshes.

**Methods:**
- _can_do_next_pass() -> bool - Only exposed for the purpose of overriding. You cannot call this function directly. Used internally to determine if `next_pass` should be shown in the editor or not.
- _can_use_render_priority() -> bool - Only exposed for the purpose of overriding. You cannot call this function directly. Used internally to determine if `render_priority` should be shown in the editor or not.
- _get_shader_mode() -> int - Only exposed for the purpose of overriding. You cannot call this function directly. Used internally by various editor tools.
- _get_shader_rid() -> RID - Only exposed for the purpose of overriding. You cannot call this function directly. Used internally by various editor tools. Used to access the RID of the Material's Shader.
- create_placeholder() -> Resource - Creates a placeholder version of this resource (PlaceholderMaterial).
- inspect_native_shader_code() - Only available when running in the editor. Opens a popup that visualizes the generated shader code, including all variants and internal shader code. See also `Shader.inspect_native_shader_code`.

**Enums:**
**Constants:** RENDER_PRIORITY_MAX=127, RENDER_PRIORITY_MIN=-128
  - RENDER_PRIORITY_MAX: Maximum value for the `render_priority` parameter.
  - RENDER_PRIORITY_MIN: Minimum value for the `render_priority` parameter.

