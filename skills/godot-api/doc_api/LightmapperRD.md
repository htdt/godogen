## LightmapperRD <- Lightmapper

LightmapperRD ("RD" stands for RenderingDevice) is the built-in GPU-based lightmapper for use with LightmapGI. On most dedicated GPUs, it can bake lightmaps much faster than most CPU-based lightmappers. LightmapperRD uses compute shaders to bake lightmaps, so it does not require CUDA or OpenCL libraries to be installed to be usable. **Note:** This lightmapper requires the GPU to support the RenderingDevice backend (Forward+ and Mobile renderers). When using the Compatibility renderer, baking will use a temporary RenderingDevice. Support for RenderingDevice is not required to *render* lightmaps that were already baked beforehand.

