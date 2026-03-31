## CCDIK3D <- IterateIK3D

CCDIK3D is rotation based IK, enabling fast and effective tracking even with large joint rotations. It's especially suitable for chains with limitations, providing smoother and more stable target tracking compared to FABRIK3D. The resulting twist around the forward vector will always be kept from the previous pose. **Note:** When the target is close to the root, it can cause unnatural movement, including joint flips and oscillations.

