## WorldEnvironment <- Node

The WorldEnvironment node is used to configure the default Environment for the scene. The parameters defined in the WorldEnvironment can be overridden by an Environment node set on the current Camera3D. Additionally, only one WorldEnvironment may be instantiated in a given scene at a time. The WorldEnvironment allows the user to specify default lighting parameters (e.g. ambient lighting), various post-processing effects (e.g. SSAO, DOF, Tonemapping), and how to draw the background (e.g. solid color, skybox). Usually, these are added in order to improve the realism/color balance of the scene.

**Props:**
- camera_attributes: CameraAttributes
- compositor: Compositor
- environment: Environment

- **camera_attributes**: The default CameraAttributes resource to use if none set on the Camera3D.
- **compositor**: The default Compositor resource to use if none set on the Camera3D.
- **environment**: The Environment resource used by this WorldEnvironment, defining the default properties.

