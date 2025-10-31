import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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
    
    if sys.argv[-1] == "--verbose":
        print(f"User prompt: {' '.join(user_prompt)}\n")

    print(f"Response: {response.text}")

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"\nFunction Call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
    

    if sys.argv[-1] == "--verbose":
        print(f"\nPrompt Tokens: {prompt_tokens}")
        print(f"Response Tokens: {response_tokens}")
else: 
    print("Please provide input text as command line arguments.")

