## StreamPeerSocket <- StreamPeer

StreamPeerSocket is an abstract base class that defines common behavior for socket-based streams.

**Methods:**
- disconnect_from_host() - Disconnects from host.
- get_status() -> int - Returns the status of the connection.
- poll() -> int - Polls the socket, updating its state. See `get_status`.

**Enums:**
**Status:** STATUS_NONE=0, STATUS_CONNECTING=1, STATUS_CONNECTED=2, STATUS_ERROR=3
  - STATUS_NONE: The initial status of the StreamPeerSocket. This is also the status after disconnecting.
  - STATUS_CONNECTING: A status representing a StreamPeerSocket that is connecting to a host.
  - STATUS_CONNECTED: A status representing a StreamPeerSocket that is connected to a host.
  - STATUS_ERROR: A status representing a StreamPeerSocket in error state.

