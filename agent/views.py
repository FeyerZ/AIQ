from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
import os
import openai
from openai import AzureOpenAI
# from django.conf import settings
from dotenv import load_dotenv
import re
import json

load_dotenv()

def insert_newlines_on_capitals(text):
    # Use regular expressions to insert a newline before each capital letter
    return re.sub(r'(?<!^)(?=[A-Z])', '<br>', text)

def get_chatgpt_response(prompt):
    # client = OpenAI()
    client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                         api_key=os.environ["AZURE_OPENAI_API_KEY"],
                         api_version="2024-02-01")

    response = client.chat.completions.create(
        model=os.environ["DEPLOYMENT_NAME"],
        messages=[
            # {"role": "system", "content": "You are the best teacher. You want to explain thoroughly as for a 5 years "
            #                               "old kid. Show result as topics that can be written on playing cards"},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},


            # {"role": "system",
            #  "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
            # {"role": "system", "name": "example_user", "content": "New synergies will help drive top-line growth."},
            # {"role": "system", "name": "example_assistant",
            #  "content": "Things working well together will increase revenue."},
            # {"role": "system", "name": "example_user",
            #  "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
            # {"role": "system", "name": "example_assistant",
            #  "content": "Let's talk later when we're less busy about how to do better."},
            # {"role": "user",
            #  "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},

            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return response.choices[0].message.content


def ask_chatgpt(request):
    major = request.session.get('major', 'unknown major')
    chapter = request.session.get('chapter', 'unknown chapter')
    first_name = request.session.get('first_name', 'unknown first name')
    last_name = request.session.get('last_name', 'unknown last name')
    age_number = request.session.get('age_number', 'unknown age number')
    interest_points = request.session.get('interest_points', 'unknown interest points')
    personality = request.session.get('personality', 'unknown personality')

    if major == 'unknown major' or chapter == 'unknown chapter' or age_number == 'unknown age number'\
            or interest_points == 'unknown interest points' or personality == 'unknown personality':
        return redirect('agent')  # Redirect to the main form if selections are missing

    #promt 1
    prompt_1 = (
        f"You are the best teacher. You want thoroughly write a poem for a {age_number} years old kid. His interest points are {interest_points} and he is {personality}. In the poem, include more about {chapter} in the field of {major}. Each row must have the same number of syllabus, and they must end in a rhyme, don't write the number of syllables, just the poem when you make the rhyme, write a new line for every rhyme so it is clear where the rhyme is.")

    # Prompt 2: Respond in the format json[{ "animal": response1, "fun_fact1": response2, "fun_fact2": response3 } ] 9 animals
    prompt_2 = (
        f"Respond in the json format with the {interest_points} as keys and 2 values as the response to the following question: What is the most interesting fact about {interest_points}? Respond only with the json file, don't say anything else and have 9 entries")
    response_1 = get_chatgpt_response(prompt_1)
    response_2 = get_chatgpt_response(prompt_2)

    name_of_object = interest_points.split(';')[0]
    prompt_3 = (
        f"You are the best drawer for children's books, draw for for a {age_number} years old kid, a photo with {name_of_object} in the portrait orientation, realistic, simple")
    prompt_3 = (f"give me 9 urls for pictures, and don't say anything else, don't count them, just send the urls")
    response_3 = get_chatgpt_response(prompt_3)
    response_1 = insert_newlines_on_capitals(response_1)
    #cut the first 7 characters from the response_2
    response_2 = response_2[8:]
    #cut the last 3 characters from the response_2
    response_2 = response_2[:-3]

    # Debugging response_2
    print(response_2)
    # Parse response_2 JSON with error handling
    try:
        response_2 = json.loads(response_2)
    except json.JSONDecodeError:
        print("JSONDecodeError: Unable to parse response_2")
        response_2 = []

    return render(request, 'response.html', {
        'response_1': response_1,
        'response_2': response_2,
        'response_3': response_3,
        'major': major,
        'chapter': chapter,
        'first_name': first_name,
        'last_name': last_name,
        'age_number': age_number,
        'interest_points': interest_points,
        'personality': personality
    })
