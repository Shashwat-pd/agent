import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import available_functions
from config import system_prompt

from functions.call_function import call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
        

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print(response.text)
            return
        
        for condidate in response.candidates:
            messages.append(condidate.content)

        for function_call_part in response.function_calls:
            res = call_function(function_call_part)


            try:
                response_content = res.parts[0].function_response.response
            except (AttributeError, IndexError):
                raise RuntimeError("Fatal Error: Missing function response.")
            messages.append(res)

            
            if verbose:
                print(f"-> {res.parts[0].function_response.response}")
            
            
            #print(f"{res.parts[0].function_response.response['result']}")
    print(response.text)

    return 





if __name__ == "__main__":
    main()
