## HTTPRequest <- Node

A node with the ability to send HTTP requests. Uses HTTPClient internally. Can be used to make HTTP requests, i.e. download or upload files or web content via HTTP. **Warning:** See the notes and warnings on HTTPClient for limitations, especially regarding TLS security. **Note:** When exporting to Android, make sure to enable the `INTERNET` permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android. **Example:** Contact a REST API and print one of its returned fields: **Example:** Load an image using HTTPRequest and display it: **Note:** HTTPRequest nodes will automatically handle decompression of response bodies. An `Accept-Encoding` header will be automatically added to each of your requests, unless one is already specified. Any response with a `Content-Encoding: gzip` header will automatically be decompressed and delivered to you as uncompressed bytes.

**Props:**
- accept_gzip: bool = true
- body_size_limit: int = -1
- download_chunk_size: int = 65536
- download_file: String = ""
- max_redirects: int = 8
- timeout: float = 0.0
- use_threads: bool = false

- **accept_gzip**: If `true`, this header will be added to each request: `Accept-Encoding: gzip, deflate` telling servers that it's okay to compress response bodies. Any Response body declaring a `Content-Encoding` of either `gzip` or `deflate` will then be automatically decompressed, and the uncompressed bytes will be delivered via `request_completed`. If the user has specified their own `Accept-Encoding` header, then no header will be added regardless of `accept_gzip`. If `false` no header will be added, and no decompression will be performed on response bodies. The raw bytes of the response body will be returned via `request_completed`.
- **body_size_limit**: Maximum allowed size for response bodies. If the response body is compressed, this will be used as the maximum allowed size for the decompressed body.
- **download_chunk_size**: The size of the buffer used and maximum bytes to read per iteration. See `HTTPClient.read_chunk_size`. Set this to a lower value (e.g. 4096 for 4 KiB) when downloading small files to decrease memory usage at the cost of download speeds.
- **download_file**: The file to download into. Will output any received file into it.
- **max_redirects**: Maximum number of allowed redirects.
- **timeout**: The duration to wait before a request times out, in seconds (independent of `Engine.time_scale`). If `timeout` is set to `0.0`, the request will never time out. For simple requests, such as communication with a REST API, it is recommended to set `timeout` to a value suitable for the server response time (commonly between `1.0` and `10.0`). This will help prevent unwanted timeouts caused by variation in response times while still allowing the application to detect when a request has timed out. For larger requests such as file downloads, it is recommended to set `timeout` to `0.0`, disabling the timeout functionality. This will help prevent large transfers from failing due to exceeding the timeout value.
- **use_threads**: If `true`, multithreading is used to improve performance.

**Methods:**
- cancel_request() - Cancels the current request.
- get_body_size() -> int - Returns the response body length. **Note:** Some Web servers may not send a body length. In this case, the value returned will be `-1`. If using chunked transfer encoding, the body length will also be `-1`.
- get_downloaded_bytes() -> int - Returns the number of bytes this HTTPRequest downloaded.
- get_http_client_status() -> int - Returns the current status of the underlying HTTPClient.
- request(url: String, custom_headers: PackedStringArray = PackedStringArray(), method: int = 0, request_data: String = "") -> int - Creates request on the underlying HTTPClient. If there is no configuration errors, it tries to connect using `HTTPClient.connect_to_host` and passes parameters onto `HTTPClient.request`. Returns `OK` if request is successfully created. (Does not imply that the server has responded), `ERR_UNCONFIGURED` if not in the tree, `ERR_BUSY` if still processing previous request, `ERR_INVALID_PARAMETER` if given string is not a valid URL format, or `ERR_CANT_CONNECT` if not using thread and the HTTPClient cannot connect to host. **Note:** When `method` is `HTTPClient.METHOD_GET`, the payload sent via `request_data` might be ignored by the server or even cause the server to reject the request (check for more details). As a workaround, you can send data as a query string in the URL (see `String.uri_encode` for an example). **Note:** It's recommended to use transport encryption (TLS) and to avoid sending sensitive information (such as login credentials) in HTTP GET URL parameters. Consider using HTTP POST requests or HTTP headers for such information instead.
- request_raw(url: String, custom_headers: PackedStringArray = PackedStringArray(), method: int = 0, request_data_raw: PackedByteArray = PackedByteArray()) -> int - Creates request on the underlying HTTPClient using a raw array of bytes for the request body. If there is no configuration errors, it tries to connect using `HTTPClient.connect_to_host` and passes parameters onto `HTTPClient.request`. Returns `OK` if request is successfully created. (Does not imply that the server has responded), `ERR_UNCONFIGURED` if not in the tree, `ERR_BUSY` if still processing previous request, `ERR_INVALID_PARAMETER` if given string is not a valid URL format, or `ERR_CANT_CONNECT` if not using thread and the HTTPClient cannot connect to host.
- set_http_proxy(host: String, port: int) - Sets the proxy server for HTTP requests. The proxy server is unset if `host` is empty or `port` is -1.
- set_https_proxy(host: String, port: int) - Sets the proxy server for HTTPS requests. The proxy server is unset if `host` is empty or `port` is -1.
- set_tls_options(client_options: TLSOptions) - Sets the TLSOptions to be used when connecting to an HTTPS server. See `TLSOptions.client`.

**Signals:**
- request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) - Emitted when a request is completed.

**Enums:**
**Result:** RESULT_SUCCESS=0, RESULT_CHUNKED_BODY_SIZE_MISMATCH=1, RESULT_CANT_CONNECT=2, RESULT_CANT_RESOLVE=3, RESULT_CONNECTION_ERROR=4, RESULT_TLS_HANDSHAKE_ERROR=5, RESULT_NO_RESPONSE=6, RESULT_BODY_SIZE_LIMIT_EXCEEDED=7, RESULT_BODY_DECOMPRESS_FAILED=8, RESULT_REQUEST_FAILED=9, ...
  - RESULT_SUCCESS: Request successful.
  - RESULT_CHUNKED_BODY_SIZE_MISMATCH: Request failed due to a mismatch between the expected and actual chunked body size during transfer. Possible causes include network errors, server misconfiguration, or issues with chunked encoding.
  - RESULT_CANT_CONNECT: Request failed while connecting.
  - RESULT_CANT_RESOLVE: Request failed while resolving.
  - RESULT_CONNECTION_ERROR: Request failed due to connection (read/write) error.
  - RESULT_TLS_HANDSHAKE_ERROR: Request failed on TLS handshake.
  - RESULT_NO_RESPONSE: Request does not have a response (yet).
  - RESULT_BODY_SIZE_LIMIT_EXCEEDED: Request exceeded its maximum size limit, see `body_size_limit`.
  - RESULT_BODY_DECOMPRESS_FAILED: Request failed due to an error while decompressing the response body. Possible causes include unsupported or incorrect compression format, corrupted data, or incomplete transfer.
  - RESULT_REQUEST_FAILED: Request failed (currently unused).
  - RESULT_DOWNLOAD_FILE_CANT_OPEN: HTTPRequest couldn't open the download file.
  - RESULT_DOWNLOAD_FILE_WRITE_ERROR: HTTPRequest couldn't write to the download file.
  - RESULT_REDIRECT_LIMIT_REACHED: Request reached its maximum redirect limit, see `max_redirects`.
  - RESULT_TIMEOUT: Request failed due to a timeout. If you expect requests to take a long time, try increasing the value of `timeout` or setting it to `0.0` to remove the timeout completely.

