## AudioEffect <- Resource

The base Resource for every audio effect. In the editor, an audio effect can be added to the current bus layout through the Audio panel. At run-time, it is also possible to manipulate audio effects through `AudioServer.add_bus_effect`, `AudioServer.remove_bus_effect`, and `AudioServer.get_bus_effect`. When applied on a bus, an audio effect creates a corresponding AudioEffectInstance. The instance is directly responsible for manipulating sound, based on the original audio effect's properties.

**Methods:**
- _instantiate() -> AudioEffectInstance - Override this method to customize the AudioEffectInstance created when this effect is applied on a bus in the editor's Audio panel, or through `AudioServer.add_bus_effect`. **Note:** It is recommended to keep a reference to the original AudioEffect in the new instance. Depending on the implementation this allows the effect instance to listen for changes at run-time and be modified accordingly.

