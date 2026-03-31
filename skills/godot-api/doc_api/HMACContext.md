## HMACContext <- RefCounted

The HMACContext class is useful for advanced HMAC use cases, such as streaming the message as it supports creating the message over time rather than providing it all at once.

**Methods:**
- finish() -> PackedByteArray - Returns the resulting HMAC. If the HMAC failed, an empty PackedByteArray is returned.
- start(hash_type: int, key: PackedByteArray) -> int - Initializes the HMACContext. This method cannot be called again on the same HMACContext until `finish` has been called.
- update(data: PackedByteArray) -> int - Updates the message to be HMACed. This can be called multiple times before `finish` is called to append `data` to the message, but cannot be called until `start` has been called.

