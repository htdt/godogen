## MultiplayerPeerExtension <- MultiplayerPeer

This class is designed to be inherited from a GDExtension plugin to implement custom networking layers for the multiplayer API (such as WebRTC). All the methods below **must** be implemented to have a working custom multiplayer implementation. See also MultiplayerAPI.

**Methods:**
- _close() - Called when the multiplayer peer should be immediately closed (see `MultiplayerPeer.close`).
- _disconnect_peer(p_peer: int, p_force: bool) - Called when the connected `p_peer` should be forcibly disconnected (see `MultiplayerPeer.disconnect_peer`).
- _get_available_packet_count() -> int - Called when the available packet count is internally requested by the MultiplayerAPI.
- _get_connection_status() -> int - Called when the connection status is requested on the MultiplayerPeer (see `MultiplayerPeer.get_connection_status`).
- _get_max_packet_size() -> int - Called when the maximum allowed packet size (in bytes) is requested by the MultiplayerAPI.
- _get_packet(r_buffer: const uint8_t **, r_buffer_size: int32_t*) -> int - Called when a packet needs to be received by the MultiplayerAPI, with `r_buffer_size` being the size of the binary `r_buffer` in bytes.
- _get_packet_channel() -> int - Called to get the channel over which the next available packet was received. See `MultiplayerPeer.get_packet_channel`.
- _get_packet_mode() -> int - Called to get the transfer mode the remote peer used to send the next available packet. See `MultiplayerPeer.get_packet_mode`.
- _get_packet_peer() -> int - Called when the ID of the MultiplayerPeer who sent the most recent packet is requested (see `MultiplayerPeer.get_packet_peer`).
- _get_packet_script() -> PackedByteArray - Called when a packet needs to be received by the MultiplayerAPI, if `_get_packet` isn't implemented. Use this when extending this class via GDScript.
- _get_transfer_channel() -> int - Called when the transfer channel to use is read on this MultiplayerPeer (see `MultiplayerPeer.transfer_channel`).
- _get_transfer_mode() -> int - Called when the transfer mode to use is read on this MultiplayerPeer (see `MultiplayerPeer.transfer_mode`).
- _get_unique_id() -> int - Called when the unique ID of this MultiplayerPeer is requested (see `MultiplayerPeer.get_unique_id`). The value must be between `1` and `2147483647`.
- _is_refusing_new_connections() -> bool - Called when the "refuse new connections" status is requested on this MultiplayerPeer (see `MultiplayerPeer.refuse_new_connections`).
- _is_server() -> bool - Called when the "is server" status is requested on the MultiplayerAPI. See `MultiplayerAPI.is_server`.
- _is_server_relay_supported() -> bool - Called to check if the server can act as a relay in the current configuration. See `MultiplayerPeer.is_server_relay_supported`.
- _poll() - Called when the MultiplayerAPI is polled. See `MultiplayerAPI.poll`.
- _put_packet(p_buffer: const uint8_t*, p_buffer_size: int) -> int - Called when a packet needs to be sent by the MultiplayerAPI, with `p_buffer_size` being the size of the binary `p_buffer` in bytes.
- _put_packet_script(p_buffer: PackedByteArray) -> int - Called when a packet needs to be sent by the MultiplayerAPI, if `_put_packet` isn't implemented. Use this when extending this class via GDScript.
- _set_refuse_new_connections(p_enable: bool) - Called when the "refuse new connections" status is set on this MultiplayerPeer (see `MultiplayerPeer.refuse_new_connections`).
- _set_target_peer(p_peer: int) - Called when the target peer to use is set for this MultiplayerPeer (see `MultiplayerPeer.set_target_peer`).
- _set_transfer_channel(p_channel: int) - Called when the channel to use is set for this MultiplayerPeer (see `MultiplayerPeer.transfer_channel`).
- _set_transfer_mode(p_mode: int) - Called when the transfer mode is set on this MultiplayerPeer (see `MultiplayerPeer.transfer_mode`).

