## PacketPeerStream <- PacketPeer

PacketStreamPeer provides a wrapper for working using packets over a stream. This allows for using packet based code with StreamPeers. PacketPeerStream implements a custom protocol over the StreamPeer, so the user should not read or write to the wrapped StreamPeer directly. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

**Props:**
- input_buffer_max_size: int = 65532
- output_buffer_max_size: int = 65532
- stream_peer: StreamPeer

- **stream_peer**: The wrapped StreamPeer object.

