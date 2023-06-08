import openai
import os
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
    )
    return response.choices[0].message["content"]

def grammar_check(essay):
    prompt = f"""
    please check if the text delimited by triple backticks \
    has any grammatical errors. If so, please provide the list \
    of errors, along with the full sentence, the type of error, \
    and the corrections, in a JSON format. Use the following \
    format for the JSON: \
    {{
        "errors": [
            {{
                "id": "Error number count. Integer",
                "sentence": "The sentence with the error.",
                "type": "Error type like Capitalization, Punctuation, Spelling, Word Order, etc.",
                "correction": "The list of corrections.",
                "translation": "Translate hint to Spanish.",
                "hint": "Hint of the answer"
            }},
            {{
                "id": "Error number count. Integer",
                "sentence": "The sentence with the error.",
                "type": "Error type like Capitalization, Punctuation, Spelling, Word Order, etc.",
                "correction": "The list of corrections.",
                "translation": "Translate hint to Spanish.",
                "hint": "Hint of the answer"
            }}
        ]
    }}
    ```{essay}```
    """

    grammar_json = get_completion(prompt)

    grammar_check = f"""
    Please check if the text delimited by triple backticks \
    has a valid JSON structure. It must contain the keys: \
    id, sentence, type, correction, translation, and hint. \
    If it is a valid JSON with all the required keys, \
    simply write 'True'. If it does not contain a valid JSON \
    or it does not contain all the required keys, \
    write 'False'.

    ```{grammar_json}```
    """

    grammar_json_check = get_completion(grammar_check)
    if grammar_json_check == "True":
        if type(grammar_json) is not dict:
            grammar_json = eval(grammar_json)
        return grammar_json
    else:
        return {"error": "Invalid JSON"}

st.set_page_config(page_title="AI:GrammarCheck", page_icon=":strawberry:")
st.title("Grammar Checker App")
essay = st.text_area("Write your text here", height=300)

if 'error_dict' not in st.session_state:
    st.session_state.error_dict = None
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if st.button('Grammar Check'):
    st.session_state.error_dict = grammar_check(essay)
    st.session_state.current_index = 0

if st.session_state.error_dict is not None:
    if 'errors' in st.session_state.error_dict:
        errors = st.session_state.error_dict['errors']

        st.text(f'Error: {st.session_state.current_index + 1}/{len(errors)}')
        st.text(f'ID: {errors[st.session_state.current_index]["id"]}')
        st.text(f'Type: {errors[st.session_state.current_index]["type"]}')
        st.text(f'Sentence: {errors[st.session_state.current_index]["sentence"]}')

        corrected_text = st.text_input('Correct the sentence here')
        
        if st.button('Hint'):
            st.text(errors[st.session_state.current_index]["hint"])

        if st.button('Translation'):
            st.text(errors[st.session_state.current_index]["translation"])

        if st.button('Answer'):
            st.text(errors[st.session_state.current_index]["correction"])
        

        if st.button('Next'):
            if st.session_state.current_index < len(errors) - 1:
                st.session_state.current_index += 1

        if st.button('Back'):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
