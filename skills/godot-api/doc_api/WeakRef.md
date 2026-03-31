## WeakRef <- RefCounted

A weakref can hold a RefCounted without contributing to the reference counter. A weakref can be created from an Object using `@GlobalScope.weakref`. If this object is not a reference, weakref still works, however, it does not have any effect on the object. Weakrefs are useful in cases where multiple classes have variables that refer to each other. Without weakrefs, using these classes could lead to memory leaks, since both references keep each other from being released. Making part of the variables a weakref can prevent this cyclic dependency, and allows the references to be released.

**Methods:**
- get_ref() -> Variant - Returns the Object this weakref is referring to. Returns `null` if that object no longer exists.

