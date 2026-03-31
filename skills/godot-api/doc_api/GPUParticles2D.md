## GPUParticles2D <- Node2D

2D particle node used to create a variety of particle systems and effects. GPUParticles2D features an emitter that generates some number of particles at a given rate. Use the `process_material` property to add a ParticleProcessMaterial to configure particle appearance and behavior. Alternatively, you can add a ShaderMaterial which will be applied to all particles. 2D particles can optionally collide with LightOccluder2D, but they don't collide with PhysicsBody2D nodes.

**Props:**
- amount: int = 8
- amount_ratio: float = 1.0
- collision_base_size: float = 1.0
- draw_order: int (GPUParticles2D.DrawOrder) = 1
- emitting: bool = true
- explosiveness: float = 0.0
- fixed_fps: int = 30
- fract_delta: bool = true
- interp_to_end: float = 0.0
- interpolate: bool = true
- lifetime: float = 1.0
- local_coords: bool = false
- one_shot: bool = false
- preprocess: float = 0.0
- process_material: Material
- randomness: float = 0.0
- seed: int = 0
- speed_scale: float = 1.0
- sub_emitter: NodePath = NodePath("")
- texture: Texture2D
- trail_enabled: bool = false
- trail_lifetime: float = 0.3
- trail_section_subdivisions: int = 4
- trail_sections: int = 8
- use_fixed_seed: bool = false
- visibility_rect: Rect2 = Rect2(-100, -100, 200, 200)

- **amount**: The number of particles to emit in one emission cycle. The effective emission rate is `(amount * amount_ratio) / lifetime` particles per second. Higher values will increase GPU requirements, even if not all particles are visible at a given time or if `amount_ratio` is decreased. **Note:** Changing this value will cause the particle system to restart. To avoid this, change `amount_ratio` instead.
- **amount_ratio**: The ratio of particles that should actually be emitted. If set to a value lower than `1.0`, this will set the amount of emitted particles throughout the lifetime to `amount * amount_ratio`. Unlike changing `amount`, changing `amount_ratio` while emitting does not affect already-emitted particles and doesn't cause the particle system to restart. `amount_ratio` can be used to create effects that make the number of emitted particles vary over time. **Note:** Reducing the `amount_ratio` has no performance benefit, since resources need to be allocated and processed for the total `amount` of particles regardless of the `amount_ratio`. If you don't intend to change the number of particles emitted while the particles are emitting, make sure `amount_ratio` is set to `1` and change `amount` to your liking instead.
- **collision_base_size**: Multiplier for particle's collision radius. `1.0` corresponds to the size of the sprite. If particles appear to sink into the ground when colliding, increase this value. If particles appear to float when colliding, decrease this value. Only effective if `ParticleProcessMaterial.collision_mode` is `ParticleProcessMaterial.COLLISION_RIGID` or `ParticleProcessMaterial.COLLISION_HIDE_ON_CONTACT`. **Note:** Particles always have a spherical collision shape.
- **draw_order**: Particle draw order.
- **emitting**: If `true`, particles are being emitted. `emitting` can be used to start and stop particles from emitting. However, if `one_shot` is `true` setting `emitting` to `true` will not restart the emission cycle unless all active particles have finished processing. Use the `finished` signal to be notified once all active particles finish processing. **Note:** For `one_shot` emitters, due to the particles being computed on the GPU, there may be a short period after receiving the `finished` signal during which setting this to `true` will not restart the emission cycle. **Tip:** If your `one_shot` emitter needs to immediately restart emitting particles once `finished` signal is received, consider calling `restart` instead of setting `emitting`.
- **explosiveness**: How rapidly particles in an emission cycle are emitted. If greater than `0`, there will be a gap in emissions before the next cycle begins.
- **fixed_fps**: The particle system's frame rate is fixed to a value. For example, changing the value to 2 will make the particles render at 2 frames per second. Note this does not slow down the simulation of the particle system itself.
- **fract_delta**: If `true`, results in fractional delta calculation which has a smoother particles display effect.
- **interp_to_end**: Causes all the particles in this node to interpolate towards the end of their lifetime. **Note:** This only works when used with a ParticleProcessMaterial. It needs to be manually implemented for custom process shaders.
- **interpolate**: Enables particle interpolation, which makes the particle movement smoother when their `fixed_fps` is lower than the screen refresh rate.
- **lifetime**: The amount of time each particle will exist (in seconds). The effective emission rate is `(amount * amount_ratio) / lifetime` particles per second.
- **local_coords**: If `true`, particles use the parent node's coordinate space (known as local coordinates). This will cause particles to move and rotate along the GPUParticles2D node (and its parents) when it is moved or rotated. If `false`, particles use global coordinates; they will not move or rotate along the GPUParticles2D node (and its parents) when it is moved or rotated.
- **one_shot**: If `true`, only one emission cycle occurs. If set `true` during a cycle, emission will stop at the cycle's end.
- **preprocess**: Particle system starts as if it had already run for this many seconds. **Note:** This can be very expensive if set to a high number as it requires running the particle shader a number of times equal to the `fixed_fps` (or 30, if `fixed_fps` is 0) for every second. In extreme cases it can even lead to a GPU crash due to the volume of work done in a single frame.
- **process_material**: Material for processing particles. Can be a ParticleProcessMaterial or a ShaderMaterial.
- **randomness**: Emission lifetime randomness ratio.
- **seed**: Sets the random seed used by the particle system. Only effective if `use_fixed_seed` is `true`.
- **speed_scale**: Particle system's running speed scaling ratio. A value of `0` can be used to pause the particles.
- **sub_emitter**: Path to another GPUParticles2D node that will be used as a subemitter (see `ParticleProcessMaterial.sub_emitter_mode`). Subemitters can be used to achieve effects such as fireworks, sparks on collision, bubbles popping into water drops, and more. **Note:** When `sub_emitter` is set, the target GPUParticles2D node will no longer emit particles on its own.
- **texture**: Particle texture. If `null`, particles will be squares with a size of 1×1 pixels. **Note:** To use a flipbook texture, assign a new CanvasItemMaterial to the GPUParticles2D's `CanvasItem.material` property, then enable `CanvasItemMaterial.particles_animation` and set `CanvasItemMaterial.particles_anim_h_frames`, `CanvasItemMaterial.particles_anim_v_frames`, and `CanvasItemMaterial.particles_anim_loop` to match the flipbook texture.
- **trail_enabled**: If `true`, enables particle trails using a mesh skinning system. **Note:** Unlike GPUParticles3D, the number of trail sections and subdivisions is set with the `trail_sections` and `trail_section_subdivisions` properties.
- **trail_lifetime**: The amount of time the particle's trail should represent (in seconds). Only effective if `trail_enabled` is `true`.
- **trail_section_subdivisions**: The number of subdivisions to use for the particle trail rendering. Higher values can result in smoother trail curves, at the cost of performance due to increased mesh complexity. See also `trail_sections`. Only effective if `trail_enabled` is `true`.
- **trail_sections**: The number of sections to use for the particle trail rendering. Higher values can result in smoother trail curves, at the cost of performance due to increased mesh complexity. See also `trail_section_subdivisions`. Only effective if `trail_enabled` is `true`.
- **use_fixed_seed**: If `true`, particles will use the same seed for every simulation using the seed defined in `seed`. This is useful for situations where the visual outcome should be consistent across replays, for example when using Movie Maker mode.
- **visibility_rect**: The Rect2 that determines the node's region which needs to be visible on screen for the particle system to be active. Grow the rect if particles suddenly appear/disappear when the node enters/exits the screen. The Rect2 can be grown via code or with the **Particles → Generate Visibility Rect** editor tool.

