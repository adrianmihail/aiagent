import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

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
    args = parser.parse_args()
    contents = args.user_prompt
    
    # store user prompt
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

    # print user prompt
    print(f"User prompt: {contents}")


    # get response from client
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model=model,contents=messages)


    # print number of tokens consumed by the interaction
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if prompt_tokens != None and response_tokens != None:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    elif prompt_tokens == None and response_tokens == None:
        raise RuntimeError("api request failed")

    # print response from client
    
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
