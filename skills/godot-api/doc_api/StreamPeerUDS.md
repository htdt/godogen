## StreamPeerUDS <- StreamPeerSocket

A stream peer that handles UNIX Domain Socket (UDS) connections. This object can be used to connect to UDS servers, or also is returned by a UDS server. Unix Domain Sockets provide inter-process communication on the same machine using the filesystem namespace. **Note:** UNIX Domain Sockets are only available on UNIX-like systems (Linux, macOS, etc.) and are not supported on Windows.

**Methods:**
- bind(path: String) -> int - Opens the UDS socket, and binds it to the specified socket path. This method is generally not needed, and only used to force the subsequent call to `connect_to_host` to use the specified `path` as the source address.
- connect_to_host(path: String) -> int - Connects to the specified UNIX Domain Socket path. Returns `OK` on success.
- get_connected_path() -> String - Returns the socket path of this peer.

