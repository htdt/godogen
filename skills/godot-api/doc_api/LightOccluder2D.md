## LightOccluder2D <- Node2D

Occludes light cast by a Light2D, casting shadows. The LightOccluder2D must be provided with an OccluderPolygon2D in order for the shadow to be computed.

**Props:**
- occluder: OccluderPolygon2D
- occluder_light_mask: int = 1
- sdf_collision: bool = true

- **occluder**: The OccluderPolygon2D used to compute the shadow.
- **occluder_light_mask**: The LightOccluder2D's occluder light mask. The LightOccluder2D will cast shadows only from Light2D(s) that have the same light mask(s).
- **sdf_collision**: If enabled, the occluder will be part of a real-time generated signed distance field that can be used in custom shaders.

