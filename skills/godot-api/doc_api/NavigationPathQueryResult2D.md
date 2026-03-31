## NavigationPathQueryResult2D <- RefCounted

This class stores the result of a 2D navigation path query from the NavigationServer2D.

**Props:**
- path: PackedVector2Array = PackedVector2Array()
- path_length: float = 0.0
- path_owner_ids: PackedInt64Array = PackedInt64Array()
- path_rids: RID[] = []
- path_types: PackedInt32Array = PackedInt32Array()

- **path**: The resulting path array from the navigation query. All path array positions are in global coordinates. Without customized query parameters this is the same path as returned by `NavigationServer2D.map_get_path`.
- **path_length**: Returns the length of the path.
- **path_owner_ids**: The `ObjectID`s of the Objects which manage the regions and links each point of the path goes through.
- **path_rids**: The RIDs of the regions and links that each point of the path goes through.
- **path_types**: The type of navigation primitive (region or link) that each point of the path goes through.

**Methods:**
- reset() - Reset the result object to its initial state. This is useful to reuse the object across multiple queries.

**Enums:**
**PathSegmentType:** PATH_SEGMENT_TYPE_REGION=0, PATH_SEGMENT_TYPE_LINK=1
  - PATH_SEGMENT_TYPE_REGION: This segment of the path goes through a region.
  - PATH_SEGMENT_TYPE_LINK: This segment of the path goes through a link.

