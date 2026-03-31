## RandomNumberGenerator <- RefCounted

RandomNumberGenerator is a class for generating pseudo-random numbers. It currently uses . **Note:** The underlying algorithm is an implementation detail and should not be depended upon. To generate a random float number (within a given range) based on a time-dependent seed:

**Props:**
- seed: int = 0
- state: int = 0

- **seed**: Initializes the random number generator state based on the given seed value. A given seed will give a reproducible sequence of pseudo-random numbers. **Note:** The RNG does not have an avalanche effect, and can output similar random streams given similar seeds. Consider using a hash function to improve your seed quality if they're sourced externally. **Note:** Setting this property produces a side effect of changing the internal `state`, so make sure to initialize the seed *before* modifying the `state`: **Note:** The default value of this property is pseudo-random, and changes when calling `randomize`. The `0` value documented here is a placeholder, and not the actual default seed.
- **state**: The current state of the random number generator. Save and restore this property to restore the generator to a previous state: **Note:** Do not set state to arbitrary values, since the random number generator requires the state to have certain qualities to behave properly. It should only be set to values that came from the state property itself. To initialize the random number generator with arbitrary input, use `seed` instead. **Note:** The default value of this property is pseudo-random, and changes when calling `randomize`. The `0` value documented here is a placeholder, and not the actual default state.

**Methods:**
- rand_weighted(weights: PackedFloat32Array) -> int - Returns a random index with non-uniform weights. Prints an error and returns `-1` if the array is empty.
- randf() -> float - Returns a pseudo-random float between `0.0` and `1.0` (inclusive).
- randf_range(from: float, to: float) -> float - Returns a pseudo-random float between `from` and `to` (inclusive).
- randfn(mean: float = 0.0, deviation: float = 1.0) -> float - Returns a , pseudo-random floating-point number from the specified `mean` and a standard `deviation`. This is also known as a Gaussian distribution. **Note:** This method uses the algorithm.
- randi() -> int - Returns a pseudo-random 32-bit unsigned integer between `0` and `4294967295` (inclusive).
- randi_range(from: int, to: int) -> int - Returns a pseudo-random 32-bit signed integer between `from` and `to` (inclusive).
- randomize() - Sets up a time-based seed for this RandomNumberGenerator instance. Unlike the [@GlobalScope] random number generation functions, different RandomNumberGenerator instances can use different seeds.

