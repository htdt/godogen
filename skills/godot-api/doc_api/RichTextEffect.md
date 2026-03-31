## RichTextEffect <- Resource

A custom effect for a RichTextLabel, which can be loaded in the RichTextLabel inspector or using `RichTextLabel.install_effect`. **Note:** For a RichTextEffect to be usable, a BBCode tag must be defined as a member variable called `bbcode` in the script. **Note:** As soon as a RichTextLabel contains at least one RichTextEffect, it will continuously process the effect unless the project is paused. This may impact battery life negatively.

**Methods:**
- _process_custom_fx(char_fx: CharFXTransform) -> bool - Override this method to modify properties in `char_fx`. The method must return `true` if the character could be transformed successfully. If the method returns `false`, it will skip transformation to avoid displaying broken text.

