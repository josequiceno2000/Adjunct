import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

MAX_ITERATIONS = 20


if len(sys.argv) > 1:
    user_prompt = sys.argv[1:]
    messages = [
        types.Content(role="user",parts=[types.Part(text=" ".join(user_prompt))]),
    ]

    verbose = sys.argv[-1] == "--verbose"

    total_prompt_tokens = 0
    total_response_tokens = 0

    if verbose:
        print(f"User prompt: {' '.join(user_prompt)}\n")
        print("--- Starting Agent Execution Loop ---")
    
    i = 0
    response = None
    while i < MAX_ITERATIONS:
        i += 1

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )

            total_prompt_tokens += response.usage_metadata.prompt_token_count
            total_response_tokens += response.usage_metadata.candidates_token_count
        
        except APIError as e:
            print(f"\nFATAL API ERROR: {e.message}")
            break
        except Exception as e:
            print(f"\nFATAL UNEXPECTED ERROR: {e}")
            break
    
        # --- Check for Final Text Response ---
        if response.text is not None and response.text.strip() != "":
            print(f"Response: {response.text}")
            break

        # --- Function Calls ---
        if response.functioncalls:
            for candidate in response.candidates:
                messages.append(candidate.content)

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=verbose)
            
                try:
                    result_data = function_call_result.parts[0].function_response.response
                except(IndexError, AttributeError):
                    raise Exception("FATAL ERROR: call_function did not return a valid types.Content object with a function_response.")
                
                if verbose:
                    print(f"--> {result_data}\n")

                messages.append(function_call_result)

        else:
            print("Response: [Agent stalled - No final text or new function calls generated.]")
            break

        if i >= MAX_ITERATIONS and not response.text:
            print(f"\nWARNING: Max iterations ({MAX_ITERATIONS}) reached without a final response.")
    
        if verbose:
            print(f"\n--- Execution Summary ---")
            print(f"Total Iterations: {i}")
            print(f"Total Prompt Tokens: {total_prompt_tokens}")
            print(f"Total Response Tokens {total_response_tokens}")
            
    else:
        print("Please provide input text as command line arguments.")