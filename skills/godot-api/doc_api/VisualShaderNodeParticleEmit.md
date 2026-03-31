## VisualShaderNodeParticleEmit <- VisualShaderNode

This node internally calls `emit_subparticle` shader method. It will emit a particle from the configured sub-emitter and also allows to customize how its emitted. Requires a sub-emitter assigned to the particles node with this shader.

**Props:**
- flags: int (VisualShaderNodeParticleEmit.EmitFlags) = 31

- **flags**: Flags used to override the properties defined in the sub-emitter's process material.

**Enums:**
**EmitFlags:** EMIT_FLAG_POSITION=1, EMIT_FLAG_ROT_SCALE=2, EMIT_FLAG_VELOCITY=4, EMIT_FLAG_COLOR=8, EMIT_FLAG_CUSTOM=16
  - EMIT_FLAG_POSITION: If enabled, the particle starts with the position defined by this node.
  - EMIT_FLAG_ROT_SCALE: If enabled, the particle starts with the rotation and scale defined by this node.
  - EMIT_FLAG_VELOCITY: If enabled,the particle starts with the velocity defined by this node.
  - EMIT_FLAG_COLOR: If enabled, the particle starts with the color defined by this node.
  - EMIT_FLAG_CUSTOM: If enabled, the particle starts with the `CUSTOM` data defined by this node.

