## VisualShaderNodeParticleAccelerator <- VisualShaderNode

Particle accelerator can be used in "process" step of particle shader. It will accelerate the particles. Connect it to the Velocity output port.

**Props:**
- mode: int (VisualShaderNodeParticleAccelerator.Mode) = 0

- **mode**: Defines in what manner the particles will be accelerated.

**Enums:**
**Mode:** MODE_LINEAR=0, MODE_RADIAL=1, MODE_TANGENTIAL=2, MODE_MAX=3
  - MODE_LINEAR: The particles will be accelerated based on their velocity.
  - MODE_RADIAL: The particles will be accelerated towards or away from the center.
  - MODE_TANGENTIAL: The particles will be accelerated tangentially to the radius vector from center to their position.
  - MODE_MAX: Represents the size of the `Mode` enum.

