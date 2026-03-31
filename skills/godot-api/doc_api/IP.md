## IP <- Object

IP contains support functions for the Internet Protocol (IP). TCP/IP support is in different classes (see StreamPeerTCP and TCPServer). IP provides DNS hostname resolution support, both blocking and threaded.

**Methods:**
- clear_cache(hostname: String = "") - Removes all of a `hostname`'s cached references. If no `hostname` is given, all cached IP addresses are removed.
- erase_resolve_item(id: int) - Removes a given item `id` from the queue. This should be used to free a queue after it has completed to enable more queries to happen.
- get_local_addresses() -> PackedStringArray - Returns all the user's current IPv4 and IPv6 addresses as an array.
- get_local_interfaces() -> Dictionary[] - Returns all network adapters as an array. Each adapter is a dictionary of the form:
- get_resolve_item_address(id: int) -> String - Returns a queued hostname's IP address, given its queue `id`. Returns an empty string on error or if resolution hasn't happened yet (see `get_resolve_item_status`).
- get_resolve_item_addresses(id: int) -> Array - Returns resolved addresses, or an empty array if an error happened or resolution didn't happen yet (see `get_resolve_item_status`).
- get_resolve_item_status(id: int) -> int - Returns a queued hostname's status as a `ResolverStatus` constant, given its queue `id`.
- resolve_hostname(host: String, ip_type: int = 3) -> String - Returns a given hostname's IPv4 or IPv6 address when resolved (blocking-type method). The address type returned depends on the `Type` constant given as `ip_type`.
- resolve_hostname_addresses(host: String, ip_type: int = 3) -> PackedStringArray - Resolves a given hostname in a blocking way. Addresses are returned as an Array of IPv4 or IPv6 addresses depending on `ip_type`.
- resolve_hostname_queue_item(host: String, ip_type: int = 3) -> int - Creates a queue item to resolve a hostname to an IPv4 or IPv6 address depending on the `Type` constant given as `ip_type`. Returns the queue ID if successful, or `RESOLVER_INVALID_ID` on error.

**Enums:**
**ResolverStatus:** RESOLVER_STATUS_NONE=0, RESOLVER_STATUS_WAITING=1, RESOLVER_STATUS_DONE=2, RESOLVER_STATUS_ERROR=3
  - RESOLVER_STATUS_NONE: DNS hostname resolver status: No status.
  - RESOLVER_STATUS_WAITING: DNS hostname resolver status: Waiting.
  - RESOLVER_STATUS_DONE: DNS hostname resolver status: Done.
  - RESOLVER_STATUS_ERROR: DNS hostname resolver status: Error.
**Constants:** RESOLVER_MAX_QUERIES=256, RESOLVER_INVALID_ID=-1
  - RESOLVER_MAX_QUERIES: Maximum number of concurrent DNS resolver queries allowed, `RESOLVER_INVALID_ID` is returned if exceeded.
  - RESOLVER_INVALID_ID: Invalid ID constant. Returned if `RESOLVER_MAX_QUERIES` is exceeded.
**Type:** TYPE_NONE=0, TYPE_IPV4=1, TYPE_IPV6=2, TYPE_ANY=3
  - TYPE_NONE: Address type: None.
  - TYPE_IPV4: Address type: Internet protocol version 4 (IPv4).
  - TYPE_IPV6: Address type: Internet protocol version 6 (IPv6).
  - TYPE_ANY: Address type: Any.

