## RootMotionView <- VisualInstance3D

*Root motion* refers to an animation technique where a mesh's skeleton is used to give impulse to a character. When working with 3D animations, a popular technique is for animators to use the root skeleton bone to give motion to the rest of the skeleton. This allows animating characters in a way where steps actually match the floor below. It also allows precise interaction with objects during cinematics. See also AnimationMixer. **Note:** RootMotionView is only visible in the editor. It will be hidden automatically in the running project.

**Props:**
- animation_path: NodePath = NodePath("")
- cell_size: float = 1.0
- color: Color = Color(0.5, 0.5, 1, 1)
- radius: float = 10.0
- zero_y: bool = true

- **animation_path**: Path to an AnimationMixer node to use as a basis for root motion.
- **cell_size**: The grid's cell size in 3D units.
- **color**: The grid's color.
- **radius**: The grid's radius in 3D units. The grid's opacity will fade gradually as the distance from the origin increases until this `radius` is reached.
- **zero_y**: If `true`, the grid's points will all be on the same Y coordinate (*local* Y = 0). If `false`, the points' original Y coordinate is preserved.

