import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"

output = []

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
        )
        )
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if sys.argv[-1] == "--verbose":
        print(f"User prompt: {' '.join(user_prompt)}\n")

    print(f"Response: {response.text}")

    if sys.argv[-1] == "--verbose":
        print(f"\nPrompt Tokens: {prompt_tokens}")
        print(f"Response Tokens: {response_tokens}")
else: 
    print("Please provide input text as command line arguments.")

