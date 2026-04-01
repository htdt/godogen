# Coordinating Scene + Script

When a task requires both scene(s) and script(s):

1. **Generate scenes first** — scenes define the node hierarchy that scripts reference via `@onready`
2. **Follow the build order** — `STRUCTURE.md` `## Build Order` lists the exact sequence. Follow it mechanically.
3. **Connect signals in scripts, not scenes** — signal connections go in `_ready()`, NOT in scene builders (scripts aren't instantiated at build-time)

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
