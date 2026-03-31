## World2D <- Resource

Class that has everything pertaining to a 2D world: A physics space, a canvas, and a sound space. 2D nodes register their resources into the current 2D world.

**Props:**
- canvas: RID
- direct_space_state: PhysicsDirectSpaceState2D
- navigation_map: RID
- space: RID

- **canvas**: The RID of this world's canvas resource. Used by the RenderingServer for 2D drawing.
- **direct_space_state**: Direct access to the world's physics 2D space state. Used for querying current and potential collisions. When using multi-threaded physics, access is limited to `Node._physics_process` in the main thread.
- **navigation_map**: The RID of this world's navigation map. Used by the NavigationServer2D.
- **space**: The RID of this world's physics space resource. Used by the PhysicsServer2D for 2D physics, treating it as both a space and an area.