**Methods:**
- capture_rect() -> Rect2 - Returns a rectangle containing the positions of all existing particles. **Note:** When using threaded rendering this method synchronizes the rendering thread. Calling it often may have a negative impact on performance.
- convert_from_particles(particles: Node) - Sets this node's properties to match a given CPUParticles2D node.
- emit_particle(xform: Transform2D, velocity: Vector2, color: Color, custom: Color, flags: int) - Emits a single particle. Whether `xform`, `velocity`, `color` and `custom` are applied depends on the value of `flags`. See `EmitFlags`. The default ParticleProcessMaterial will overwrite `color` and use the contents of `custom` as `(rotation, age, animation, lifetime)`. **Note:** `emit_particle` is only supported on the Forward+ and Mobile rendering methods, not Compatibility.
- request_particles_process(process_time: float) - Requests the particles to process for extra process time during a single frame. Useful for particle playback, if used in combination with `use_fixed_seed` or by calling `restart` with parameter `keep_seed` set to `true`.
- restart(keep_seed: bool = false) - Restarts the particle emission cycle, clearing existing particles. To avoid particles vanishing from the viewport, wait for the `finished` signal before calling. **Note:** The `finished` signal is only emitted by `one_shot` emitters. If `keep_seed` is `true`, the current random seed will be preserved. Useful for seeking and playback.

**Signals:**
- finished - Emitted when all active particles have finished processing. To immediately restart the emission cycle, call `restart`. This signal is never emitted when `one_shot` is disabled, as particles will be emitted and processed continuously. **Note:** For `one_shot` emitters, due to the particles being computed on the GPU, there may be a short period after receiving the signal during which setting `emitting` to `true` will not restart the emission cycle. This delay is avoided by instead calling `restart`.

**Enums:**
**DrawOrder:** DRAW_ORDER_INDEX=0, DRAW_ORDER_LIFETIME=1, DRAW_ORDER_REVERSE_LIFETIME=2
  - DRAW_ORDER_INDEX: Particles are drawn in the order emitted.
  - DRAW_ORDER_LIFETIME: Particles are drawn in order of remaining lifetime. In other words, the particle with the highest lifetime is drawn at the front.
  - DRAW_ORDER_REVERSE_LIFETIME: Particles are drawn in reverse order of remaining lifetime. In other words, the particle with the lowest lifetime is drawn at the front.
**EmitFlags:** EMIT_FLAG_POSITION=1, EMIT_FLAG_ROTATION_SCALE=2, EMIT_FLAG_VELOCITY=4, EMIT_FLAG_COLOR=8, EMIT_FLAG_CUSTOM=16
  - EMIT_FLAG_POSITION: Particle starts at the specified position.
  - EMIT_FLAG_ROTATION_SCALE: Particle starts with specified rotation and scale.
  - EMIT_FLAG_VELOCITY: Particle starts with the specified velocity vector, which defines the emission direction and speed.
  - EMIT_FLAG_COLOR: Particle starts with specified color.
  - EMIT_FLAG_CUSTOM: Particle starts with specified `CUSTOM` data.

