## BlitMaterial <- Material

A material resource that can be used by DrawableTextures when processing blit calls to draw.

**Props:**
- blend_mode: int (BlitMaterial.BlendMode) = 0

- **blend_mode**: The manner in which the newly blitted texture is blended with the original DrawableTexture.

**Enums:**
**BlendMode:** BLEND_MODE_MIX=0, BLEND_MODE_ADD=1, BLEND_MODE_SUB=2, BLEND_MODE_MUL=3, BLEND_MODE_DISABLED=4
  - BLEND_MODE_MIX: Mix blending mode. Colors are assumed to be independent of the alpha (opacity) value.
  - BLEND_MODE_ADD: Additive blending mode.
  - BLEND_MODE_SUB: Subtractive blending mode.
  - BLEND_MODE_MUL: Multiplicative blending mode.
  - BLEND_MODE_DISABLED: No blending mode, direct color copy.

