## ResourceImporter <- RefCounted

This is the base class for Godot's resource importers. To implement your own resource importers using editor plugins, see EditorImportPlugin.

**Methods:**
- _get_build_dependencies(path: String) -> PackedStringArray - Called when the engine compilation profile editor wants to check what build options an imported resource needs. For example, ResourceImporterDynamicFont has a property called `ResourceImporterDynamicFont.multichannel_signed_distance_field`, that depends on the engine to be build with the "msdfgen" module. If that resource happened to be a custom one, it would be handled like this:

**Enums:**
**ImportOrder:** IMPORT_ORDER_DEFAULT=0, IMPORT_ORDER_SCENE=100
  - IMPORT_ORDER_DEFAULT: The default import order.
  - IMPORT_ORDER_SCENE: The import order for scenes, which ensures scenes are imported *after* all other core resources such as textures. Custom importers should generally have an import order lower than `100` to avoid issues when importing scenes that rely on custom resources.

