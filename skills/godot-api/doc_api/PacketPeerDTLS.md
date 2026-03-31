## PacketPeerDTLS <- PacketPeer

This class represents a DTLS peer connection. It can be used to connect to a DTLS server, and is returned by `DTLSServer.take_connection`. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android. **Warning:** TLS certificate revocation and certificate pinning are currently not supported. Revoked certificates are accepted as long as they are otherwise valid. If this is a concern, you may want to use automatically managed certificates with a short validity period.

**Methods:**
- connect_to_peer(packet_peer: PacketPeerUDP, hostname: String, client_options: TLSOptions = null) -> int - Connects a `packet_peer` beginning the DTLS handshake using the underlying PacketPeerUDP which must be connected (see `PacketPeerUDP.connect_to_host`). You can optionally specify the `client_options` to be used while verifying the TLS connections. See `TLSOptions.client` and `TLSOptions.client_unsafe`.
- disconnect_from_peer() - Disconnects this peer, terminating the DTLS session.
- get_status() -> int - Returns the status of the connection.
- poll() - Poll the connection to check for incoming packets. Call this frequently to update the status and keep the connection working.

**Enums:**
**Status:** STATUS_DISCONNECTED=0, STATUS_HANDSHAKING=1, STATUS_CONNECTED=2, STATUS_ERROR=3, STATUS_ERROR_HOSTNAME_MISMATCH=4
  - STATUS_DISCONNECTED: A status representing a PacketPeerDTLS that is disconnected.
  - STATUS_HANDSHAKING: A status representing a PacketPeerDTLS that is currently performing the handshake with a remote peer.
  - STATUS_CONNECTED: A status representing a PacketPeerDTLS that is connected to a remote peer.
  - STATUS_ERROR: A status representing a PacketPeerDTLS in a generic error state.
  - STATUS_ERROR_HOSTNAME_MISMATCH: An error status that shows a mismatch in the DTLS certificate domain presented by the host and the domain requested for validation.

