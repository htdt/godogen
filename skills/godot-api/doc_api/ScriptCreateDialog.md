## ScriptCreateDialog <- ConfirmationDialog

The ScriptCreateDialog creates script files according to a given template for a given scripting language. The standard use is to configure its fields prior to calling one of the `Window.popup` methods.

**Props:**
- dialog_hide_on_ok: bool = false
- ok_button_text: String = "Create"
- title: String = "Attach Node Script"


**Methods:**
- config(inherits: String, path: String, built_in_enabled: bool = true, load_enabled: bool = true) - Prefills required fields to configure the ScriptCreateDialog for use.

**Signals:**
- script_created(script: Script) - Emitted when the user clicks the OK button.

