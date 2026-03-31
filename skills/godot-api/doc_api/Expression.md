## Expression <- RefCounted

An expression can be made of any arithmetic operation, built-in math function call, method call of a passed instance, or built-in type construction call. An example expression text using the built-in math functions could be `sqrt(pow(3, 2) + pow(4, 2))`. In the following example we use a LineEdit node to write our expression and show the result.

**Methods:**
- execute(inputs: Array = [], base_instance: Object = null, show_error: bool = true, const_calls_only: bool = false) -> Variant - Executes the expression that was previously parsed by `parse` and returns the result. Before you use the returned object, you should check if the method failed by calling `has_execute_failed`. If you defined input variables in `parse`, you can specify their values in the inputs array, in the same order.
- get_error_text() -> String - Returns the error text if `parse` or `execute` has failed.
- has_execute_failed() -> bool - Returns `true` if `execute` has failed.
- parse(expression: String, input_names: PackedStringArray = PackedStringArray()) -> int - Parses the expression and returns an `Error` code. You can optionally specify names of variables that may appear in the expression with `input_names`, so that you can bind them when it gets executed.

