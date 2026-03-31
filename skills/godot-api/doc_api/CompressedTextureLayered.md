## CompressedTextureLayered <- TextureLayered

Base class for CompressedTexture2DArray and CompressedTexture3D. Cannot be used directly, but contains all the functions necessary for accessing the derived resource types. See also TextureLayered.

**Props:**
- load_path: String = ""

- **load_path**: The path the texture should be loaded from.

**Methods:**
- load(path: String) -> int - Loads the texture at `path`.

