## GPUParticlesAttractorSphere3D <- GPUParticlesAttractor3D

A spheroid-shaped attractor that influences particles from GPUParticles3D nodes. Can be used to attract particles towards its origin, or to push them away from its origin. Particle attractors work in real-time and can be moved, rotated and scaled during gameplay. Unlike collision shapes, non-uniform scaling of attractors is also supported. **Note:** Particle attractors only affect GPUParticles3D, not CPUParticles3D.

**Props:**
- radius: float = 1.0

- **radius**: The attractor sphere's radius in 3D units. **Note:** Stretched ellipses can be obtained by using non-uniform scaling on the GPUParticlesAttractorSphere3D node.

