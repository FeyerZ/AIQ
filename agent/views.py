import os
import json
import re
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from openai import AzureOpenAI
import io
import sys
import logging
load_dotenv()
logger = logging.getLogger('debug_logger')
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
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    domain = request.session.get('domain', 'unknown domain')
    subdomain = request.session.get('subdomain', 'unknown subdomain')
    first_name = request.session.get('first_name', 'unknown first name')
    last_name = request.session.get('last_name', 'unknown last name')
    age_number = request.session.get('age_number', 'unknown age number')
    interest_points = request.session.get('interest_points', 'unknown interest points')
    personality = request.session.get('personality', 'unknown personality')

    if domain == 'unknown domain' or subdomain == 'unknown subdomain' or age_number == 'unknown age number' \
            or interest_points == 'unknown interest points' or personality == 'unknown personality':
        return redirect('agent')  # Redirect to the main form if selections are missing

    # Prompt 1
    if domain != 'languages':
        prompt_1= (
        f"You are the best teacher. You want to thoroughly write a poem for a {age_number} year old kid. "
        f"His interest points are {interest_points} and he is {personality}. In the poem, include more about {subdomain} "
        f"in the field of {domain}. Each row must have the same number of syllables, and they must end in a rhyme. "
        f"Don't write the number of syllables, just the poem. When you make the rhyme, write a new line for every rhyme so it is clear where the rhyme is."
    )
    else:
        prompt_1 = (
            f"You are the best teacher. You want to thoroughly write a poem for a {age_number} year old kid. "
            f"His interest points are {interest_points} and he is {personality}. In the poem, include words in {subdomain} language using that language's letters, and don't write it's pronunciation words that an {age_number} year old would learn. "
            f". Each row must have the same number of syllables, and they must end in a rhyme. "
            f"Don't write the number of syllables, just the poem. When you make the rhyme, write a new line for every rhyme so it is clear where the rhyme is."
            f"At the end of the response, write a new line and write 'HHHHH' so it is clear where the poem ends."
            f"then write the words in {subdomain} each on a new line."
        )


    # Prompt 2: Respond in the format json[{ "animal": response1, "fun_fact1": response2, "fun_fact2": response3 } ] 9 animals
    prompt_2 = (
        f"Respond in the json format with the {interest_points} as keys and 2 values as the response to the following question: You know everything. What are the 2 most interesting facts about {interest_points}? Respond only with the json file, don't say anything else and have 9 entries. "
    )

    try:
        response_1 = get_chatgpt_response(prompt_1)
        response_2 = get_chatgpt_response(prompt_2)
    except Exception as e:
        print(f"Error in getting responses from GPT: {e}")
        return render(request, '', {'error': 'Unable to get responses from GPT'})
    response_1, word_list = response_1.split('HHHHH')
    #make a list of strings from word_list
    #delete the elements that are empty strings
    word_list = word_list.split('\n')
    word_list = [word for word in word_list if word.strip()]
    final_word_list = []
    #add all words from word_list to a file
    with open('word_list.txt', 'w', encoding='utf-8') as a:
        for word in word_list:
            a.write(word + '\n')
    for word in word_list:
        prompt_for_translation = ("translate " + word + " to English, don't say anything else, just the word and the translated word and it's pronunciation in " + subdomain + " language separated by a =, each word on a new line in this format: word (pronunciation) = translated word ")
        try:
            response_for_translation = get_chatgpt_response(prompt_for_translation)
            with open('open_ai_response.txt', 'w', encoding='utf-8') as g:
                g.write(response_for_translation)
            response_for_translation = response_for_translation.split('\n')
            original_word_and_pronunciation = response_for_translation[0].split('=')[0]
            translated_word = response_for_translation[0].split('=')[1]
            original_word_and_pronunciation = original_word_and_pronunciation.strip()
            translated_word = translated_word.strip()
            final_word_list.append(original_word_and_pronunciation)
            final_word_list.append(translated_word)
            with open('final_word_list.txt', 'w', encoding='utf-8') as b:
                for word in final_word_list:
                    b.write(word + '\n')
        except Exception as e:
            print(f"Error in getting responses from GPT: {e}")
            return render(request, '', {'error': 'Unable to get responses from GPT'})

    response_2 = response_2[8:-3]  # Adjust slicing as needed
    response_2_keys = get_keys_from_response(response_2)
    response_3_urls = []
    for key in response_2_keys:
        prompt_3 = (
            f"You are the best drawer for children's books. Generate a photo with {key} "
            f"in the portrait orientation, realistic, simple"
        )
        try:
            #response_3 = get_dalle_response(prompt_3)
            #response_3_urls.append(response_3)
            print("photo generated successfully")
        except Exception as e:
            #print(f"Error in getting response from DALL-E: {e}")
            # Handle the error as needed, for now, appending None as placeholder
            response_3_urls.append(None)

    try:
        response_2 = json.loads(response_2)
    except json.JSONDecodeError:
        print("JSONDecodeError: Unable to parse response_2")
        response_2 = {}
    response_1_list = response_1.split('\n')
    mid_index = len(response_1_list)//2
    first_half = response_1_list[:mid_index]
    second_half = response_1_list[mid_index:]
    paired_words = [(final_word_list[i], final_word_list[i + 1]) for i in range(0, len(final_word_list), 2)]
    with open('paired_words.txt', 'w', encoding='utf-8') as f:
        for item in paired_words:
            f.write(item[0] + ' = ' + item[1] + '\n')
    return render(request, 'response.html', {
        'paired_words': paired_words,
        'response_1': first_half,
        'response_1_2': second_half,
        'response_2': response_2,
        'response_3': response_3_urls,
        'domain': domain,
        'subdomain': subdomain,
        'first_name': first_name,
        'last_name': last_name,
        'age_number': age_number,
        'interest_points': interest_points,
        'personality': personality
    })
