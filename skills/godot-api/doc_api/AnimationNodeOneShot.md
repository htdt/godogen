## AnimationNodeOneShot <- AnimationNodeSync

A resource to add to an AnimationNodeBlendTree. This animation node will execute a sub-animation and return once it finishes. Blend times for fading in and out can be customized, as well as filters. After setting the request and changing the animation playback, the one-shot node automatically clears the request on the next process frame by setting its `request` value to `ONE_SHOT_REQUEST_NONE`.

**Props:**
- abort_on_reset: bool = false
- autorestart: bool = false
- autorestart_delay: float = 1.0
- autorestart_random_delay: float = 0.0
- break_loop_at_end: bool = false
- fadein_curve: Curve
- fadein_time: float = 0.0
- fadeout_curve: Curve
- fadeout_time: float = 0.0
- mix_mode: int (AnimationNodeOneShot.MixMode) = 0

- **abort_on_reset**: If `true`, the sub-animation will abort if resumed with a reset after a prior interruption.
- **autorestart**: If `true`, the sub-animation will restart automatically after finishing. In other words, to start auto restarting, the animation must be played once with the `ONE_SHOT_REQUEST_FIRE` request. The `ONE_SHOT_REQUEST_ABORT` request stops the auto restarting, but it does not disable the `autorestart` itself. So, the `ONE_SHOT_REQUEST_FIRE` request will start auto restarting again.
- **autorestart_delay**: The delay after which the automatic restart is triggered, in seconds.
- **autorestart_random_delay**: If `autorestart` is `true`, a random additional delay (in seconds) between 0 and this value will be added to `autorestart_delay`.
- **break_loop_at_end**: If `true`, breaks the loop at the end of the loop cycle for transition, even if the animation is looping.
- **fadein_curve**: Determines how cross-fading between animations is eased. If empty, the transition will be linear. Should be a unit Curve.
- **fadein_time**: The fade-in duration. For example, setting this to `1.0` for a 5 second length animation will produce a cross-fade that starts at 0 second and ends at 1 second during the animation. **Note:** AnimationNodeOneShot transitions the current state after the fading has finished.
- **fadeout_curve**: Determines how cross-fading between animations is eased. If empty, the transition will be linear. Should be a unit Curve.
- **fadeout_time**: The fade-out duration. For example, setting this to `1.0` for a 5 second length animation will produce a cross-fade that starts at 4 second and ends at 5 second during the animation. **Note:** AnimationNodeOneShot transitions the current state after the fading has finished.
- **mix_mode**: The blend type.

**Enums:**
**OneShotRequest:** ONE_SHOT_REQUEST_NONE=0, ONE_SHOT_REQUEST_FIRE=1, ONE_SHOT_REQUEST_ABORT=2, ONE_SHOT_REQUEST_FADE_OUT=3
  - ONE_SHOT_REQUEST_NONE: The default state of the request. Nothing is done.
  - ONE_SHOT_REQUEST_FIRE: The request to play the animation connected to "shot" port.
  - ONE_SHOT_REQUEST_ABORT: The request to stop the animation connected to "shot" port.
  - ONE_SHOT_REQUEST_FADE_OUT: The request to fade out the animation connected to "shot" port.
**MixMode:** MIX_MODE_BLEND=0, MIX_MODE_ADD=1
  - MIX_MODE_BLEND: Blends two animations. See also AnimationNodeBlend2.
  - MIX_MODE_ADD: Blends two animations additively. See also AnimationNodeAdd2.

