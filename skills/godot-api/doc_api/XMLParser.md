## XMLParser <- RefCounted

Provides a low-level interface for creating parsers for files. This class can serve as base to make custom XML parsers. To parse XML, you must open a file with the `open` method or a buffer with the `open_buffer` method. Then, the `read` method must be called to parse the next nodes. Most of the methods take into consideration the currently parsed node. Here is an example of using XMLParser to parse an SVG file (which is based on XML), printing each element and its attributes as a dictionary:

**Methods:**
- get_attribute_count() -> int - Returns the number of attributes in the currently parsed element. **Note:** If this method is used while the currently parsed node is not `NODE_ELEMENT` or `NODE_ELEMENT_END`, this count will not be updated and will still reflect the last element.
- get_attribute_name(idx: int) -> String - Returns the name of an attribute of the currently parsed element, specified by the `idx` index.
- get_attribute_value(idx: int) -> String - Returns the value of an attribute of the currently parsed element, specified by the `idx` index.
- get_current_line() -> int - Returns the current line in the parsed file, counting from 0.
- get_named_attribute_value(name: String) -> String - Returns the value of an attribute of the currently parsed element, specified by its `name`. This method will raise an error if the element has no such attribute.
- get_named_attribute_value_safe(name: String) -> String - Returns the value of an attribute of the currently parsed element, specified by its `name`. This method will return an empty string if the element has no such attribute.
- get_node_data() -> String - Returns the contents of a text node. This method will raise an error if the current parsed node is of any other type.
- get_node_name() -> String - Returns the name of a node. This method will raise an error if the currently parsed node is a text node. **Note:** The content of a `NODE_CDATA` node and the comment string of a `NODE_COMMENT` node are also considered names.
- get_node_offset() -> int - Returns the byte offset of the currently parsed node since the beginning of the file or buffer. This is usually equivalent to the number of characters before the read position.
- get_node_type() -> int - Returns the type of the current node. Compare with `NodeType` constants.
- has_attribute(name: String) -> bool - Returns `true` if the currently parsed element has an attribute with the `name`.
- is_empty() -> bool - Returns `true` if the currently parsed element is empty, e.g. `<element />`.
- open(file: String) -> int - Opens an XML `file` for parsing. This method returns an error code.
- open_buffer(buffer: PackedByteArray) -> int - Opens an XML raw `buffer` for parsing. This method returns an error code.
- read() -> int - Parses the next node in the file. This method returns an error code.
- seek(position: int) -> int - Moves the buffer cursor to a certain offset (since the beginning) and reads the next node there. This method returns an error code.
- skip_section() - Skips the current section. If the currently parsed node contains more inner nodes, they will be ignored and the cursor will go to the closing of the current element.

**Enums:**
**NodeType:** NODE_NONE=0, NODE_ELEMENT=1, NODE_ELEMENT_END=2, NODE_TEXT=3, NODE_COMMENT=4, NODE_CDATA=5, NODE_UNKNOWN=6
  - NODE_NONE: There's no node (no file or buffer opened).
  - NODE_ELEMENT: An element node type, also known as a tag, e.g. `<title>`.
  - NODE_ELEMENT_END: An end of element node type, e.g. `</title>`.
  - NODE_TEXT: A text node type, i.e. text that is not inside an element. This includes whitespace.
  - NODE_COMMENT: A comment node type, e.g. `<!--A comment-->`.
  - NODE_CDATA: A node type for CDATA (Character Data) sections, e.g. `<![CDATA[CDATA section]]>`.
  - NODE_UNKNOWN: An unknown node type.

