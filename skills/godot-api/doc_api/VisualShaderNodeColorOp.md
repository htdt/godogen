## VisualShaderNodeColorOp <- VisualShaderNode

Applies `operator` to two color inputs.

**Props:**
- operator: int (VisualShaderNodeColorOp.Operator) = 0

- **operator**: An operator to be applied to the inputs.

**Enums:**
**Operator:** OP_SCREEN=0, OP_DIFFERENCE=1, OP_DARKEN=2, OP_LIGHTEN=3, OP_OVERLAY=4, OP_DODGE=5, OP_BURN=6, OP_SOFT_LIGHT=7, OP_HARD_LIGHT=8, OP_MAX=9
  - OP_SCREEN: Produce a screen effect with the following formula:
  - OP_DIFFERENCE: Produce a difference effect with the following formula:
  - OP_DARKEN: Produce a darken effect with the following formula:
  - OP_LIGHTEN: Produce a lighten effect with the following formula:
  - OP_OVERLAY: Produce an overlay effect with the following formula:
  - OP_DODGE: Produce a dodge effect with the following formula:
  - OP_BURN: Produce a burn effect with the following formula:
  - OP_SOFT_LIGHT: Produce a soft light effect with the following formula:
  - OP_HARD_LIGHT: Produce a hard light effect with the following formula:
  - OP_MAX: Represents the size of the `Operator` enum.

