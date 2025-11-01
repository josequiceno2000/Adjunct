import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
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


if len(sys.argv) > 1:
    user_prompt = sys.argv[1:]
    messages = [
        types.Content(role="user",parts=[types.Part(text=" ".join(user_prompt))]),
    ]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
        )
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    verbose = sys.argv[-1] == "--verbose"

    if verbose: 
        print(f"User prompt: {' '.join(user_prompt)}\n")

    if response.text is not None and response.text.strip() != "":
        print(f"Response: {response.text}")
    elif not response.function_calls:
        print("Response: [No conversational response or function call was generated.]")

    if response.function_calls:
        function_call_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=verbose)
            
            try:
                result_data = function_call_result.parts[0].function_response.response
            except(IndexError, AttributeError):
                raise Exception("FATAL ERROR: call_function did not return a valid types.Content with a function_response.")
            
            if verbose:
                print(f"--> {result_data}\n")
            
            function_call_results.append(function_call_result)

    if verbose:
        print(f"\nPrompt Tokens: {prompt_tokens}")
        print(f"Response Tokens: {response_tokens}")
    
else: 
    print("Please provide input text as command line arguments.")

