import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

contents = sys.argv[1:] if len(sys.argv) > 1 else print("Please provide input text as command line arguments.")

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents=contents)
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

print(response.text)
print(f"Prompt Tokens: {prompt_tokens}")
print(f"Response Tokens: {response_tokens}")
