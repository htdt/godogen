# Coordinating Scene + Script

When a task requires both scene(s) and script(s):

1. **Generate scenes first** — scenes define the node hierarchy that scripts reference via `@onready`
1b. **Follow the build order** — `STRUCTURE.md` contains a `## Build Order` section listing the exact sequence of scene builder executions. Follow this order mechanically instead of inferring dependencies from scene references.
2. **Name nodes predictably** — scripts use `@onready var x: Type = $NodeName`, so the scene builder MUST set `.name` on every node to match
3. **Attach scripts in scene builder** — use `node.set_script(load("res://scripts/foo.gd"))` as specified in STRUCTURE.md
4. **Connect signals in scripts, not scenes** — signal connections go in the script's `_ready()`, NOT in the scene builder (scripts aren't instantiated at build-time)
5. **Match extends to node type** — the script's `extends CharacterBody3D` must match the node it's attached to in the scene

## Example

Scene builder creates the node:
```gdscript
# In scene builder (_initialize):
var player := CharacterBody3D.new()
player.name = "Player"                          # Script uses @onready $Player
var hitbox := Area3D.new()
hitbox.name = "Hitbox"                           # Script uses @onready $Hitbox
player.add_child(hitbox)
player.set_script(load("res://scripts/player_controller.gd"))
```

Runtime script references those nodes:
```gdscript
# In player_controller.gd:
extends CharacterBody3D                          # Matches node type
@onready var hitbox: Area3D = $Hitbox            # Matches .name from scene

func _ready() -> void:
    hitbox.body_entered.connect(_on_hitbox_body_entered)  # Signal connected here, not in scene
```
