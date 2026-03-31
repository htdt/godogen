## VisualShaderNodeParticleEmitter <- VisualShaderNode

Particle emitter nodes can be used in "start" step of particle shaders and they define the starting position of the particles. Connect them to the Position output port.

**Props:**
- mode_2d: bool = false

- **mode_2d**: If `true`, the result of this emitter is projected to 2D space. By default it is `false` and meant for use in 3D space.

