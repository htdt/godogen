## FileDialog <- ConfirmationDialog

FileDialog is a preset dialog used to choose files and directories in the filesystem. It supports filter masks. FileDialog automatically sets its window title according to the `file_mode`. If you want to use a custom title, disable this by setting `mode_overrides_title` to `false`. **Note:** FileDialog is invisible by default. To make it visible, call one of the `popup_*` methods from Window on the node, such as `Window.popup_centered_clamped`.

**Props:**
- access: int (FileDialog.Access) = 0
- current_dir: String
- current_file: String
- current_path: String
- deleting_enabled: bool = true
- dialog_hide_on_ok: bool = false
- display_mode: int (FileDialog.DisplayMode) = 0
- favorites_enabled: bool = true
- file_filter_toggle_enabled: bool = true
- file_mode: int (FileDialog.FileMode) = 4
- file_sort_options_enabled: bool = true
- filename_filter: String = ""
- filters: PackedStringArray = PackedStringArray()
- folder_creation_enabled: bool = true
- hidden_files_toggle_enabled: bool = true
- layout_toggle_enabled: bool = true
- mode_overrides_title: bool = true
- option_count: int = 0
- option_{index}/default: int = 0
- option_{index}/name: String = ""
- option_{index}/values: PackedStringArray = PackedStringArray()
- overwrite_warning_enabled: bool = true
- recent_list_enabled: bool = true
- root_subfolder: String = ""
- show_hidden_files: bool = false
- size: Vector2i = Vector2i(640, 360)
- title: String = "Save a File"
- use_native_dialog: bool = false

- **access**: The file system access scope. **Warning:** In Web builds, FileDialog cannot access the host file system. In sandboxed Linux and macOS environments, `use_native_dialog` is automatically used to allow limited access to host file system.
- **current_dir**: The current working directory of the file dialog. **Note:** For native file dialogs, this property is only treated as a hint and may not be respected by specific OS implementations.
- **current_file**: The currently selected file of the file dialog.
- **current_path**: The currently selected file path of the file dialog.
- **deleting_enabled**: If `true`, the context menu will show the "Delete" option, which allows moving files and folders to trash.
- **display_mode**: Display mode of the dialog's file list.
- **favorites_enabled**: If `true`, shows the toggle favorite button and favorite list on the left side of the dialog.
- **file_filter_toggle_enabled**: If `true`, shows the toggle file filter button.
- **file_mode**: The dialog's open or save mode, which affects the selection behavior.
- **file_sort_options_enabled**: If `true`, shows the file sorting options button.
- **filename_filter**: The filter for file names (case-insensitive). When set to a non-empty string, only files that contains the substring will be shown. `filename_filter` can be edited by the user with the filter button at the top of the file dialog. See also `filters`, which should be used to restrict the file types that can be selected instead of `filename_filter` which is meant to be set by the user.
- **filters**: The available file type filters. Each filter string in the array should be formatted like this: `*.png,*.jpg,*.jpeg;Image Files;image/png,image/jpeg`. The description text of the filter is optional and can be omitted. Both file extensions and MIME type should be always set. **Note:** Embedded file dialogs and Windows file dialogs support only file extensions, while Android, Linux, and macOS file dialogs also support MIME types.
- **folder_creation_enabled**: If `true`, shows the button for creating new directories (when using `FILE_MODE_OPEN_DIR`, `FILE_MODE_OPEN_ANY`, or `FILE_MODE_SAVE_FILE`), and the context menu will have the "New Folder..." option.
- **hidden_files_toggle_enabled**: If `true`, shows the toggle hidden files button.
- **layout_toggle_enabled**: If `true`, shows the layout switch buttons (list/thumbnails).
- **mode_overrides_title**: If `true`, changing the `file_mode` property will set the window title accordingly (e.g. setting `file_mode` to `FILE_MODE_OPEN_FILE` will change the window title to "Open a File").
- **option_count**: The number of additional OptionButtons and CheckBoxes in the dialog.
- **option_{index}/default**: The default value for the option at `index`. **Note:** `index` is a value in the `0 .. option_count - 1` range.
- **option_{index}/name**: The name of the option at `index`. **Note:** `index` is a value in the `0 .. option_count - 1` range.
- **option_{index}/values**: The list of values for the option at `index`. **Note:** `index` is a value in the `0 .. option_count - 1` range.
- **overwrite_warning_enabled**: If `true`, the FileDialog will warn the user before overwriting files in save mode.
- **recent_list_enabled**: If `true`, shows the recent directories list on the left side of the dialog.
- **root_subfolder**: If non-empty, the given sub-folder will be "root" of this FileDialog, i.e. user won't be able to go to its parent directory. **Note:** This property is ignored by native file dialogs.
- **show_hidden_files**: If `true`, the dialog will show hidden files. **Note:** This property is ignored by native file dialogs on Android and Linux.
- **use_native_dialog**: If `true`, and if supported by the current DisplayServer, OS native dialog will be used instead of custom one. **Note:** On Android, it is only supported when using `ACCESS_FILESYSTEM`. For access mode `ACCESS_RESOURCES` and `ACCESS_USERDATA`, the system will fall back to custom FileDialog. **Note:** On Linux and macOS, sandboxed apps always use native dialogs to access the host file system. **Note:** On macOS, sandboxed apps will save security-scoped bookmarks to retain access to the opened folders across multiple sessions. Use `OS.get_granted_permissions` to get a list of saved bookmarks. **Note:** Native dialogs are isolated from the base process, file dialog properties can't be modified once the dialog is shown. **Note:** This property is ignored in EditorFileDialog.

