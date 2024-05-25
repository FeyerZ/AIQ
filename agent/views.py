import os
import json
import re
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from openai import AzureOpenAI

load_dotenv()

def insert_newlines_on_capitals(text):
    # Use regular expressions to insert a newline before each capital letter
    return re.sub(r'(?<!^)(?=[A-Z])', '<br>', text)

def get_chatgpt_response(prompt):
    client_text = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )

    try:
        response = client_text.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME"),
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in get_chatgpt_response: {e}")
        raise

def get_dalle_response(prompt):
    client_image = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_DALLE_ENDPOINT"),
        api_key=os.getenv("AZURE_DALLE_API_KEY"),
        api_version="2024-02-01"
    )

    try:
        response = client_image.images.generate(
            model=os.getenv("DEPLOYMENT_NAME_DALLE"),
            prompt=prompt,
            n=1
        )
        image_url = json.loads(response.model_dump_json())['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error in get_dalle_response: {e}")
        raise

def get_keys_from_response(response):
    # Parse the JSON response and return the keys
    try:
        response = json.loads(response)
        keys = response.keys()
    except json.JSONDecodeError:
        print("JSONDecodeError: Unable to parse response")
        keys = []

    return keys

def ask_chatgpt(request):
    major = request.session.get('major', 'unknown major')
    chapter = request.session.get('chapter', 'unknown chapter')
    first_name = request.session.get('first_name', 'unknown first name')
    last_name = request.session.get('last_name', 'unknown last name')
    age_number = request.session.get('age_number', 'unknown age number')
    interest_points = request.session.get('interest_points', 'unknown interest points')
    personality = request.session.get('personality', 'unknown personality')

    if major == 'unknown major' or chapter == 'unknown chapter' or age_number == 'unknown age number' \
            or interest_points == 'unknown interest points' or personality == 'unknown personality':
        return redirect('agent')  # Redirect to the main form if selections are missing

    # Prompt 1
    prompt_1 = (
        f"You are the best teacher. You want to thoroughly write a poem for a {age_number} year old kid. "
        f"His interest points are {interest_points} and he is {personality}. In the poem, include more about {chapter} "
        f"in the field of {major}. Each row must have the same number of syllables, and they must end in a rhyme. "
        f"Don't write the number of syllables, just the poem. When you make the rhyme, write a new line for every rhyme so it is clear where the rhyme is."
    )

    # Prompt 2: Respond in the format json[{ "animal": response1, "fun_fact1": response2, "fun_fact2": response3 } ] 9 animals
    prompt_2 = (
        f"Respond in the json format with the {interest_points} as keys and 2 values as the response to the following question: "
        f"What is the most interesting fact about {interest_points}? Respond only with the json file, don't say anything else and have 9 entries"
    )

    try:
        response_1 = get_chatgpt_response(prompt_1)
        response_2 = get_chatgpt_response(prompt_2)
    except Exception as e:
        print(f"Error in getting responses from GPT: {e}")
        return render(request, 'error.html', {'error': 'Unable to get responses from GPT'})

    response_1 = insert_newlines_on_capitals(response_1)
    response_2 = response_2[8:-3]  # Adjust slicing as needed

    response_2_keys = get_keys_from_response(response_2)
    response_3_urls = []
    for key in response_2_keys:
        prompt_3 = (
            f"You are the best drawer for children's books. Generate a photo for a {age_number} year old kid, a photo with {key} "
            f"in the portrait orientation, realistic, simple"
        )
        try:
            response_3 = get_dalle_response(prompt_3)
            print(response_3)
            response_3_urls.append(response_3)
        except Exception as e:
            print(f"Error in getting response from DALL-E: {e}")
            # Handle the error as needed, for now, appending None as placeholder
            response_3_urls.append(None)

    # Debugging response_2
    # print(response_2)
    # Parse response_2 JSON with error handling
    try:
        response_2 = json.loads(response_2)
    except json.JSONDecodeError:
        print("JSONDecodeError: Unable to parse response_2")
        response_2 = {}

    return render(request, 'response.html', {
        'response_1': response_1,
        'response_2': response_2,
        'response_3': response_3_urls,
        'major': major,
        'chapter': chapter,
        'first_name': first_name,
        'last_name': last_name,
        'age_number': age_number,
        'interest_points': interest_points,
        'personality': personality
    })
