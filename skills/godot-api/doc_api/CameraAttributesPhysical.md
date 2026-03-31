## CameraAttributesPhysical <- CameraAttributes

CameraAttributesPhysical is used to set rendering settings based on a physically-based camera's settings. It is responsible for exposure, auto-exposure, and depth of field. When used in a WorldEnvironment it provides default settings for exposure, auto-exposure, and depth of field that will be used by all cameras without their own CameraAttributes, including the editor camera. When used in a Camera3D it will override any CameraAttributes set in the WorldEnvironment and will override the Camera3Ds `Camera3D.far`, `Camera3D.near`, `Camera3D.fov`, and `Camera3D.keep_aspect` properties. When used in VoxelGI or LightmapGI, only the exposure settings will be used. The default settings are intended for use in an outdoor environment, tips for settings for use in an indoor environment can be found in each setting's documentation. **Note:** Depth of field blur is only supported in the Forward+ and Mobile rendering methods, not Compatibility. **Note:** Auto-exposure is only supported in the Forward+ rendering method, not Mobile or Compatibility.

**Props:**
- auto_exposure_max_exposure_value: float = 10.0
- auto_exposure_min_exposure_value: float = -8.0
- exposure_aperture: float = 16.0
- exposure_shutter_speed: float = 100.0
- frustum_far: float = 4000.0
- frustum_focal_length: float = 35.0
- frustum_focus_distance: float = 10.0
- frustum_near: float = 0.05

- **auto_exposure_max_exposure_value**: The maximum luminance (in EV100) used when calculating auto exposure. When calculating scene average luminance, color values will be clamped to at least this value. This limits the auto-exposure from exposing below a certain brightness, resulting in a cut off point where the scene will remain bright.
- **auto_exposure_min_exposure_value**: The minimum luminance (in EV100) used when calculating auto exposure. When calculating scene average luminance, color values will be clamped to at least this value. This limits the auto-exposure from exposing above a certain brightness, resulting in a cut off point where the scene will remain dark.
- **exposure_aperture**: Size of the aperture of the camera, measured in f-stops. An f-stop is a unitless ratio between the focal length of the camera and the diameter of the aperture. A high aperture setting will result in a smaller aperture which leads to a dimmer image and sharper focus. A low aperture results in a wide aperture which lets in more light resulting in a brighter, less-focused image. Default is appropriate for outdoors at daytime (i.e. for use with a default DirectionalLight3D), for indoor lighting, a value between 2 and 4 is more appropriate. Only available when `ProjectSettings.rendering/lights_and_shadows/use_physical_light_units` is enabled.
- **exposure_shutter_speed**: Time for shutter to open and close, evaluated as `1 / shutter_speed` seconds. A higher value will allow less light (leading to a darker image), while a lower value will allow more light (leading to a brighter image). Only available when `ProjectSettings.rendering/lights_and_shadows/use_physical_light_units` is enabled.
- **frustum_far**: Override value for `Camera3D.far`. Used internally when calculating depth of field. When attached to a Camera3D as its `Camera3D.attributes`, it will override the `Camera3D.far` property.
- **frustum_focal_length**: Distance between camera lens and camera aperture, measured in millimeters. Controls field of view and depth of field. A larger focal length will result in a smaller field of view and a narrower depth of field meaning fewer objects will be in focus. A smaller focal length will result in a wider field of view and a larger depth of field meaning more objects will be in focus. When attached to a Camera3D as its `Camera3D.attributes`, it will override the `Camera3D.fov` property and the `Camera3D.keep_aspect` property.
- **frustum_focus_distance**: Distance from camera of object that will be in focus, measured in meters. Internally this will be clamped to be at least 1 millimeter larger than `frustum_focal_length`.
- **frustum_near**: Override value for `Camera3D.near`. Used internally when calculating depth of field. When attached to a Camera3D as its `Camera3D.attributes`, it will override the `Camera3D.near` property.

**Methods:**
- get_fov() -> float - Returns the vertical field of view that corresponds to the `frustum_focal_length`. This value is calculated internally whenever `frustum_focal_length` is changed.

