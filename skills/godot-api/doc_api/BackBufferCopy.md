## BackBufferCopy <- Node2D

Node for back-buffering the currently-displayed screen. The region defined in the BackBufferCopy node is buffered with the content of the screen it covers, or the entire screen according to the `copy_mode`. It can be accessed in shader scripts using the screen texture (i.e. a uniform sampler with `hint_screen_texture`). **Note:** Since this node inherits from Node2D (and not Control), anchors and margins won't apply to child Control-derived nodes. This can be problematic when resizing the window. To avoid this, add Control-derived nodes as *siblings* to the BackBufferCopy node instead of adding them as children.

**Props:**
- copy_mode: int (BackBufferCopy.CopyMode) = 1
- rect: Rect2 = Rect2(-100, -100, 200, 200)

- **copy_mode**: Buffer mode.
- **rect**: The area covered by the BackBufferCopy. Only used if `copy_mode` is `COPY_MODE_RECT`.

**Enums:**
**CopyMode:** COPY_MODE_DISABLED=0, COPY_MODE_RECT=1, COPY_MODE_VIEWPORT=2
  - COPY_MODE_DISABLED: Disables the buffering mode. This means the BackBufferCopy node will directly use the portion of screen it covers.
  - COPY_MODE_RECT: BackBufferCopy buffers a rectangular region.
  - COPY_MODE_VIEWPORT: BackBufferCopy buffers the entire screen.