**Methods:**
- add_filter(filter: String, description: String = "", mime_type: String = "") - Adds a comma-separated file extension `filter` and comma-separated MIME type `mime_type` option to the FileDialog with an optional `description`, which restricts what files can be picked. A `filter` should be of the form `"filename.extension"`, where filename and extension can be `*` to match any string. Filters starting with `.` (i.e. empty filenames) are not allowed. For example, a `filter` of `"*.png, *.jpg"`, a `mime_type` of `image/png, image/jpeg`, and a `description` of `"Images"` results in filter text "Images (*.png, *.jpg)". **Note:** Embedded file dialogs and Windows file dialogs support only file extensions, while Android, Linux, and macOS file dialogs also support MIME types.
- add_option(name: String, values: PackedStringArray, default_value_index: int) - Adds an additional OptionButton to the file dialog. If `values` is empty, a CheckBox is added instead. `default_value_index` should be an index of the value in the `values`. If `values` is empty it should be either `1` (checked), or `0` (unchecked).
- clear_filename_filter() - Clear the filter for file names.
- clear_filters() - Clear all the added filters in the dialog.
- deselect_all() - Clear all currently selected items in the dialog.
- get_favorite_list() -> PackedStringArray - Returns the list of favorite directories, which is shared by all FileDialog nodes. Useful to store the list of favorites between project sessions. This method can be called only from the main thread.
- get_line_edit() -> LineEdit - Returns the LineEdit for the selected file. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.
- get_option_default(option: int) -> int - Returns the default value index of the OptionButton or CheckBox with index `option`.
- get_option_name(option: int) -> String - Returns the name of the OptionButton or CheckBox with index `option`.
- get_option_values(option: int) -> PackedStringArray - Returns an array of values of the OptionButton with index `option`.
- get_recent_list() -> PackedStringArray - Returns the list of recent directories, which is shared by all FileDialog nodes. Useful to store the list of recents between project sessions. This method can be called only from the main thread.
- get_selected_options() -> Dictionary - Returns a Dictionary with the selected values of the additional OptionButtons and/or CheckBoxes. Dictionary keys are names and values are selected value indices.
- get_vbox() -> VBoxContainer - Returns the vertical box container of the dialog, custom controls can be added to it. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property. **Note:** Changes to this node are ignored by native file dialogs, use `add_option` to add custom elements to the dialog instead.
- invalidate() - Invalidates and updates this dialog's content list. **Note:** This method does nothing on native file dialogs.
- is_customization_flag_enabled(flag: int) -> bool - Returns `true` if the provided `flag` is enabled.
- popup_file_dialog() - Shows the FileDialog using the default size and position for file dialogs, and selects the file name if there is a current file.
- set_customization_flag_enabled(flag: int, enabled: bool) - Sets the specified customization `flag`, allowing to customize the features available in this FileDialog.
- set_favorite_list(favorites: PackedStringArray) - Sets the list of favorite directories, which is shared by all FileDialog nodes. Useful to restore the list of favorites saved with `get_favorite_list`. This method can be called only from the main thread. **Note:** FileDialog will update its internal ItemList of favorites when its visibility changes. Be sure to call this method earlier if you want your changes to have effect.
- set_get_icon_callback(callback: Callable) - Sets the callback used by the FileDialog nodes to get a file icon, when `DISPLAY_LIST` mode is used. The callback should take a single String argument (file path), and return a Texture2D. If an invalid texture is returned, the [theme_item file] icon will be used instead.
- set_get_thumbnail_callback(callback: Callable) - Sets the callback used by the FileDialog nodes to get a file icon, when `DISPLAY_THUMBNAILS` mode is used. The callback should take a single String argument (file path), and return a Texture2D. If an invalid texture is returned, the [theme_item file_thumbnail] icon will be used instead. Thumbnails are usually more complex and may take a while to load. To avoid stalling the application, you can use ImageTexture to asynchronously create the thumbnail.
- set_option_default(option: int, default_value_index: int) - Sets the default value index of the OptionButton or CheckBox with index `option`.
- set_option_name(option: int, name: String) - Sets the name of the OptionButton or CheckBox with index `option`.
- set_option_values(option: int, values: PackedStringArray) - Sets the option values of the OptionButton with index `option`.
- set_recent_list(recents: PackedStringArray) - Sets the list of recent directories, which is shared by all FileDialog nodes. Useful to restore the list of recents saved with `set_recent_list`. This method can be called only from the main thread. **Note:** FileDialog will update its internal ItemList of recent directories when its visibility changes. Be sure to call this method earlier if you want your changes to have effect.

