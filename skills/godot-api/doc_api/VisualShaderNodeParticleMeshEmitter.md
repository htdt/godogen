## VisualShaderNodeParticleMeshEmitter <- VisualShaderNodeParticleEmitter

VisualShaderNodeParticleEmitter that makes the particles emitted in a shape of the assigned `mesh`. It will emit from the mesh's surfaces, either all or only the specified one.

**Props:**
- mesh: Mesh
- surface_index: int = 0
- use_all_surfaces: bool = true

- **mesh**: The Mesh that defines emission shape.
- **surface_index**: Index of the surface that emits particles. `use_all_surfaces` must be `false` for this to take effect.
- **use_all_surfaces**: If `true`, the particles will emit from all surfaces of the mesh.

