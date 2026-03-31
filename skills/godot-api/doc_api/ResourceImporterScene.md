## ResourceImporterScene <- ResourceImporter

See also ResourceImporterOBJ, which is used for OBJ models that can be imported as an independent Mesh or a scene. Additional options (such as extracting individual meshes or materials to files) are available in the **Advanced Import Settings** dialog. This dialog can be accessed by double-clicking a 3D scene in the FileSystem dock or by selecting a 3D scene in the FileSystem dock, going to the Import dock and choosing **Advanced**. **Note:** ResourceImporterScene is *not* used for PackedScenes, such as `.tscn` and `.scn` files.

**Props:**
- _subresources: Dictionary = {}
- animation/fps: float = 30
- animation/import: bool = true
- animation/import_rest_as_RESET: bool = false
- animation/remove_immutable_tracks: bool = true
- animation/trimming: bool = false
- import_script/path: String = ""
- materials/extract: int = 0
- materials/extract_format: int = 0
- materials/extract_path: String = ""
- meshes/create_shadow_meshes: bool = true
- meshes/ensure_tangents: bool = true
- meshes/force_disable_compression: bool = false
- meshes/generate_lods: bool = true
- meshes/light_baking: int = 1
- meshes/lightmap_texel_size: float = 0.2
- nodes/apply_root_scale: bool = true
- nodes/import_as_skeleton_bones: bool = false
- nodes/root_name: String = ""
- nodes/root_scale: float = 1.0
- nodes/root_script: Script = null
- nodes/root_type: String = ""
- nodes/use_name_suffixes: bool = true
- nodes/use_node_type_suffixes: bool = true
- skins/use_named_skins: bool = true

