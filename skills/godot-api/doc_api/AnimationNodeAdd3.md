## AnimationNodeAdd3 <- AnimationNodeSync

A resource to add to an AnimationNodeBlendTree. Blends two animations out of three additively out of three based on the amount value. This animation node has three inputs: - The base animation to add to - A "-add" animation to blend with when the blend amount is negative - A "+add" animation to blend with when the blend amount is positive If the absolute value of the amount is greater than `1.0`, the animation connected to "in" port is blended with the amplified animation connected to "-add"/"+add" port. **Note:** The signs are only used to distinguish ports, and additive blending occurs based on absolute values always, meaning the animation of a "-add" port does not subtract from the animation of an "in" port.

