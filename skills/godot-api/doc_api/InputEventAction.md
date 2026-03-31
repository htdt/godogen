## InputEventAction <- InputEvent

Contains a generic action which can be targeted from several types of inputs. Actions and their events can be set in the **Input Map** tab in **Project > Project Settings**, or with the InputMap class. **Note:** Unlike the other InputEvent subclasses which map to unique physical events, this virtual one is not emitted by the engine. This class is useful to emit actions manually with `Input.parse_input_event`, which are then received in `Node._input`. To check if a physical event matches an action from the Input Map, use `InputEvent.is_action` and `InputEvent.is_action_pressed`.

**Props:**
- action: StringName = &""
- event_index: int = -1
- pressed: bool = false
- strength: float = 1.0

- **action**: The action's name. This is usually the name of an existing action in the InputMap which you want this custom event to match.
- **event_index**: The real event index in action this event corresponds to (from events defined for this action in the InputMap). If `-1`, a unique ID will be used and actions pressed with this ID will need to be released with another InputEventAction.
- **pressed**: If `true`, the action's state is pressed. If `false`, the action's state is released.
- **strength**: The action's strength between 0 and 1. This value is considered as equal to 0 if pressed is `false`. The event strength allows faking analog joypad motion events, by specifying how strongly the joypad axis is bent or pressed.