- **_subresources**: Contains properties for the scene's subresources. This is an internal option which is not visible in the Import dock.
- **animation/fps**: The number of frames per second to use for baking animation curves to a series of points with linear interpolation. It's recommended to configure this value to match the value you're using as a baseline in your 3D modeling software. Higher values result in more precise animation with fast movement changes, at the cost of higher file sizes and memory usage. Thanks to interpolation, there is usually not much benefit in going above 30 FPS (as the animation will still appear smooth at higher rendering framerates).
- **animation/import**: If `true`, import animations from the 3D scene.
- **animation/import_rest_as_RESET**: If `true`, adds an Animation named `RESET`, containing the `Skeleton3D.get_bone_rest` from Skeleton3D nodes. This can be useful to extract an animation in the reference pose.
- **animation/remove_immutable_tracks**: If `true`, remove animation tracks that only contain default values. This can reduce output file size and memory usage with certain 3D scenes, depending on the contents of their animation tracks.
- **animation/trimming**: If `true`, trim the beginning and end of animations if there are no keyframe changes. This can reduce output file size and memory usage with certain 3D scenes, depending on the contents of their animation tracks.
- **import_script/path**: Path to an import script, which can run code after the import process has completed for custom processing. See for more information.
- **materials/extract**: Material extraction mode. - `0 (Keep Internal)`, materials are not extracted. - `1 (Extract Once)`, materials are extracted once and reused on subsequent import. - `2 (Extract and Overwrite)`, materials are extracted and overwritten on every import.
- **materials/extract_format**: Extracted material file format. - `0 (Text)`, text file format (`*.tres`). - `1 (Binary)`, binary file format (`*.res`). - `2 (Material)`, binary file format (`*.material`).
- **materials/extract_path**: Path extracted materials are saved to. If empty, source scene path is used.
- **meshes/create_shadow_meshes**: If `true`, enables the generation of shadow meshes on import. This optimizes shadow rendering without reducing quality by welding vertices together when possible. This in turn reduces the memory bandwidth required to render shadows. Shadow mesh generation currently doesn't support using a lower detail level than the source mesh (but shadow rendering will make use of LODs when relevant).
- **meshes/ensure_tangents**: If `true`, generate vertex tangents using if the input meshes don't have tangent data. When possible, it's recommended to let the 3D modeling software generate tangents on export instead on relying on this option. Tangents are required for correct display of normal and height maps, along with any material/shader features that require tangents. If you don't need material features that require tangents, disabling this can reduce output file size and speed up importing if the source 3D file doesn't contain tangents.
- **meshes/force_disable_compression**: If `true`, mesh compression will not be used. Consider enabling if you notice blocky artifacts in your mesh normals or UVs, or if you have meshes that are larger than a few thousand meters in each direction.
- **meshes/generate_lods**: If `true`, generates lower detail variants of the mesh which will be displayed in the distance to improve rendering performance. Not all meshes benefit from LOD, especially if they are never rendered from far away. Disabling this can reduce output file size and speed up importing. See for more information.
- **meshes/light_baking**: Configures the meshes' `GeometryInstance3D.gi_mode` in the 3D scene. If set to **Static Lightmaps**, sets the meshes' GI mode to Static and generates UV2 on import for LightmapGI baking.
- **meshes/lightmap_texel_size**: Controls the size of each texel on the baked lightmap. A smaller value results in more precise lightmaps, at the cost of larger lightmap sizes and longer bake times. **Note:** Only effective if `meshes/light_baking` is set to **Static Lightmaps**.
- **nodes/apply_root_scale**: If `true`, `nodes/root_scale` will be applied to the descendant nodes, meshes, animations, bones, etc. This means that if you add a child node later on within the imported scene, it won't be scaled. If `false`, `nodes/root_scale` will multiply the scale of the root node instead.
- **nodes/import_as_skeleton_bones**: Treat all nodes in the imported scene as if they are bones within a single Skeleton3D. Can be used to guarantee that imported animations target skeleton bones rather than nodes. May also be used to assign the `"Root"` bone in a BoneMap. See for more information.
- **nodes/root_name**: Override for the root node name. If empty, the root node will use what the scene specifies, or the file name if the scene does not specify a root name.
- **nodes/root_scale**: The uniform scale to use for the scene root. The default value of `1.0` will not perform any rescaling. See `nodes/apply_root_scale` for details of how this scale is applied.
- **nodes/root_script**: If set to a valid script, attaches the script to the root node of the imported scene. If the type of the root node is not compatible with the script, the root node will be replaced with a type that is compatible with the script. This setting can also be used on other non-mesh nodes in the scene to attach scripts to them.
- **nodes/root_type**: Override for the root node type. If empty, the root node will use what the scene specifies, or Node3D if the scene does not specify a root type. Using a node type that inherits from Node3D is recommended. Otherwise, you'll lose the ability to position the node directly in the 3D editor.
- **nodes/use_name_suffixes**: If `true`, will use suffixes in the names of imported objects such as nodes and resources to determine types and properties, such as `-noimp` to skip import of a node or animation, `-alpha` to enable alpha transparency on a material, and `-vcol` to enable vertex colors on a material. Disabling this makes editor-imported files more similar to the original files, and more similar to files imported at runtime. See for more information.
- **nodes/use_node_type_suffixes**: If `true`, will use suffixes in the node names to determine the node type, such as `-col` for collision shapes. This is only used when `nodes/use_name_suffixes` is `true`. Disabling this makes editor-imported files more similar to the original files, and more similar to files imported at runtime. See for more information.
- **skins/use_named_skins**: If checked, use named Skins for animation. The MeshInstance3D node contains 3 properties of relevance here: a skeleton NodePath pointing to the Skeleton3D node (usually `..`), a mesh, and a skin: - The Skeleton3D node contains a list of bones with names, their pose and rest, a name and a parent bone. - The mesh is all of the raw vertex data needed to display a mesh. In terms of the mesh, it knows how vertices are weight-painted and uses some internal numbering often imported from 3D modeling software. - The skin contains the information necessary to bind this mesh onto this Skeleton3D. For every one of the internal bone IDs chosen by the 3D modeling software, it contains two things. Firstly, a matrix known as the Bind Pose Matrix, Inverse Bind Matrix, or IBM for short. Secondly, the Skin contains each bone's name (if `skins/use_named_skins` is `true`), or the bone's index within the Skeleton3D list (if `skins/use_named_skins` is `false`). Together, this information is enough to tell Godot how to use the bone poses in the Skeleton3D node to render the mesh from each MeshInstance3D. Note that each MeshInstance3D may share binds, as is common in models exported from Blender, or each MeshInstance3D may use a separate Skin object, as is common in models exported from other tools such as Maya.

