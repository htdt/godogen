## PlaceholderTexture2DArray <- PlaceholderTextureLayered

This class is used when loading a project that uses a Texture2D subclass in 2 conditions: - When running the project exported in dedicated server mode, only the texture's dimensions are kept (as they may be relied upon for gameplay purposes or positioning of other elements). This allows reducing the exported PCK's size significantly. - When this subclass is missing due to using a different engine version or build (e.g. modules disabled). **Note:** This is not intended to be used as an actual texture for rendering. It is not guaranteed to work like one in shaders or materials (for example when calculating UV).

