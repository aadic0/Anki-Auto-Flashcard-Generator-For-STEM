import openai
import json

def call_llm(text):
    with open("config.json") as f:
        api_key = json.load(f)["openai_api_key"]
    
    openai.api_key = api_key
    prompt = f"Convert the following text into Anki flashcards. Use 'Front::Back' format, one per line.\n\n{text[:4000]}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
