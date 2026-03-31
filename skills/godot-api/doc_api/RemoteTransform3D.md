## RemoteTransform3D <- Node3D

RemoteTransform3D pushes its own Transform3D to another Node3D derived Node (called the remote node) in the scene. It can be set to update another Node's position, rotation and/or scale. It can use either global or local coordinates.

**Props:**
- remote_path: NodePath = NodePath("")
- update_position: bool = true
- update_rotation: bool = true
- update_scale: bool = true
- use_global_coordinates: bool = true

- **remote_path**: The NodePath to the remote node, relative to the RemoteTransform3D's position in the scene.
- **update_position**: If `true`, the remote node's position is updated.
- **update_rotation**: If `true`, the remote node's rotation is updated.
- **update_scale**: If `true`, the remote node's scale is updated.
- **use_global_coordinates**: If `true`, global coordinates are used. If `false`, local coordinates are used.

**Methods:**
- force_update_cache() - RemoteTransform3D caches the remote node. It may not notice if the remote node disappears; `force_update_cache` forces it to update the cache again.

