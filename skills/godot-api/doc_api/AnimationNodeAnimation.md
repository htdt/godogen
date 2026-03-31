## AnimationNodeAnimation <- AnimationRootNode

A resource to add to an AnimationNodeBlendTree. Only has one output port using the `animation` property. Used as an input for AnimationNodes that blend animations together.

**Props:**
- advance_on_start: bool = false
- animation: StringName = &""
- loop_mode: int (Animation.LoopMode)
- play_mode: int (AnimationNodeAnimation.PlayMode) = 0
- start_offset: float
- stretch_time_scale: bool
- timeline_length: float
- use_custom_timeline: bool = false

- **advance_on_start**: If `true`, on receiving a request to play an animation from the start, the first frame is not drawn, but only processed, and playback starts from the next frame. See also the notes of `AnimationPlayer.play`.
- **animation**: Animation to use as an output. It is one of the animations provided by `AnimationTree.anim_player`.
- **loop_mode**: If `use_custom_timeline` is `true`, override the loop settings of the original Animation resource with the value. **Note:** If the `Animation.loop_mode` isn't set to looping, the `Animation.track_set_interpolation_loop_wrap` option will not be respected. If you cannot get the expected behavior, consider duplicating the Animation resource and changing the loop settings.
- **play_mode**: Determines the playback direction of the animation.
- **start_offset**: If `use_custom_timeline` is `true`, offset the start position of the animation. This is useful for adjusting which foot steps first in 3D walking animations.
- **stretch_time_scale**: If `true`, scales the time so that the length specified in `timeline_length` is one cycle. This is useful for matching the periods of walking and running animations. If `false`, the original animation length is respected. If you set the loop to `loop_mode`, the animation will loop in `timeline_length`.
- **timeline_length**: The length of the custom timeline. If `stretch_time_scale` is `true`, scales the animation to this length.
- **use_custom_timeline**: If `true`, AnimationNode provides an animation based on the Animation resource with some parameters adjusted.

**Enums:**
**PlayMode:** PLAY_MODE_FORWARD=0, PLAY_MODE_BACKWARD=1
  - PLAY_MODE_FORWARD: Plays animation in forward direction.
  - PLAY_MODE_BACKWARD: Plays animation in backward direction.

