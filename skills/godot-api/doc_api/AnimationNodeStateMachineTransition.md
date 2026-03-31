## AnimationNodeStateMachineTransition <- Resource

The path generated when using `AnimationNodeStateMachinePlayback.travel` is limited to the nodes connected by AnimationNodeStateMachineTransition. You can set the timing and conditions of the transition in detail.

**Props:**
- advance_condition: StringName = &""
- advance_expression: String = ""
- advance_mode: int (AnimationNodeStateMachineTransition.AdvanceMode) = 1
- break_loop_at_end: bool = false
- priority: int = 1
- reset: bool = true
- switch_mode: int (AnimationNodeStateMachineTransition.SwitchMode) = 0
- xfade_curve: Curve
- xfade_time: float = 0.0

- **advance_condition**: Turn on auto advance when this condition is set. The provided name will become a boolean parameter on the AnimationTree that can be controlled from code (see ). For example, if `AnimationTree.tree_root` is an AnimationNodeStateMachine and `advance_condition` is set to `"idle"`:
- **advance_expression**: Use an expression as a condition for state machine transitions. It is possible to create complex animation advance conditions for switching between states and gives much greater flexibility for creating complex state machines by directly interfacing with the script code.
- **advance_mode**: Determines whether the transition should be disabled, enabled when using `AnimationNodeStateMachinePlayback.travel`, or traversed automatically if the `advance_condition` and `advance_expression` checks are `true` (if assigned).
- **break_loop_at_end**: If `true`, breaks the loop at the end of the loop cycle for transition, even if the animation is looping.
- **priority**: Lower priority transitions are preferred when travelling through the tree via `AnimationNodeStateMachinePlayback.travel` or `advance_mode` is set to `ADVANCE_MODE_AUTO`.
- **reset**: If `true`, the destination animation is played back from the beginning when switched.
- **switch_mode**: The transition type.
- **xfade_curve**: Ease curve for better control over cross-fade between this state and the next. Should be a unit Curve.
- **xfade_time**: The time to cross-fade between this state and the next. **Note:** AnimationNodeStateMachine transitions the current state immediately after the start of the fading. The precise remaining time can only be inferred from the main animation. When AnimationNodeOutput is considered as the most upstream, so the `xfade_time` is not scaled depending on the downstream delta. See also `AnimationNodeOneShot.fadeout_time`.

**Signals:**
- advance_condition_changed - Emitted when `advance_condition` is changed.

**Enums:**
**SwitchMode:** SWITCH_MODE_IMMEDIATE=0, SWITCH_MODE_SYNC=1, SWITCH_MODE_AT_END=2
  - SWITCH_MODE_IMMEDIATE: Switch to the next state immediately. The current state will end and blend into the beginning of the new one.
  - SWITCH_MODE_SYNC: Switch to the next state immediately, but will seek the new state to the playback position of the old state.
  - SWITCH_MODE_AT_END: Wait for the current state playback to end, then switch to the beginning of the next state animation.
**AdvanceMode:** ADVANCE_MODE_DISABLED=0, ADVANCE_MODE_ENABLED=1, ADVANCE_MODE_AUTO=2
  - ADVANCE_MODE_DISABLED: Don't use this transition.
  - ADVANCE_MODE_ENABLED: Only use this transition during `AnimationNodeStateMachinePlayback.travel`.
  - ADVANCE_MODE_AUTO: Automatically use this transition if the `advance_condition` and `advance_expression` checks are `true` (if assigned).

