## XROrigin3D <- Node3D

This is a special node within the AR/VR system that maps the physical location of the center of our tracking space to the virtual location within our game world. Multiple origin points can be added to the scene tree, but only one can used at a time. All the XRCamera3D, XRController3D, and XRAnchor3D nodes should be direct children of this node for spatial tracking to work correctly. It is the position of this node that you update when your character needs to move through your game world while we're not moving in the real world. Movement in the real world is always in relation to this origin point. For example, if your character is driving a car, the XROrigin3D node should be a child node of this car. Or, if you're implementing a teleport system to move your character, you should change the position of this node.

**Props:**
- current: bool = false
- world_scale: float = 1.0

- **current**: If `true`, this origin node is currently being used by the XRServer. Only one origin point can be used at a time.
- **world_scale**: The scale of the game world compared to the real world. This is the same as `XRServer.world_scale`. By default, most AR/VR platforms assume that 1 game unit corresponds to 1 real world meter.

