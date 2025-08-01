# https://groq.com/ 사용

import streamlit as st
import pandas as pd
import numpy as np

import os
from openai import OpenAI
from dotenv import load_dotenv # python-dotenv 라는 패키지로 .env 안에 잇는 값을 읽는다.

from groq import Groq

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)

@st.cache_data
def load_data():
    df = pd.read_csv("data_6_store_lat_lon.csv")
    return df

df = load_data()

def table_definition_prompt(df, address):
    
    prompt = '''Given the following pandas dataframe definition,
            write closest store's name and distance between {} and store
            \n### pandas dataframe, with its properties:
            
            #
            # df의 컬럼명({})
            #
            '''.format(address, ",".join(str(x) for x in df.columns))
    
    return prompt

nlp_text = st.text_input('주소를 입력하세요: ')
accept = st.button('요청')

if accept :
    full_prompt = str(table_definition_prompt(df,  str(nlp_text)))
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that receives a user-inputted address and searches for the nearest convenience store based on a preloaded DataFrame containing store names and their latitude and longitude coordinates. You must: \
                1. Geocode the input address to obtain its latitude and longitude. \
                2. Calculate the distances between the input location and each store in the DataFrame using the Haversine formula or similar geographic distance calculation.\
                3. Identify the closest convenience store.\
                4. Return the name of the nearest convenience store and the distance to it from the input address in kilometers (rounded to two decimal places).\
                If the address is invalid or cannot be geocoded, politely ask the user to enter a valid address. Do not hallucinate any data.\
                    not any explanation or ``` for copy. \
                You should not any expression. store's name : distances between store and input address format\
                "
        },
        {
            "role": "user",
            # "content": f"address to answer = {str(nlp_text)}"
            "content": f"A query to answer: {full_prompt}"
        }
        ],
        temperature=1,
        max_completion_tokens=200,
        top_p=1,
        stream=True,
        stop=None,
    )

    full_response = ""
    print(completion)
    for chunk in completion:
        content_piece  = chunk.choices[0].delta.content or ""
        full_response += content_piece

    code_str = full_response.strip()
    st.code(code_str)
    # st.write(eval(code_str))