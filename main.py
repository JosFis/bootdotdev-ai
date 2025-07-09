import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

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
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)
print(response.text)

if verbose_output:
    x = response.usage_metadata.prompt_token_count
    y = response.usage_metadata.candidates_token_count
    print(f'User prompt: "{user_prompt}"')
    print(f"Prompt tokens: {x}")
    print(f"Response tokens: {y}")
