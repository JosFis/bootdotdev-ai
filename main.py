import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

"""
# Gratis gebruikslimieten voor Gemini 2.0 Flash
Volgens de officiële documentatie zijn de limieten voor de gratis tier als volgt:

- Requests per minuut (RPM): 15
- Tokens per minuut (TPM): 1.000.000
- Requests per dag (RPD): 1.500
"""

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# Input
if len(sys.argv) == 1 or len(sys.argv[1]) == 0:
    exit(1)

user_prompt = sys.argv[1]

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose_output = True
else:
    verbose_output = False

# build messages
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Get Response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    )
)
function_call_part = response.function_calls
if function_call_part:  
    #print(function_call_part)
    for fcp in function_call_part:
        print(f"Calling function: {fcp.name}({fcp.args})")
else:
    print(response.text)

if verbose_output:
    x = response.usage_metadata.prompt_token_count
    y = response.usage_metadata.candidates_token_count
    print(f'User prompt: "{user_prompt}"')
    print(f"Prompt tokens: {x}")
    print(f"Response tokens: {y}")
