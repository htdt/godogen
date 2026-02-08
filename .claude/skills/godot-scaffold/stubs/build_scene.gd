extends SceneTree
## Stub scene builder — scaffold fills in the vars below, scene skill replaces with full implementation.
## Run: cd {project_root} && godot --headless --script scenes/build_{name}.gd

var _root_type := "Node3D"
var _root_name := "Main"
var _script_path := ""
var _output_path := "res://scenes/main.tscn"
var _children: Array = []

func _initialize() -> void:
	var root: Node = _make_node(_root_type)
	root.name = _root_name

	if _script_path != "":
		var scr = load(_script_path)
		if scr:
			root.set_script(scr)

	for child_def in _children:
		var child_scene: PackedScene = load(child_def[1])
		if child_scene:
			var inst = child_scene.instantiate()
			inst.name = child_def[0]
			root.add_child(inst)
			inst.owner = root

	set_owner_on_new_nodes(root, root)

	var packed := PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, _output_path)
	print("Saved: " + _output_path)
	quit(0)

func set_owner_on_new_nodes(node: Node, scene_owner: Node) -> void:
	for child in node.get_children():
		child.owner = scene_owner
		if child.scene_file_path.is_empty():
			set_owner_on_new_nodes(child, scene_owner)

func _make_node(type_name: String) -> Node:
	match type_name:
		"Node": return Node.new()
		"Node2D": return Node2D.new()
		"Node3D": return Node3D.new()
		"CharacterBody2D": return CharacterBody2D.new()
		"CharacterBody3D": return CharacterBody3D.new()
		"RigidBody2D": return RigidBody2D.new()
		"RigidBody3D": return RigidBody3D.new()
		"StaticBody2D": return StaticBody2D.new()
		"StaticBody3D": return StaticBody3D.new()
		"AnimatableBody2D": return AnimatableBody2D.new()
		"AnimatableBody3D": return AnimatableBody3D.new()
		"Area2D": return Area2D.new()
		"Area3D": return Area3D.new()
		"Camera2D": return Camera2D.new()
		"Camera3D": return Camera3D.new()
		"Control": return Control.new()
		"CanvasLayer": return CanvasLayer.new()
		"SubViewport": return SubViewport.new()
		"WorldEnvironment": return WorldEnvironment.new()
		"Marker2D": return Marker2D.new()
		"Marker3D": return Marker3D.new()
	push_warning("Unknown type '" + type_name + "', using Node3D")
	return Node3D.new()
