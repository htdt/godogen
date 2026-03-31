## VehicleWheel3D <- Node3D

A node used as a child of a VehicleBody3D parent to simulate the behavior of one of its wheels. This node also acts as a collider to detect if the wheel is touching a surface. **Note:** This class has known issues and isn't designed to provide realistic 3D vehicle physics. If you want advanced vehicle physics, you may need to write your own physics integration using another PhysicsBody3D class.

**Props:**
- brake: float = 0.0
- damping_compression: float = 0.83
- damping_relaxation: float = 0.88
- engine_force: float = 0.0
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 2
- steering: float = 0.0
- suspension_max_force: float = 6000.0
- suspension_stiffness: float = 5.88
- suspension_travel: float = 0.2
- use_as_steering: bool = false
- use_as_traction: bool = false
- wheel_friction_slip: float = 10.5
- wheel_radius: float = 0.5
- wheel_rest_length: float = 0.15
- wheel_roll_influence: float = 0.1

- **brake**: Slows down the wheel by applying a braking force. The wheel is only slowed down if it is in contact with a surface. The force you need to apply to adequately slow down your vehicle depends on the `RigidBody3D.mass` of the vehicle. For a vehicle with a mass set to 1000, try a value in the 25 - 30 range for hard braking.
- **damping_compression**: The damping applied to the suspension spring when being compressed, meaning when the wheel is moving up relative to the vehicle. It is measured in Newton-seconds per millimeter (N⋅s/mm), or megagrams per second (Mg/s). This value should be between 0.0 (no damping) and 1.0, but may be more. A value of 0.0 means the car will keep bouncing as the spring keeps its energy. A good value for this is around 0.3 for a normal car, 0.5 for a race car.
- **damping_relaxation**: The damping applied to the suspension spring when rebounding or extending, meaning when the wheel is moving down relative to the vehicle. It is measured in Newton-seconds per millimeter (N⋅s/mm), or megagrams per second (Mg/s). This value should be between 0.0 (no damping) and 1.0, but may be more. This value should always be slightly higher than the `damping_compression` property. For a `damping_compression` value of 0.3, try a relaxation value of 0.5.
- **engine_force**: Accelerates the wheel by applying an engine force. The wheel is only sped up if it is in contact with a surface. The `RigidBody3D.mass` of the vehicle has an effect on the acceleration of the vehicle. For a vehicle with a mass set to 1000, try a value in the 25 - 50 range for acceleration. **Note:** The simulation does not take the effect of gears into account, you will need to add logic for this if you wish to simulate gears. A negative value will result in the wheel reversing.
- **steering**: The steering angle for the wheel, in radians. Setting this to a non-zero value will result in the vehicle turning when it's moving.
- **suspension_max_force**: The maximum force the spring can resist. This value should be higher than a quarter of the `RigidBody3D.mass` of the VehicleBody3D or the spring will not carry the weight of the vehicle. Good results are often obtained by a value that is about 3× to 4× this number.
- **suspension_stiffness**: The stiffness of the suspension, measured in Newtons per millimeter (N/mm), or megagrams per second squared (Mg/s²). Use a value lower than 50 for an off-road car, a value between 50 and 100 for a race car and try something around 200 for something like a Formula 1 car.
- **suspension_travel**: This is the distance the suspension can travel. As Godot units are equivalent to meters, keep this setting relatively low. Try a value between 0.1 and 0.3 depending on the type of car.
- **use_as_steering**: If `true`, this wheel will be turned when the car steers. This value is used in conjunction with `VehicleBody3D.steering` and ignored if you are using the per-wheel `steering` value instead.
- **use_as_traction**: If `true`, this wheel transfers engine force to the ground to propel the vehicle forward. This value is used in conjunction with `VehicleBody3D.engine_force` and ignored if you are using the per-wheel `engine_force` value instead.
- **wheel_friction_slip**: This determines how much grip this wheel has. It is combined with the friction setting of the surface the wheel is in contact with. 0.0 means no grip, 1.0 is normal grip. For a drift car setup, try setting the grip of the rear wheels slightly lower than the front wheels, or use a lower value to simulate tire wear. It's best to set this to 1.0 when starting out.
- **wheel_radius**: The radius of the wheel in meters.
- **wheel_rest_length**: This is the distance in meters the wheel is lowered from its origin point. Don't set this to 0.0 and move the wheel into position, instead move the origin point of your wheel (the gizmo in Godot) to the position the wheel will take when bottoming out, then use the rest length to move the wheel down to the position it should be in when the car is in rest.
- **wheel_roll_influence**: This value affects the roll of your vehicle. If set to 1.0 for all wheels, your vehicle will resist body roll, while a value of 0.0 will be prone to rolling over.

**Methods:**
- get_contact_body() -> Node3D - Returns the contacting body node if valid in the tree, as Node3D. At the moment, GridMap is not supported so the node will be always of type PhysicsBody3D. Returns `null` if the wheel is not in contact with a surface, or the contact body is not a PhysicsBody3D.
- get_contact_normal() -> Vector3 - Returns the normal of the suspension's collision in world space if the wheel is in contact. If the wheel isn't in contact with anything, returns a vector pointing directly along the suspension axis toward the vehicle in world space.
- get_contact_point() -> Vector3 - Returns the point of the suspension's collision in world space if the wheel is in contact. If the wheel isn't in contact with anything, returns the maximum point of the wheel's ray cast in world space, which is defined by `wheel_rest_length + wheel_radius`.
- get_rpm() -> float - Returns the rotational speed of the wheel in revolutions per minute.
- get_skidinfo() -> float - Returns a value between 0.0 and 1.0 that indicates whether this wheel is skidding. 0.0 is skidding (the wheel has lost grip, e.g. icy terrain), 1.0 means not skidding (the wheel has full grip, e.g. dry asphalt road).
- is_in_contact() -> bool - Returns `true` if this wheel is in contact with a surface.

