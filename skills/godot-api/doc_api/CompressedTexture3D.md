## CompressedTexture3D <- Texture3D

CompressedTexture3D is the VRAM-compressed counterpart of ImageTexture3D. The file extension for CompressedTexture3D files is `.ctex3d`. This file format is internal to Godot; it is created by importing other image formats with the import system. CompressedTexture3D uses VRAM compression, which allows to reduce memory usage on the GPU when rendering the texture. This also improves loading times, as VRAM-compressed textures are faster to load compared to textures using lossless compression. VRAM compression can exhibit noticeable artifacts and is intended to be used for 3D rendering, not 2D. See Texture3D for a general description of 3D textures.

**Props:**
- load_path: String = ""

- **load_path**: The CompressedTexture3D's file path to a `.ctex3d` file.

**Methods:**
- load(path: String) -> int - Loads the texture from the specified `path`.

