## PhysicsMaterial <- Resource

Holds physics-related properties of a surface, namely its roughness and bounciness. This class is used to apply these properties to a physics body.

**Props:**
- absorbent: bool = false
- bounce: float = 0.0
- friction: float = 1.0
- rough: bool = false

- **absorbent**: If `true`, subtracts the bounciness from the colliding object's bounciness instead of adding it.
- **bounce**: The body's bounciness. Values range from `0` (no bounce) to `1` (full bounciness). **Note:** Even with `bounce` set to `1.0`, some energy will be lost over time due to linear and angular damping. To have a physics body that preserves all its energy over time, set `bounce` to `1.0`, the body's linear damp mode to **Replace** (if applicable), its linear damp to `0.0`, its angular damp mode to **Replace** (if applicable), and its angular damp to `0.0`.
- **friction**: The body's friction. Values range from `0` (frictionless) to `1` (maximum friction).
- **rough**: If `true`, the physics engine will use the friction of the object marked as "rough" when two objects collide. If `false`, the physics engine will use the lowest friction of all colliding objects instead. If `true` for both colliding objects, the physics engine will use the highest friction.

