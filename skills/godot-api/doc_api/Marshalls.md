## Marshalls <- Object

Provides data transformation and encoding utility functions.

**Methods:**
- base64_to_raw(base64_str: String) -> PackedByteArray - Returns a decoded PackedByteArray corresponding to the Base64-encoded string `base64_str`.
- base64_to_utf8(base64_str: String) -> String - Returns a decoded string corresponding to the Base64-encoded string `base64_str`.
- base64_to_variant(base64_str: String, allow_objects: bool = false) -> Variant - Returns a decoded Variant corresponding to the Base64-encoded string `base64_str`. If `allow_objects` is `true`, decoding objects is allowed. Internally, this uses the same decoding mechanism as the `@GlobalScope.bytes_to_var` method. **Warning:** Deserialized objects can contain code which gets executed. Do not use this option if the serialized object comes from untrusted sources to avoid potential security threats such as remote code execution.
- raw_to_base64(array: PackedByteArray) -> String - Returns a Base64-encoded string of a given PackedByteArray.
- utf8_to_base64(utf8_str: String) -> String - Returns a Base64-encoded string of the UTF-8 string `utf8_str`.
- variant_to_base64(variant: Variant, full_objects: bool = false) -> String - Returns a Base64-encoded string of the Variant `variant`. If `full_objects` is `true`, encoding objects is allowed (and can potentially include code). Internally, this uses the same encoding mechanism as the `@GlobalScope.var_to_bytes` method.

