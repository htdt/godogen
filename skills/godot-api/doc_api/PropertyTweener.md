## PropertyTweener <- Tweener

PropertyTweener is used to interpolate a property in an object. See `Tween.tween_property` for more usage information. The tweener will finish automatically if the target object is freed. **Note:** `Tween.tween_property` is the only correct way to create PropertyTweener. Any PropertyTweener created manually will not function correctly.

**Methods:**
- as_relative() -> PropertyTweener - When called, the final value will be used as a relative value instead. **Example:** Move the node by `100` pixels to the right.
- from(value: Variant) -> PropertyTweener - Sets a custom initial value to the PropertyTweener. **Example:** Move the node from position `(100, 100)` to `(200, 100)`.
- from_current() -> PropertyTweener - Makes the PropertyTweener use the current property value (i.e. at the time of creating this PropertyTweener) as a starting point. This is equivalent of using `from` with the current value. These two calls will do the same:
- set_custom_interpolator(interpolator_method: Callable) -> PropertyTweener - Allows interpolating the value with a custom easing function. The provided `interpolator_method` will be called with a value ranging from `0.0` to `1.0` and is expected to return a value within the same range (values outside the range can be used for overshoot). The return value of the method is then used for interpolation between initial and final value. Note that the parameter passed to the method is still subject to the tweener's own easing.
- set_delay(delay: float) -> PropertyTweener - Sets the time in seconds after which the PropertyTweener will start interpolating. By default there's no delay.
- set_ease(ease: int) -> PropertyTweener - Sets the type of used easing from `Tween.EaseType`. If not set, the default easing is used from the Tween that contains this Tweener.
- set_trans(trans: int) -> PropertyTweener - Sets the type of used transition from `Tween.TransitionType`. If not set, the default transition is used from the Tween that contains this Tweener.

