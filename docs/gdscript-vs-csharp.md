# GDScript vs C# — Skill Instruction Comparison

## What C# eliminated

**GDScript's type inference minefield is gone.** The GDScript quirks.md had a 28-line "Type Inference Errors" section documenting `:=` footguns — `instantiate()` returns Variant, polymorphic math functions (`abs`, `clamp`, `lerp`, `min`, `max`...) return Variant, array/dict element access returns Variant. All of these silently break type inference with `:=`. This entire class of errors doesn't exist in C#.

Other GDScript-specific issues removed:
- `preload()` vs `load()` ordering trap during generation
- `await` during `--write-movie` advancing frame counter
- `@onready` timing with `init()` vs `_ready()`
- `get_path()` name collision with Node built-in
- Pass-by-value workarounds needing Array accumulators (C# has `ref`/`out` and return values)

**task-execution.md shrank 14%** — the GDScript version needed `--check-only -s` per-file pre-validation step; C# replaces it with a single `dotnet build` that catches everything at once.

## What C# added

**One major quirk: `SetScript()` disposes the C# managed wrapper.** After calling `SetScript()` on a node, the C# variable is dead (`ObjectDisposedException`). This requires a "temp parent" pattern to re-obtain root nodes. It's well-contained — 12 lines of example code — and once the pattern is in the template, it's never a problem in practice.

Other C#-specific additions:
- `.csproj` file (5 lines of boilerplate, but one more file to manage)
- `dotnet build` step in the pipeline (replaces per-file `--check-only`)
- `partial` class requirement on every Godot class
- Signal delegates must end in `EventHandler`
- C# enum names are unreliable in LLM output (training data is predominantly GDScript) — explicit `godot-api` lookup instruction added

## Code comparison: asset loading

The game logic is conceptually identical — same nodes, same hierarchy, same engine API. The difference is how much the language fights you while writing it.

```gdscript
# GDScript — three traps in four lines
var scene: PackedScene = load("res://assets/glb/car.glb")  # MUST type, or load() returns Resource
var model = scene.instantiate()                              # MUST use = not :=, Variant inference
var found = find_mesh_instance(model)                        # MUST use = not :=, recursive return
```

```csharp
// C# — just works
var scene = GD.Load<PackedScene>("res://assets/glb/car.glb");  // generic returns PackedScene
var model = scene.Instantiate();                                // type flows through
var found = FindMeshInstance(model);                            // same
```

GDScript requires remembering where `var x :=` is forbidden and where explicit typing is needed. C# generics and type inference handle this automatically. The actual game logic — physics, input, camera rigs, collision setup, node hierarchy — is 1:1 identical between the two. PascalCase instead of snake_case, `new Vector3()` instead of `Vector3()`, braces instead of indentation. No conceptual difference.

## Qualitative assessment

**GDScript complexity profile:** Death by a thousand paper cuts. The type inference system creates a steady stream of subtle errors — the LLM generates plausible code that fails silently or with cryptic messages. Every `load()`, `instantiate()`, `abs()`, array access is a potential trap. The `:=` operator is the default instinct but fails on ~15 common API patterns.

**C# complexity profile:** One sharp edge (`SetScript()` disposal), one ecosystem tax (`.csproj` + `dotnet build`), one LLM bias issue (enum names from GDScript training data). Everything else is standard typed language — the compiler catches mistakes before runtime. The type system works *with* you rather than against you.

**Bottom line:** C# is not easier or harder to write *conceptually* — it's easier to write *correctly*. The compiler catches what GDScript lets through silently. C# trades GDScript's diffuse type-system complexity (many small gotchas scattered everywhere) for a small number of well-documented, well-contained sharp edges. The instructions are 9% larger by line count but carry less cognitive load — the quirks file alone went from 100 lines to 79 despite adding the `SetScript()` pattern. The LLM generates more correct code on the first try because the type system prevents the Variant inference class of errors entirely.
