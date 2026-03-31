## ShaderInclude <- Resource

A shader include file, saved with the `.gdshaderinc` extension. This class allows you to define a custom shader snippet that can be included in a Shader by using the preprocessor directive `#include`, followed by the file path (e.g. `#include "res://shader_lib.gdshaderinc"`). The snippet doesn't have to be a valid shader on its own.

**Props:**
- code: String = ""

- **code**: Returns the code of the shader include file. The returned text is what the user has written, not the full generated code used internally.

