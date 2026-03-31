## AwaitTweener <- Tweener

AwaitTweener is used to await a specified signal, allowing asynchronous steps in Tween animation. See `Tween.tween_await` for more usage information. The `Tweener.finished` signal is emitted when either the awaited signal is received, when timeout is reached, or when the target object is freed.

**Methods:**
- set_timeout(timeout: float) -> AwaitTweener - Sets the maximum time an AwaitTweener can wait for the signal. Can be used as a safeguard for signals that may never be emitted. If not specified, the tweener will wait indefinitely.