**Signals:**
- dir_selected(dir: String) - Emitted when the user selects a directory.
- file_selected(path: String) - Emitted when the user selects a file by double-clicking it or pressing the **OK** button.
- filename_filter_changed(filter: String) - Emitted when the filter for file names changes.
- files_selected(paths: PackedStringArray) - Emitted when the user selects multiple files.

**Enums:**
**FileMode:** FILE_MODE_OPEN_FILE=0, FILE_MODE_OPEN_FILES=1, FILE_MODE_OPEN_DIR=2, FILE_MODE_OPEN_ANY=3, FILE_MODE_SAVE_FILE=4
  - FILE_MODE_OPEN_FILE: The dialog allows selecting one, and only one file.
  - FILE_MODE_OPEN_FILES: The dialog allows selecting multiple files.
  - FILE_MODE_OPEN_DIR: The dialog only allows selecting a directory, disallowing the selection of any file.
  - FILE_MODE_OPEN_ANY: The dialog allows selecting one file or directory.
  - FILE_MODE_SAVE_FILE: The dialog will warn when a file exists.
**Access:** ACCESS_RESOURCES=0, ACCESS_USERDATA=1, ACCESS_FILESYSTEM=2
  - ACCESS_RESOURCES: The dialog only allows accessing files under the Resource path (`res://`).
  - ACCESS_USERDATA: The dialog only allows accessing files under user data path (`user://`).
  - ACCESS_FILESYSTEM: The dialog allows accessing files on the whole file system.
**DisplayMode:** DISPLAY_THUMBNAILS=0, DISPLAY_LIST=1
  - DISPLAY_THUMBNAILS: The dialog displays files as a grid of thumbnails. Use [theme_item thumbnail_size] to adjust their size.
  - DISPLAY_LIST: The dialog displays files as a list of filenames.
**Customization:** CUSTOMIZATION_HIDDEN_FILES=0, CUSTOMIZATION_CREATE_FOLDER=1, CUSTOMIZATION_FILE_FILTER=2, CUSTOMIZATION_FILE_SORT=3, CUSTOMIZATION_FAVORITES=4, CUSTOMIZATION_RECENT=5, CUSTOMIZATION_LAYOUT=6, CUSTOMIZATION_OVERWRITE_WARNING=7, CUSTOMIZATION_DELETE=8
  - CUSTOMIZATION_HIDDEN_FILES: Toggles visibility of the favorite button, and the favorite list on the left side of the dialog. Equivalent to `hidden_files_toggle_enabled`.
  - CUSTOMIZATION_CREATE_FOLDER: If enabled, shows the button for creating new directories (when using `FILE_MODE_OPEN_DIR`, `FILE_MODE_OPEN_ANY`, or `FILE_MODE_SAVE_FILE`). Equivalent to `folder_creation_enabled`.
  - CUSTOMIZATION_FILE_FILTER: If enabled, shows the toggle file filter button. Equivalent to `file_filter_toggle_enabled`.
  - CUSTOMIZATION_FILE_SORT: If enabled, shows the file sorting options button. Equivalent to `file_sort_options_enabled`.
  - CUSTOMIZATION_FAVORITES: If enabled, shows the toggle favorite button and favorite list on the left side of the dialog. Equivalent to `favorites_enabled`.
  - CUSTOMIZATION_RECENT: If enabled, shows the recent directories list on the left side of the dialog. Equivalent to `recent_list_enabled`.
  - CUSTOMIZATION_LAYOUT: If enabled, shows the layout switch buttons (list/thumbnails). Equivalent to `layout_toggle_enabled`.
  - CUSTOMIZATION_OVERWRITE_WARNING: If enabled, the FileDialog will warn the user before overwriting files in save mode. Equivalent to `overwrite_warning_enabled`.
  - CUSTOMIZATION_DELETE: If enabled, the context menu will show the "Delete" option, which allows moving files and folders to trash. Equivalent to `deleting_enabled`.

