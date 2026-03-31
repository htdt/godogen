## AESContext <- RefCounted

This class holds the context information required for encryption and decryption operations with AES (Advanced Encryption Standard). Both AES-ECB and AES-CBC modes are supported.

**Methods:**
- finish() - Close this AES context so it can be started again. See `start`.
- get_iv_state() -> PackedByteArray - Get the current IV state for this context (IV gets updated when calling `update`). You normally don't need this function. **Note:** This function only makes sense when the context is started with `MODE_CBC_ENCRYPT` or `MODE_CBC_DECRYPT`.
- start(mode: int, key: PackedByteArray, iv: PackedByteArray = PackedByteArray()) -> int - Start the AES context in the given `mode`. A `key` of either 16 or 32 bytes must always be provided, while an `iv` (initialization vector) of exactly 16 bytes, is only needed when `mode` is either `MODE_CBC_ENCRYPT` or `MODE_CBC_DECRYPT`.
- update(src: PackedByteArray) -> PackedByteArray - Run the desired operation for this AES context. Will return a PackedByteArray containing the result of encrypting (or decrypting) the given `src`. See `start` for mode of operation. **Note:** The size of `src` must be a multiple of 16. Apply some padding if needed.

**Enums:**
**Mode:** MODE_ECB_ENCRYPT=0, MODE_ECB_DECRYPT=1, MODE_CBC_ENCRYPT=2, MODE_CBC_DECRYPT=3, MODE_MAX=4
  - MODE_ECB_ENCRYPT: AES electronic codebook encryption mode.
  - MODE_ECB_DECRYPT: AES electronic codebook decryption mode.
  - MODE_CBC_ENCRYPT: AES cipher block chaining encryption mode.
  - MODE_CBC_DECRYPT: AES cipher block chaining decryption mode.
  - MODE_MAX: Maximum value for the mode enum.

