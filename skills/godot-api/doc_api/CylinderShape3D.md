## CylinderShape3D <- Shape3D

A 3D cylinder shape, intended for use in physics. Usually used to provide a shape for a CollisionShape3D. **Note:** There are several known bugs with cylinder collision shapes. Using CapsuleShape3D or BoxShape3D instead is recommended. **Performance:** CylinderShape3D is fast to check collisions against, but it is slower than CapsuleShape3D, BoxShape3D, and SphereShape3D.

**Props:**
- height: float = 2.0
- radius: float = 0.5

- **height**: The cylinder's height.
- **radius**: The cylinder's radius.

