from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
import os
import openai
from openai import AzureOpenAI
# from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

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

    prompt = (f"You are the best teacher. You want to explain thoroughly for a {age_number} years old kid. His "
              f"interest points are {interest_points} and he is {personality}. Tell me more about chapter {chapter} in "
              f"the field of {major}. Show result as topics that can be written on playing cards. Give some more "
              f"details about each of them")
    response = get_chatgpt_response(prompt)

    return render(request, 'response.html', {'response': response,'major': major, 'chapter': chapter,
                                             'first_name': first_name, 'last_name': last_name, 'age_number': age_number,
                                             'interest_points': interest_points, 'personality': personality})
