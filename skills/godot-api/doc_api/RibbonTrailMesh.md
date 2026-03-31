## RibbonTrailMesh <- PrimitiveMesh

RibbonTrailMesh represents a straight ribbon-shaped mesh with variable width. The ribbon is composed of a number of flat or cross-shaped sections, each with the same `section_length` and number of `section_segments`. A `curve` is sampled along the total length of the ribbon, meaning that the curve determines the size of the ribbon along its length. This primitive mesh is usually used for particle trails.

**Props:**
- curve: Curve
- section_length: float = 0.2
- section_segments: int = 3
- sections: int = 5
- shape: int (RibbonTrailMesh.Shape) = 1
- size: float = 1.0

- **curve**: Determines the size of the ribbon along its length. The size of a particular section segment is obtained by multiplying the baseline `size` by the value of this curve at the given distance. For values smaller than `0`, the faces will be inverted. Should be a unit Curve.
- **section_length**: The length of a section of the ribbon.
- **section_segments**: The number of segments in a section. The `curve` is sampled on each segment to determine its size. Higher values result in a more detailed ribbon at the cost of performance.
- **sections**: The total number of sections on the ribbon.
- **shape**: Determines the shape of the ribbon.
- **size**: The baseline size of the ribbon. The size of a particular section segment is obtained by multiplying this size by the value of the `curve` at the given distance.

**Enums:**
**Shape:** SHAPE_FLAT=0, SHAPE_CROSS=1
  - SHAPE_FLAT: Gives the mesh a single flat face.
  - SHAPE_CROSS: Gives the mesh two perpendicular flat faces, making a cross shape.

