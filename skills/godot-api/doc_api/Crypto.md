## Crypto <- RefCounted

The Crypto class provides access to advanced cryptographic functionalities. Currently, this includes asymmetric key encryption/decryption, signing/verification, and generating cryptographically secure random bytes, RSA keys, HMAC digests, and self-signed X509Certificates.

**Methods:**
- constant_time_compare(trusted: PackedByteArray, received: PackedByteArray) -> bool - Compares two PackedByteArrays for equality without leaking timing information in order to prevent timing attacks. See for more information.
- decrypt(key: CryptoKey, ciphertext: PackedByteArray) -> PackedByteArray - Decrypt the given `ciphertext` with the provided private `key`. **Note:** The maximum size of accepted ciphertext is limited by the key size.
- encrypt(key: CryptoKey, plaintext: PackedByteArray) -> PackedByteArray - Encrypt the given `plaintext` with the provided public `key`. **Note:** The maximum size of accepted plaintext is limited by the key size.
- generate_random_bytes(size: int) -> PackedByteArray - Generates a PackedByteArray of cryptographically secure random bytes with given `size`.
- generate_rsa(size: int) -> CryptoKey - Generates an RSA CryptoKey that can be used for creating self-signed certificates and passed to `StreamPeerTLS.accept_stream`.
- generate_self_signed_certificate(key: CryptoKey, issuer_name: String = "CN=myserver,O=myorganisation,C=IT", not_before: String = "20140101000000", not_after: String = "20340101000000") -> X509Certificate - Generates a self-signed X509Certificate from the given CryptoKey and `issuer_name`. The certificate validity will be defined by `not_before` and `not_after` (first valid date and last valid date). The `issuer_name` must contain at least "CN=" (common name, i.e. the domain name), "O=" (organization, i.e. your company name), "C=" (country, i.e. 2 lettered ISO-3166 code of the country the organization is based in). A small example to generate an RSA key and an X509 self-signed certificate.
- hmac_digest(hash_type: int, key: PackedByteArray, msg: PackedByteArray) -> PackedByteArray - Generates an digest of `msg` using `key`. The `hash_type` parameter is the hashing algorithm that is used for the inner and outer hashes. Currently, only `HashingContext.HASH_SHA256` and `HashingContext.HASH_SHA1` are supported.
- sign(hash_type: int, hash: PackedByteArray, key: CryptoKey) -> PackedByteArray - Sign a given `hash` of type `hash_type` with the provided private `key`.
- verify(hash_type: int, hash: PackedByteArray, signature: PackedByteArray, key: CryptoKey) -> bool - Verify that a given `signature` for `hash` of type `hash_type` against the provided public `key`.

