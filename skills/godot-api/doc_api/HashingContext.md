## HashingContext <- RefCounted

The HashingContext class provides an interface for computing cryptographic hashes over multiple iterations. Useful for computing hashes of big files (so you don't have to load them all in memory), network streams, and data streams in general (so you don't have to hold buffers). The `HashType` enum shows the supported hashing algorithms.

**Methods:**
- finish() -> PackedByteArray - Closes the current context, and return the computed hash.
- start(type: int) -> int - Starts a new hash computation of the given `type` (e.g. `HASH_SHA256` to start computation of an SHA-256).
- update(chunk: PackedByteArray) -> int - Updates the computation with the given `chunk` of data.

**Enums:**
**HashType:** HASH_MD5=0, HASH_SHA1=1, HASH_SHA256=2
  - HASH_MD5: Hashing algorithm: MD5.
  - HASH_SHA1: Hashing algorithm: SHA-1.
  - HASH_SHA256: Hashing algorithm: SHA-256.

