import openai
import os
import json
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": 'You:'},
        {"role": "user", "content": "```"},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": "<"},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": ">"},
        {"role": "assistant", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=2000
    )
    return response.choices[0].message["content"]

essay_text = st.text_area("Enter your essay")

if st.button("Check Grammar"):
    prompt = f"""
    Please check if the text delimited by triple backticks \
    has any grammatical errors. If so, please provide the list \
    of errors, along with the full sentence, the type of error \
    and the corrections, in a JSON format. Use the following \
    format for the JSON:

    {{
    "errors": [
        {{
            "id": "Error number count. Integer",
            "sentence": "The sentence with the error.",
            "type": "Error type like Capitalization, Punctuation, Spelling, Word Order, etc",
            "correction": "The list of corrections."
        }}
        ]
    }}
    ```{essay_text}```
    """


grammar_json = get_completion(prompt)

try:
    grammar_json = json.loads(grammar_json)
except json.JSONDecodeError:
    st.write("Invalid JSON format. Please check the response from the model.")

if "errors" in grammar_json:
    st.write("Error ID:", grammar_json["errors"][0]['id'])
    st.write("Sentence:", grammar_json["errors"][0]['sentence'])
    st.write("Type:", grammar_json["errors"][0]['type'])
else:
    st.write("No grammatical errors found.")
