## PhysicalSkyMaterial <- Material

The PhysicalSkyMaterial uses the Preetham analytic daylight model to draw a sky based on physical properties. This results in a substantially more realistic sky than the ProceduralSkyMaterial, but it is slightly slower and less flexible. The PhysicalSkyMaterial only supports one sun. The color, energy, and direction of the sun are taken from the first DirectionalLight3D in the scene tree.

**Props:**
- energy_multiplier: float = 1.0
- ground_color: Color = Color(0.1, 0.07, 0.034, 1)
- mie_coefficient: float = 0.005
- mie_color: Color = Color(0.69, 0.729, 0.812, 1)
- mie_eccentricity: float = 0.8
- night_sky: Texture2D
- rayleigh_coefficient: float = 2.0
- rayleigh_color: Color = Color(0.3, 0.405, 0.6, 1)
- sun_disk_scale: float = 1.0
- turbidity: float = 10.0
- use_debanding: bool = true

- **energy_multiplier**: The sky's overall brightness multiplier. Higher values result in a brighter sky.
- **ground_color**: Modulates the Color on the bottom half of the sky to represent the ground.
- **mie_coefficient**: Controls the strength of for the sky. Mie scattering results from light colliding with larger particles (like water). On earth, Mie scattering results in a whitish color around the sun and horizon.
- **mie_color**: Controls the Color of the effect. While not physically accurate, this allows for the creation of alien-looking planets.
- **mie_eccentricity**: Controls the direction of the . A value of `1` means that when light hits a particle it's passing through straight forward. A value of `-1` means that all light is scatter backwards.
- **night_sky**: Texture2D for the night sky. This is added to the sky, so if it is bright enough, it may be visible during the day.
- **rayleigh_coefficient**: Controls the strength of the . Rayleigh scattering results from light colliding with small particles. It is responsible for the blue color of the sky.
- **rayleigh_color**: Controls the Color of the . While not physically accurate, this allows for the creation of alien-looking planets. For example, setting this to a red Color results in a Mars-looking atmosphere with a corresponding blue sunset.
- **sun_disk_scale**: Sets the size of the sun disk. Default value is based on Sol's perceived size from Earth.
- **turbidity**: Sets the thickness of the atmosphere. High turbidity creates a foggy-looking atmosphere, while a low turbidity results in a clearer atmosphere.
- **use_debanding**: If `true`, enables debanding. Debanding adds a small amount of noise which helps reduce banding that appears from the smooth changes in color in the sky.

