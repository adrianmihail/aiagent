import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function

def main():
    print("Hello from aiagent!")

    # load the api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("api key not found")

    # load the gemini client
    client = genai.Client(api_key=api_key)

    # get user prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    contents = args.user_prompt
    
    # store user prompt
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

    def generate_content(client, messages, verbose):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=SYSTEM_PROMPT
            ),
        )

        
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, verbose)
            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            
            response_dict = result.parts[0].function_response.response
            inner_result = response_dict.get("result") if isinstance(response_dict,dict) else response_dict
            
            if verbose:
                print(f"-> {inner_result}")
            
            function_responses.append(result.parts[0])
    
    # loop over response to create conversation
    for _ in range(20):
        generate_content(client,messages,args.verbose)
        


if __name__ == "__main__":
    main()
