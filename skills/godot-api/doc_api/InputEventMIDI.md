## InputEventMIDI <- InputEvent

InputEventMIDI stores information about messages from (Musical Instrument Digital Interface) devices. These may include musical keyboards, synthesizers, and drum machines. MIDI messages can be received over a 5-pin MIDI connector or over USB. If your device supports both be sure to check the settings in the device to see which output it is using. By default, Godot does not detect MIDI devices. You need to call `OS.open_midi_inputs`, first. You can check which devices are detected with `OS.get_connected_midi_inputs`, and close the connection with `OS.close_midi_inputs`. **Note:** Godot does not support MIDI output, so there is no way to emit MIDI messages from Godot. Only MIDI input is supported. **Note:** On the Web platform, using MIDI input requires a browser permission to be granted first. This permission request is performed when calling `OS.open_midi_inputs`. MIDI input will not work until the user accepts the permission request.

**Props:**
- channel: int = 0
- controller_number: int = 0
- controller_value: int = 0
- instrument: int = 0
- message: int (MIDIMessage) = 0
- pitch: int = 0
- pressure: int = 0
- velocity: int = 0

- **channel**: The MIDI channel of this message, ranging from `0` to `15`. MIDI channel `9` is reserved for percussion instruments.
- **controller_number**: The unique number of the controller, if `message` is `MIDI_MESSAGE_CONTROL_CHANGE`, otherwise this is `0`. This value can be used to identify sliders for volume, balance, and panning, as well as switches and pedals on the MIDI device. See the for a small list.
- **controller_value**: The value applied to the controller. If `message` is `MIDI_MESSAGE_CONTROL_CHANGE`, this value ranges from `0` to `127`, otherwise it is `0`. See also `controller_value`.
- **instrument**: The instrument (also called *program* or *preset*) used on this MIDI message. This value ranges from `0` to `127`. To see what each value means, refer to the . Keep in mind that the list is off by 1 because it does not begin from 0. A value of `0` corresponds to the acoustic grand piano.
- **message**: Represents the type of MIDI message (see the `MIDIMessage` enum). For more information, see the .
- **pitch**: The pitch index number of this MIDI message. This value ranges from `0` to `127`. On a piano, the **middle C** is `60`, followed by a **C-sharp** (`61`), then a **D** (`62`), and so on. Each octave is split in offsets of 12. See the "MIDI note number" column of the a full list.
- **pressure**: The strength of the key being pressed. This value ranges from `0` to `127`. **Note:** For many devices, this value is always `0`. Other devices such as musical keyboards may simulate pressure by changing the `velocity`, instead.
- **velocity**: The velocity of the MIDI message. This value ranges from `0` to `127`. For a musical keyboard, this corresponds to how quickly the key was pressed, and is rarely above `110` in practice. **Note:** Some MIDI devices may send a `MIDI_MESSAGE_NOTE_ON` message with `0` velocity and expect it to be treated the same as a `MIDI_MESSAGE_NOTE_OFF` message. If necessary, this can be handled with a few lines of code:

