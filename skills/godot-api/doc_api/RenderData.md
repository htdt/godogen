## RenderData <- Object

Abstract render data object, exists for the duration of rendering a single viewport. See also RenderDataRD, RenderSceneData, and RenderSceneDataRD. **Note:** This is an internal rendering server object. Do not instantiate this class from a script.

**Methods:**
- get_camera_attributes() -> RID - Returns the RID of the camera attributes object in the RenderingServer being used to render this viewport.
- get_environment() -> RID - Returns the RID of the environment object in the RenderingServer being used to render this viewport.
- get_render_scene_buffers() -> RenderSceneBuffers - Returns the RenderSceneBuffers object managing the scene buffers for rendering this viewport.
- get_render_scene_data() -> RenderSceneData - Returns the RenderSceneData object managing this frames scene data.

