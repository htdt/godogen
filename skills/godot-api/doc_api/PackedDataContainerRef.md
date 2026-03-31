## PackedDataContainerRef <- RefCounted

When packing nested containers using PackedDataContainer, they are recursively packed into PackedDataContainerRef (only applies to Array and Dictionary). Their data can be retrieved the same way as from PackedDataContainer. Prints: [codeblock lang=text] 1 2 3 ::nested1 ::nested2 4 5 6 [/codeblock]

**Methods:**
- size() -> int - Returns the size of the packed container (see `Array.size` and `Dictionary.size`).

