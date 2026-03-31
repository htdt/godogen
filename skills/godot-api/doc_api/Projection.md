## Projection

A 4×4 matrix used for 3D projective transformations. It can represent transformations such as translation, rotation, scaling, shearing, and perspective division. It consists of four Vector4 columns. For purely linear transformations (translation, rotation, and scale), it is recommended to use Transform3D, as it is more performant and requires less memory. Used internally as Camera3D's projection matrix. **Note:** In a boolean context, a projection will evaluate to `false` if it's equal to `IDENTITY`. Otherwise, a projection will always evaluate to `true`.

**Props:**
- w: Vector4 = Vector4(0, 0, 0, 1)
- x: Vector4 = Vector4(1, 0, 0, 0)
- y: Vector4 = Vector4(0, 1, 0, 0)
- z: Vector4 = Vector4(0, 0, 1, 0)

- **w**: The projection matrix's W vector (column 3). Equivalent to array index `3`.
- **x**: The projection matrix's X vector (column 0). Equivalent to array index `0`.
- **y**: The projection matrix's Y vector (column 1). Equivalent to array index `1`.
- **z**: The projection matrix's Z vector (column 2). Equivalent to array index `2`.

**Methods:**
- create_depth_correction(flip_y: bool) -> Projection - Creates a new Projection that projects positions from a depth range of `-1` to `1` to one that ranges from `0` to `1`, and flips the projected positions vertically, according to `flip_y`.
- create_fit_aabb(aabb: AABB) -> Projection - Creates a new Projection that scales a given projection to fit around a given AABB in projection space.
- create_for_hmd(eye: int, aspect: float, intraocular_dist: float, display_width: float, display_to_lens: float, oversample: float, z_near: float, z_far: float) -> Projection - Creates a new Projection for projecting positions onto a head-mounted display with the given X:Y aspect ratio, distance between eyes, display width, distance to lens, oversampling factor, and depth clipping planes. `eye` creates the projection for the left eye when set to 1, or the right eye when set to 2.
- create_frustum(left: float, right: float, bottom: float, top: float, z_near: float, z_far: float) -> Projection - Creates a new Projection that projects positions in a frustum with the given clipping planes.
- create_frustum_aspect(size: float, aspect: float, offset: Vector2, z_near: float, z_far: float, flip_fov: bool = false) -> Projection - Creates a new Projection that projects positions in a frustum with the given size, X:Y aspect ratio, offset, and clipping planes. `flip_fov` determines whether the projection's field of view is flipped over its diagonal.
- create_light_atlas_rect(rect: Rect2) -> Projection - Creates a new Projection that projects positions into the given Rect2.
- create_orthogonal(left: float, right: float, bottom: float, top: float, z_near: float, z_far: float) -> Projection - Creates a new Projection that projects positions using an orthogonal projection with the given clipping planes.
- create_orthogonal_aspect(size: float, aspect: float, z_near: float, z_far: float, flip_fov: bool = false) -> Projection - Creates a new Projection that projects positions using an orthogonal projection with the given size, X:Y aspect ratio, and clipping planes. `flip_fov` determines whether the projection's field of view is flipped over its diagonal.
- create_perspective(fovy: float, aspect: float, z_near: float, z_far: float, flip_fov: bool = false) -> Projection - Creates a new Projection that projects positions using a perspective projection with the given Y-axis field of view (in degrees), X:Y aspect ratio, and clipping planes. `flip_fov` determines whether the projection's field of view is flipped over its diagonal.
- create_perspective_hmd(fovy: float, aspect: float, z_near: float, z_far: float, flip_fov: bool, eye: int, intraocular_dist: float, convergence_dist: float) -> Projection - Creates a new Projection that projects positions using a perspective projection with the given Y-axis field of view (in degrees), X:Y aspect ratio, and clipping distances. The projection is adjusted for a head-mounted display with the given distance between eyes and distance to a point that can be focused on. `eye` creates the projection for the left eye when set to 1, or the right eye when set to 2. `flip_fov` determines whether the projection's field of view is flipped over its diagonal.
- determinant() -> float - Returns a scalar value that is the signed factor by which areas are scaled by this matrix. If the sign is negative, the matrix flips the orientation of the area. The determinant can be used to calculate the invertibility of a matrix or solve linear systems of equations involving the matrix, among other applications.
- flipped_y() -> Projection - Returns a copy of this Projection with the signs of the values of the Y column flipped.
- get_aspect() -> float - Returns the X:Y aspect ratio of this Projection's viewport.
- get_far_plane_half_extents() -> Vector2 - Returns the dimensions of the far clipping plane of the projection, divided by two.
- get_fov() -> float - Returns the horizontal field of view of the projection (in degrees).
- get_fovy(fovx: float, aspect: float) -> float - Returns the vertical field of view of the projection (in degrees) associated with the given horizontal field of view (in degrees) and aspect ratio. **Note:** Unlike most methods of Projection, `aspect` is expected to be 1 divided by the X:Y aspect ratio.
- get_lod_multiplier() -> float - Returns the factor by which the visible level of detail is scaled by this Projection.
- get_pixels_per_meter(for_pixel_width: int) -> int - Returns `for_pixel_width` divided by the viewport's width measured in meters on the near plane, after this Projection is applied.
- get_projection_plane(plane: int) -> Plane - Returns the clipping plane of this Projection whose index is given by `plane`. `plane` should be equal to one of `PLANE_NEAR`, `PLANE_FAR`, `PLANE_LEFT`, `PLANE_TOP`, `PLANE_RIGHT`, or `PLANE_BOTTOM`.
- get_viewport_half_extents() -> Vector2 - Returns the dimensions of the viewport plane that this Projection projects positions onto, divided by two.
- get_z_far() -> float - Returns the distance for this Projection beyond which positions are clipped.
- get_z_near() -> float - Returns the distance for this Projection before which positions are clipped.
- inverse() -> Projection - Returns a Projection that performs the inverse of this Projection's projective transformation.
- is_orthogonal() -> bool - Returns `true` if this Projection performs an orthogonal projection.
- jitter_offseted(offset: Vector2) -> Projection - Returns a Projection with the X and Y values from the given Vector2 added to the first and second values of the final column respectively.
- perspective_znear_adjusted(new_znear: float) -> Projection - Returns a Projection with the near clipping distance adjusted to be `new_znear`. **Note:** The original Projection must be a perspective projection.

**Enums:**
**Planes:** PLANE_NEAR=0, PLANE_FAR=1, PLANE_LEFT=2, PLANE_TOP=3, PLANE_RIGHT=4, PLANE_BOTTOM=5
  - PLANE_NEAR: The index value of the projection's near clipping plane.
  - PLANE_FAR: The index value of the projection's far clipping plane.
  - PLANE_LEFT: The index value of the projection's left clipping plane.
  - PLANE_TOP: The index value of the projection's top clipping plane.
  - PLANE_RIGHT: The index value of the projection's right clipping plane.
  - PLANE_BOTTOM: The index value of the projection bottom clipping plane.
**Constants:** IDENTITY=Projection(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1), ZERO=Projection(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  - IDENTITY: A Projection with no transformation defined. When applied to other data structures, no transformation is performed.
  - ZERO: A Projection with all values initialized to 0. When applied to other data structures, they will be zeroed.

