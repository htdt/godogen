## CapsuleShape3D <- Shape3D

A 3D capsule shape, intended for use in physics. Usually used to provide a shape for a CollisionShape3D. **Performance:** CapsuleShape3D is fast to check collisions against. It is faster than CylinderShape3D, but slower than SphereShape3D and BoxShape3D.

**Props:**
- height: float = 2.0
- mid_height: float
- radius: float = 0.5

- **height**: The capsule's full height, including the hemispheres. **Note:** The `height` of a capsule must be at least twice its `radius`. Otherwise, the capsule becomes a sphere. If the `height` is less than twice the `radius`, the properties adjust to a valid value.
- **mid_height**: The capsule's height, excluding the hemispheres. This is the height of the central cylindrical part in the middle of the capsule, and is the distance between the centers of the two hemispheres. This is a wrapper for `height`.
- **radius**: The capsule's radius. **Note:** The `radius` of a capsule cannot be greater than half of its `height`. Otherwise, the capsule becomes a sphere. If the `radius` is greater than half of the `height`, the properties adjust to a valid value.

