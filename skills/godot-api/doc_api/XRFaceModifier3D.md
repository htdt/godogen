## XRFaceModifier3D <- Node3D

This node applies weights from an XRFaceTracker to a mesh with supporting face blend shapes. The blend shapes are supported, as well as ARKit and SRanipal blend shapes. The node attempts to identify blend shapes based on name matching. Blend shapes should match the names listed in the chart.

**Props:**
- face_tracker: StringName = &"/user/face_tracker"
- target: NodePath = NodePath("")

- **face_tracker**: The XRFaceTracker path.
- **target**: The NodePath of the face MeshInstance3D.

