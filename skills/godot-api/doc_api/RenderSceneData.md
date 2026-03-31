## RenderSceneData <- Object

Abstract scene data object, exists for the duration of rendering a single viewport. See also RenderSceneDataRD, RenderData, and RenderDataRD. **Note:** This is an internal rendering server object. Do not instantiate this class from a script.

**Methods:**
- get_cam_projection() -> Projection - Returns the camera projection used to render this frame. **Note:** If more than one view is rendered, this will return a combined projection.
- get_cam_transform() -> Transform3D - Returns the camera transform used to render this frame. **Note:** If more than one view is rendered, this will return a centered transform.
- get_uniform_buffer() -> RID - Return the RID of the uniform buffer containing the scene data as a UBO.
- get_view_count() -> int - Returns the number of views being rendered.
- get_view_eye_offset(view: int) -> Vector3 - Returns the eye offset per view used to render this frame. This is the offset between our camera transform and the eye transform.
- get_view_projection(view: int) -> Projection - Returns the view projection per view used to render this frame. **Note:** If a single view is rendered, this returns the camera projection. If more than one view is rendered, this will return a projection for the given view including the eye offset.

