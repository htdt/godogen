## SkeletonModification2D <- Resource

This resource provides an interface that can be expanded so code that operates on Bone2D nodes in a Skeleton2D can be mixed and matched together to create complex interactions. This is used to provide Godot with a flexible and powerful Inverse Kinematics solution that can be adapted for many different uses.

**Props:**
- enabled: bool = true
- execution_mode: int = 0

- **enabled**: If `true`, the modification's `_execute` function will be called by the SkeletonModificationStack2D.
- **execution_mode**: The execution mode for the modification. This tells the modification stack when to execute the modification. Some modifications have settings that are only available in certain execution modes.

**Methods:**
- _draw_editor_gizmo() - Used for drawing **editor-only** modification gizmos. This function will only be called in the Godot editor and can be overridden to draw custom gizmos. **Note:** You will need to use the Skeleton2D from `SkeletonModificationStack2D.get_skeleton` and it's draw functions, as the SkeletonModification2D resource cannot draw on its own.
- _execute(delta: float) - Executes the given modification. This is where the modification performs whatever function it is designed to do.
- _setup_modification(modification_stack: SkeletonModificationStack2D) - Called when the modification is setup. This is where the modification performs initialization.
- clamp_angle(angle: float, min: float, max: float, invert: bool) -> float - Takes an angle and clamps it so it is within the passed-in `min` and `max` range. `invert` will inversely clamp the angle, clamping it to the range outside of the given bounds.
- get_editor_draw_gizmo() -> bool - Returns whether this modification will call `_draw_editor_gizmo` in the Godot editor to draw modification-specific gizmos.
- get_is_setup() -> bool - Returns whether this modification has been successfully setup or not.
- get_modification_stack() -> SkeletonModificationStack2D - Returns the SkeletonModificationStack2D that this modification is bound to. Through the modification stack, you can access the Skeleton2D the modification is operating on.
- set_editor_draw_gizmo(draw_gizmo: bool) - Sets whether this modification will call `_draw_editor_gizmo` in the Godot editor to draw modification-specific gizmos.
- set_is_setup(is_setup: bool) - Manually allows you to set the setup state of the modification. This function should only rarely be used, as the SkeletonModificationStack2D the modification is bound to should handle setting the modification up.

