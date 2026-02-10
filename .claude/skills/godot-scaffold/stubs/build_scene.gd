extends SceneTree
## Scene builder template — copy to scenes/build_<name>.gd, replace placeholders.
## Run: cd {project_root} && godot --headless --script scenes/build_<name>.gd

func _initialize() -> void:
	var root := ROOT_TYPE.new()     # REPLACE ROOT_TYPE — e.g. CharacterBody3D
	root.name = "ROOT_NAME"         # REPLACE ROOT_NAME — e.g. "Player"

	# SCRIPT — delete block if no script on root
	root.set_script(load("SCRIPT_PATH"))  # REPLACE SCRIPT_PATH — e.g. "res://scripts/player.gd"

	# CHILDREN — delete block if none, duplicate per child
	var CHILD_VAR := load("CHILD_PATH").instantiate()  # REPLACE CHILD_VAR, CHILD_PATH
	CHILD_VAR.name = "CHILD_NAME"                      # REPLACE CHILD_NAME
	root.add_child(CHILD_VAR)

	# SAVE
	_set_owners(root, root)
	var packed := PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "OUTPUT_PATH")  # REPLACE OUTPUT_PATH — e.g. "res://scenes/player.tscn"
	print("Saved: OUTPUT_PATH")                # REPLACE OUTPUT_PATH
	quit(0)

func _set_owners(node: Node, owner: Node) -> void:
	for c in node.get_children():
		c.owner = owner
		if c.scene_file_path.is_empty():
			_set_owners(c, owner)
