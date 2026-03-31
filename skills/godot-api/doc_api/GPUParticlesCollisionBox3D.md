## GPUParticlesCollisionBox3D <- GPUParticlesCollision3D

A box-shaped 3D particle collision shape affecting GPUParticles3D nodes. Particle collision shapes work in real-time and can be moved, rotated and scaled during gameplay. Unlike attractors, non-uniform scaling of collision shapes is *not* supported. **Note:** `ParticleProcessMaterial.collision_mode` must be `ParticleProcessMaterial.COLLISION_RIGID` or `ParticleProcessMaterial.COLLISION_HIDE_ON_CONTACT` on the GPUParticles3D's process material for collision to work. **Note:** Particle collision only affects GPUParticles3D, not CPUParticles3D.

**Props:**
- size: Vector3 = Vector3(2, 2, 2)

- **size**: The collision box's size in 3D units.

