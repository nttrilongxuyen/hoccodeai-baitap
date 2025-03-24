from together import Together
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv(".../.env") 

client = Together(
    api_key=os.getenv("together_key")
)
context = []

modeld="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
input_messages=[]

while(True):
    print("\n\n-----------------USER")
    user_input = input()

    user_input={
            "role": "user", 
            "content": user_input
        }
    input_messages.append(user_input)

    stream = client.chat.completions.create(
        model=modeld,
        messages=input_messages,
        stream=True
    )

    model_stream=""
    print("===================LLM")
    for chunk in stream:
        model_stream = f"{"" if model_stream == "" else model_stream}{chunk.choices[0].delta.content} "
        print(chunk.choices[0].delta.content or "", end="")

    input_messages.append({
        "role": "assistant",
        "content": model_stream
    })
    