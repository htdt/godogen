## SubtweenTweener <- Tweener

SubtweenTweener is used to execute a Tween as one step in a sequence defined by another Tween. See `Tween.tween_subtween` for more usage information. **Note:** `Tween.tween_subtween` is the only correct way to create SubtweenTweener. Any SubtweenTweener created manually will not function correctly.

**Methods:**
- set_delay(delay: float) -> SubtweenTweener - Sets the time in seconds after which the SubtweenTweener will start running the subtween. By default there's no delay.

