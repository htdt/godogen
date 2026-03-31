## AnimationNodeSync <- AnimationNode

An animation node used to combine, mix, or blend two or more animations together while keeping them synchronized within an AnimationTree.

**Props:**
- sync: bool = false

- **sync**: If `false`, the blended animations' frame are stopped when the blend value is `0`. If `true`, forcing the blended animations to advance frame.

