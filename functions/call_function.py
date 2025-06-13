from function_dictionary import func_dict
from google.genai import types
working_dictionary = "./calculator"

def call_function(function_call_part, verbose=False):

    func_name = function_call_part.name
    kwargs = function_call_part.args

    if verbose:
        print(f"Calling function: {func_name}({kwargs})")
    print(f" - Calling function: {func_name}")

    res = func_dict[func_name](
                working_dictionary,
                **kwargs
    )
    
    if func_dict.get(func_name) is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": res},
            )
        ],
    )