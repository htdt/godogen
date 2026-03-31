## PackedInt64Array

An array specifically designed to hold 64-bit integer values. Packs data tightly, so it saves memory for large array sizes. **Note:** This type stores signed 64-bit integers, which means it can take values in the interval `[-2^63, 2^63 - 1]`, i.e. `[-9223372036854775808, 9223372036854775807]`. Exceeding those bounds will wrap around. If you only need to pack 32-bit integers tightly, see PackedInt32Array for a more memory-friendly alternative. **Differences between packed arrays, typed arrays, and untyped arrays:** Packed arrays are generally faster to iterate on and modify compared to a typed array of the same type (e.g. PackedInt64Array versus `Array[int]`). Also, packed arrays consume less memory. As a downside, packed arrays are less flexible as they don't offer as many convenience methods such as `Array.map`. Typed arrays are in turn faster to iterate on and modify than untyped arrays. **Note:** Packed arrays are always passed by reference. To get a copy of an array that can be modified independently of the original array, use `duplicate`. This is *not* the case for built-in properties and methods. In these cases the returned packed array is a copy, and changing it will *not* affect the original value. To update a built-in property of this type, modify the returned array and then assign it to the property again. **Note:** In a boolean context, a packed array will evaluate to `false` if it's empty. Otherwise, a packed array will always evaluate to `true`.

**Methods:**
- append(value: int) -> bool - Appends an element at the end of the array (alias of `push_back`).
- append_array(array: PackedInt64Array) - Appends a PackedInt64Array at the end of this array.
- bsearch(value: int, before: bool = true) -> int - Finds the index of an existing value (or the insertion index that maintains sorting order, if the value is not yet present in the array) using binary search. Optionally, a `before` specifier can be passed. If `false`, the returned index comes after all existing entries of the value in the array. **Note:** Calling `bsearch` on an unsorted array results in unexpected behavior.
- clear() - Clears the array. This is equivalent to using `resize` with a size of `0`.
- count(value: int) -> int - Returns the number of times an element is in the array.
- duplicate() -> PackedInt64Array - Creates a copy of the array, and returns it.
- erase(value: int) -> bool - Removes the first occurrence of a value from the array and returns `true`. If the value does not exist in the array, nothing happens and `false` is returned. To remove an element by index, use `remove_at` instead.
- fill(value: int) - Assigns the given value to all elements in the array. This can typically be used together with `resize` to create an array with a given size and initialized elements.
- find(value: int, from: int = 0) -> int - Searches the array for a value and returns its index or `-1` if not found. Optionally, the initial search index can be passed.
- get(index: int) -> int - Returns the 64-bit integer at the given `index` in the array. If `index` is out-of-bounds or negative, this method fails and returns `0`. This method is similar (but not identical) to the `[]` operator. Most notably, when this method fails, it doesn't pause project execution if run from the editor.
- has(value: int) -> bool - Returns `true` if the array contains `value`.
- insert(at_index: int, value: int) -> int - Inserts a new integer at a given position in the array. The position must be valid, or at the end of the array (`idx == size()`).
- is_empty() -> bool - Returns `true` if the array is empty.
- push_back(value: int) -> bool - Appends a value to the array.
- remove_at(index: int) - Removes an element from the array by index.
- resize(new_size: int) -> int - Sets the size of the array. If the array is grown, reserves elements at the end of the array. If the array is shrunk, truncates the array to the new size. Calling `resize` once and assigning the new values is faster than adding new elements one by one. Returns `OK` on success, or one of the following `Error` constants if this method fails: `ERR_INVALID_PARAMETER` if the size is negative, or `ERR_OUT_OF_MEMORY` if allocations fail. Use `size` to find the actual size of the array after resize.
- reverse() - Reverses the order of the elements in the array.
- rfind(value: int, from: int = -1) -> int - Searches the array in reverse order. Optionally, a start search index can be passed. If negative, the start index is considered relative to the end of the array.
- set(index: int, value: int) - Changes the integer at the given index.
- size() -> int - Returns the number of elements in the array.
- slice(begin: int, end: int = 2147483647) -> PackedInt64Array - Returns the slice of the PackedInt64Array, from `begin` (inclusive) to `end` (exclusive), as a new PackedInt64Array. The absolute value of `begin` and `end` will be clamped to the array size, so the default value for `end` makes it slice to the size of the array by default (i.e. `arr.slice(1)` is a shorthand for `arr.slice(1, arr.size())`). If either `begin` or `end` are negative, they will be relative to the end of the array (i.e. `arr.slice(0, -2)` is a shorthand for `arr.slice(0, arr.size() - 2)`).
- sort() - Sorts the elements of the array in ascending order.
- to_byte_array() -> PackedByteArray - Returns a copy of the data converted to a PackedByteArray, where each element has been encoded as 8 bytes. The size of the new array will be `int64_array.size() * 8`.

