import openai
import os
import json
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
    
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [ {"role": "system", "content": 'You:'},
        {"role": "user", "content": "```"},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": "```"},
        {"role": "user", "content": '"""\n'},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": '\n"""'},
        {"role": "user", "content": "<"},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": ">"},
        {"role": "user", "content": ","},
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": ":"},
        {"role": "assistant", "content": prompt}] #prompt real
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

essay = f"""
This is an englush essay with a lot of spelling mistakes. \
It is also a very long essay. \
It is about a topc that is very interesting. \
Is about the history of the artificial ntelligence. \
And about How artificial intelligence is going to change the world. \
However, it is not very well written. \
It is not very structured and organized. \
It is, not, very well formatted. \
It is is not well punctuated. \
It is not cApitalized very well . \
It is not well very written. \

"""
#prompt = f"""
#Please do a grammar check on my essay. 
#<{essay}>
#"""
#response = get_completion(prompt)
#print(response)

    #Convert to structured format
    
grammar_json=get_completion(f"""
please check if the text delimited by triple backticks \
has any grammatical erros. If so, please provide the list\
of errors, along with the full sentence, the type of error \
and the corrections, in a json format. Use the following\
format for the JSON: \
"errors": [
"id": "Error number count. Integer", \
"sentence": "The sentence with the error.",\
"type": "Error type like Capitalization, Punctuation, Spelling, Word Order, etc.", \
"correction": "The list of correction."]\
    
´´´{essay}´´´
""")

#print(grammar_json)

#check if it works

json_check= get_completion(f"""
Please check if the text delimited by triple backticks\
has a valid json structure. It must contain the keys: \
id, sentence, type and correction.\
If it is valid JSON with all the keys required,\
simply write 'True'. If it does not contain a valid json\
or it does not contain all the required keys,\
write 'FALSE'.

```{grammar_json}```
"""
)

#print(json_check)

if type(grammar_json) is not dict: 
    grammar_json= json.loads(grammar_json)
    print(grammar_json["errors"][0])

