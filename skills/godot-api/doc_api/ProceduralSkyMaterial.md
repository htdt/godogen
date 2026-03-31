## ProceduralSkyMaterial <- Material

ProceduralSkyMaterial provides a way to create an effective background quickly by defining procedural parameters for the sun, the sky and the ground. The sky and ground are defined by a main color, a color at the horizon, and an easing curve to interpolate between them. Suns are described by a position in the sky, a color, and a max angle from the sun at which the easing curve ends. The max angle therefore defines the size of the sun in the sky. ProceduralSkyMaterial supports up to 4 suns, using the color, and energy, direction, and angular distance of the first four DirectionalLight3D nodes in the scene. This means that the suns are defined individually by the properties of their corresponding DirectionalLight3Ds and globally by `sun_angle_max` and `sun_curve`. ProceduralSkyMaterial uses a lightweight shader to draw the sky and is therefore suited for real-time updates. This makes it a great option for a sky that is simple and computationally cheap, but unrealistic. If you need a more realistic procedural option, use PhysicalSkyMaterial.

**Props:**
- energy_multiplier: float = 1.0
- ground_bottom_color: Color = Color(0.2, 0.169, 0.133, 1)
- ground_curve: float = 0.02
- ground_energy_multiplier: float = 1.0
- ground_horizon_color: Color = Color(0.6463, 0.6558, 0.6708, 1)
- sky_cover: Texture2D
- sky_cover_modulate: Color = Color(1, 1, 1, 1)
- sky_curve: float = 0.15
- sky_energy_multiplier: float = 1.0
- sky_horizon_color: Color = Color(0.6463, 0.6558, 0.6708, 1)
- sky_top_color: Color = Color(0.385, 0.454, 0.55, 1)
- sun_angle_max: float = 30.0
- sun_curve: float = 0.15
- use_debanding: bool = true

- **energy_multiplier**: The sky's overall brightness multiplier. Higher values result in a brighter sky.
- **ground_bottom_color**: Color of the ground at the bottom. Blends with `ground_horizon_color`.
- **ground_curve**: How quickly the `ground_horizon_color` fades into the `ground_bottom_color`.
- **ground_energy_multiplier**: Multiplier for ground color. A higher value will make the ground brighter.
- **ground_horizon_color**: Color of the ground at the horizon. Blends with `ground_bottom_color`.
- **sky_cover**: The sky cover texture to use. This texture must use an equirectangular projection (similar to PanoramaSkyMaterial). The texture's colors will be *added* to the existing sky color, and will be multiplied by `sky_energy_multiplier` and `sky_cover_modulate`. This is mainly suited to displaying stars at night, but it can also be used to display clouds at day or night (with a non-physically-accurate look).
- **sky_cover_modulate**: The tint to apply to the `sky_cover` texture. This can be used to change the sky cover's colors or opacity independently of the sky energy, which is useful for day/night or weather transitions. Only effective if a texture is defined in `sky_cover`.
- **sky_curve**: How quickly the `sky_horizon_color` fades into the `sky_top_color`.
- **sky_energy_multiplier**: Multiplier for sky color. A higher value will make the sky brighter.
- **sky_horizon_color**: Color of the sky at the horizon. Blends with `sky_top_color`.
- **sky_top_color**: Color of the sky at the top. Blends with `sky_horizon_color`.
- **sun_angle_max**: Distance from center of sun where it fades out completely.
- **sun_curve**: How quickly the sun fades away between the edge of the sun disk and `sun_angle_max`.
- **use_debanding**: If `true`, enables debanding. Debanding adds a small amount of noise which helps reduce banding that appears from the smooth changes in color in the sky.

