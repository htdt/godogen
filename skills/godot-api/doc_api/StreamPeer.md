## StreamPeer <- RefCounted

StreamPeer is an abstract base class mostly used for stream-based protocols (such as TCP). It provides an API for sending and receiving data through streams as raw data or strings. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

**Props:**
- big_endian: bool = false

- **big_endian**: If `true`, this StreamPeer will using big-endian format for encoding and decoding.

**Methods:**
- get_8() -> int - Gets a signed byte from the stream.
- get_16() -> int - Gets a signed 16-bit value from the stream.
- get_32() -> int - Gets a signed 32-bit value from the stream.
- get_64() -> int - Gets a signed 64-bit value from the stream.
- get_available_bytes() -> int - Returns the number of bytes this StreamPeer has available.
- get_data(bytes: int) -> Array - Returns a chunk data with the received bytes, as an Array containing two elements: an `Error` constant and a PackedByteArray. `bytes` is the number of bytes to be received. If not enough bytes are available, the function will block until the desired amount is received.
- get_double() -> float - Gets a double-precision float from the stream.
- get_float() -> float - Gets a single-precision float from the stream.
- get_half() -> float - Gets a half-precision float from the stream.
- get_partial_data(bytes: int) -> Array - Returns a chunk data with the received bytes, as an Array containing two elements: an `Error` constant and a PackedByteArray. `bytes` is the number of bytes to be received. If not enough bytes are available, the function will return how many were actually received.
- get_string(bytes: int = -1) -> String - Gets an ASCII string with byte-length `bytes` from the stream. If `bytes` is negative (default) the length will be read from the stream using the reverse process of `put_string`.
- get_u8() -> int - Gets an unsigned byte from the stream.
- get_u16() -> int - Gets an unsigned 16-bit value from the stream.
- get_u32() -> int - Gets an unsigned 32-bit value from the stream.
- get_u64() -> int - Gets an unsigned 64-bit value from the stream.
- get_utf8_string(bytes: int = -1) -> String - Gets a UTF-8 string with byte-length `bytes` from the stream (this decodes the string sent as UTF-8). If `bytes` is negative (default) the length will be read from the stream using the reverse process of `put_utf8_string`.
- get_var(allow_objects: bool = false) -> Variant - Gets a Variant from the stream. If `allow_objects` is `true`, decoding objects is allowed. Internally, this uses the same decoding mechanism as the `@GlobalScope.bytes_to_var` method. **Warning:** Deserialized objects can contain code which gets executed. Do not use this option if the serialized object comes from untrusted sources to avoid potential security threats such as remote code execution.
- put_8(value: int) - Puts a signed byte into the stream.
- put_16(value: int) - Puts a signed 16-bit value into the stream.
- put_32(value: int) - Puts a signed 32-bit value into the stream.
- put_64(value: int) - Puts a signed 64-bit value into the stream.
- put_data(data: PackedByteArray) -> int - Sends a chunk of data through the connection, blocking if necessary until the data is done sending. This function returns an `Error` code.
- put_double(value: float) - Puts a double-precision float into the stream.
- put_float(value: float) - Puts a single-precision float into the stream.
- put_half(value: float) - Puts a half-precision float into the stream.
- put_partial_data(data: PackedByteArray) -> Array - Sends a chunk of data through the connection. If all the data could not be sent at once, only part of it will. This function returns two values, an `Error` code and an integer, describing how much data was actually sent.
- put_string(value: String) - Puts a zero-terminated ASCII string into the stream prepended by a 32-bit unsigned integer representing its size. **Note:** To put an ASCII string without prepending its size, you can use `put_data`:
- put_u8(value: int) - Puts an unsigned byte into the stream.
- put_u16(value: int) - Puts an unsigned 16-bit value into the stream.
- put_u32(value: int) - Puts an unsigned 32-bit value into the stream.
- put_u64(value: int) - Puts an unsigned 64-bit value into the stream.
- put_utf8_string(value: String) - Puts a zero-terminated UTF-8 string into the stream prepended by a 32 bits unsigned integer representing its size. **Note:** To put a UTF-8 string without prepending its size, you can use `put_data`:
- put_var(value: Variant, full_objects: bool = false) - Puts a Variant into the stream. If `full_objects` is `true` encoding objects is allowed (and can potentially include code). Internally, this uses the same encoding mechanism as the `@GlobalScope.var_to_bytes` method.

