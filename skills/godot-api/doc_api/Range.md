## Range <- Control

Range is an abstract base class for controls that represent a number within a range, using a configured `step` and `page` size. See e.g. ScrollBar and Slider for examples of higher-level nodes using Range.

**Props:**
- allow_greater: bool = false
- allow_lesser: bool = false
- exp_edit: bool = false
- max_value: float = 100.0
- min_value: float = 0.0
- page: float = 0.0
- ratio: float
- rounded: bool = false
- size_flags_vertical: int (Control.SizeFlags) = 0
- step: float = 0.01
- value: float = 0.0

- **allow_greater**: If `true`, `value` may be greater than `max_value`.
- **allow_lesser**: If `true`, `value` may be less than `min_value`.
- **exp_edit**: If `true`, and `min_value` is greater or equal to `0`, `value` will be represented exponentially rather than linearly.
- **max_value**: Maximum value. Range is clamped if `value` is greater than `max_value`.
- **min_value**: Minimum value. Range is clamped if `value` is less than `min_value`.
- **page**: Page size. Used mainly for ScrollBar. A ScrollBar's grabber length is the ScrollBar's size multiplied by `page` over the difference between `min_value` and `max_value`.
- **ratio**: The value mapped between 0 and 1.
- **rounded**: If `true`, `value` will always be rounded to the nearest integer.
- **step**: If greater than `0.0`, `value` will always be rounded to a multiple of this property's value above `min_value`. For example, if `min_value` is `0.1` and step is `0.2`, then `value` is limited to `0.1`, `0.3`, `0.5`, and so on. If `rounded` is also `true`, `value` will first be rounded to a multiple of this property's value, then rounded to the nearest integer.
- **value**: Range's current value. Changing this property (even via code) will trigger `value_changed` signal. Use `set_value_no_signal` if you want to avoid it.

**Methods:**
- _value_changed(new_value: float) - Called when the Range's value is changed (following the same conditions as `value_changed`).
- set_value_no_signal(value: float) - Sets the Range's current value to the specified `value`, without emitting the `value_changed` signal.
- share(with: Node) - Binds two Ranges together along with any ranges previously grouped with either of them. When any of range's member variables change, it will share the new value with all other ranges in its group.
- unshare() - Stops the Range from sharing its member variables with any other.

**Signals:**
- changed - Emitted when `min_value`, `max_value`, `page`, or `step` change.
- value_changed(value: float) - Emitted when `value` changes. When used on a Slider, this is called continuously while dragging (potentially every frame). If you are performing an expensive operation in a function connected to `value_changed`, consider using a *debouncing* Timer to call the function less often. **Note:** Unlike signals such as `LineEdit.text_changed`, `value_changed` is also emitted when `value` is set directly via code.

