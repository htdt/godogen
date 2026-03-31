## PacketPeer <- RefCounted

PacketPeer is an abstraction and base class for packet-based protocols (such as UDP). It provides an API for sending and receiving packets both as raw data or variables. This makes it easy to transfer data over a protocol, without having to encode data as low-level bytes or having to worry about network ordering. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

**Props:**
- encode_buffer_max_size: int = 8388608

- **encode_buffer_max_size**: Maximum buffer size allowed when encoding Variants. Raise this value to support heavier memory allocations. The `put_var` method allocates memory on the stack, and the buffer used will grow automatically to the closest power of two to match the size of the Variant. If the Variant is bigger than `encode_buffer_max_size`, the method will error out with `ERR_OUT_OF_MEMORY`.

**Methods:**
- get_available_packet_count() -> int - Returns the number of packets currently available in the ring-buffer.
- get_packet() -> PackedByteArray - Gets a raw packet.
- get_packet_error() -> int - Returns the error state of the last packet received (via `get_packet` and `get_var`).
- get_var(allow_objects: bool = false) -> Variant - Gets a Variant. If `allow_objects` is `true`, decoding objects is allowed. Internally, this uses the same decoding mechanism as the `@GlobalScope.bytes_to_var` method. **Warning:** Deserialized objects can contain code which gets executed. Do not use this option if the serialized object comes from untrusted sources to avoid potential security threats such as remote code execution.
- put_packet(buffer: PackedByteArray) -> int - Sends a raw packet.
- put_var(var: Variant, full_objects: bool = false) -> int - Sends a Variant as a packet. If `full_objects` is `true`, encoding objects is allowed (and can potentially include code). Internally, this uses the same encoding mechanism as the `@GlobalScope.var_to_bytes` method.

