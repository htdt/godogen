## World3D <- Resource

Class that has everything pertaining to a world: A physics space, a visual scenario, and a sound space. 3D nodes register their resources into the current 3D world.

**Props:**
- camera_attributes: CameraAttributes
- direct_space_state: PhysicsDirectSpaceState3D
- environment: Environment
- fallback_environment: Environment
- navigation_map: RID
- scenario: RID
- space: RID

- **camera_attributes**: The default CameraAttributes resource to use if none set on the Camera3D.
- **direct_space_state**: Direct access to the world's physics 3D space state. Used for querying current and potential collisions. When using multi-threaded physics, access is limited to `Node._physics_process` in the main thread.
- **environment**: The World3D's Environment.
- **fallback_environment**: The World3D's fallback environment will be used if `environment` fails or is missing.
- **navigation_map**: The RID of this world's navigation map. Used by the NavigationServer3D.
- **scenario**: The World3D's visual scenario.
- **space**: The World3D's physics space.

