## StreamPeerTLS <- StreamPeer

A stream peer that handles TLS connections. This object can be used to connect to a TLS server or accept a single TLS client connection. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

**Methods:**
- accept_stream(stream: StreamPeer, server_options: TLSOptions) -> int - Accepts a peer connection as a server using the given `server_options`. See `TLSOptions.server`.
- connect_to_stream(stream: StreamPeer, common_name: String, client_options: TLSOptions = null) -> int - Connects to a peer using an underlying StreamPeer `stream` and verifying the remote certificate is correctly signed for the given `common_name`. You can pass the optional `client_options` parameter to customize the trusted certification authorities, or disable the common name verification. See `TLSOptions.client` and `TLSOptions.client_unsafe`.
- disconnect_from_stream() - Disconnects from host.
- get_status() -> int - Returns the status of the connection.
- get_stream() -> StreamPeer - Returns the underlying StreamPeer connection, used in `accept_stream` or `connect_to_stream`.
- poll() - Poll the connection to check for incoming bytes. Call this right before `StreamPeer.get_available_bytes` for it to work properly.

**Enums:**
**Status:** STATUS_DISCONNECTED=0, STATUS_HANDSHAKING=1, STATUS_CONNECTED=2, STATUS_ERROR=3, STATUS_ERROR_HOSTNAME_MISMATCH=4
  - STATUS_DISCONNECTED: A status representing a StreamPeerTLS that is disconnected.
  - STATUS_HANDSHAKING: A status representing a StreamPeerTLS during handshaking.
  - STATUS_CONNECTED: A status representing a StreamPeerTLS that is connected to a host.
  - STATUS_ERROR: A status representing a StreamPeerTLS in error state.
  - STATUS_ERROR_HOSTNAME_MISMATCH: An error status that shows a mismatch in the TLS certificate domain presented by the host and the domain requested for validation.

