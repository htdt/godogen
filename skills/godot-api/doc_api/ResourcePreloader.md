## ResourcePreloader <- Node

This node is used to preload sub-resources inside a scene, so when the scene is loaded, all the resources are ready to use and can be retrieved from the preloader. You can add the resources using the ResourcePreloader tab when the node is selected. GDScript has a simplified `@GDScript.preload` built-in method which can be used in most situations, leaving the use of ResourcePreloader for more advanced scenarios.

**Methods:**
- add_resource(name: StringName, resource: Resource) - Adds a resource to the preloader with the given `name`. If a resource with the given `name` already exists, the new resource will be renamed to "`name` N" where N is an incrementing number starting from 2.
- get_resource(name: StringName) -> Resource - Returns the resource associated to `name`.
- get_resource_list() -> PackedStringArray - Returns the list of resources inside the preloader.
- has_resource(name: StringName) -> bool - Returns `true` if the preloader contains a resource associated to `name`.
- remove_resource(name: StringName) - Removes the resource associated to `name` from the preloader.
- rename_resource(name: StringName, newname: StringName) - Renames a resource inside the preloader from `name` to `newname`.

