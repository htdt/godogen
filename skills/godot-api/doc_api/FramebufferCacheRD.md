## FramebufferCacheRD <- Object

Framebuffer cache manager for RenderingDevice-based renderers. Provides a way to create a framebuffer and reuse it in subsequent calls for as long as the used textures exists. Framebuffers will automatically be cleaned up when dependent objects are freed.

**Methods:**
- get_cache_multipass(textures: RID[], passes: RDFramebufferPass[], views: int) -> RID - Creates, or obtains a cached, framebuffer. `textures` lists textures accessed. `passes` defines the subpasses and texture allocation, if left empty a single pass is created and textures are allocated depending on their usage flags. `views` defines the number of views used when rendering.

