import os
import json
import re
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from openai import AzureOpenAI

load_dotenv()


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
        f"Respond in the json format with the {interest_points} as keys and 2 values as the response to the following question: You know everything. What are the 2 most interesting facts about {interest_points}? Respond only with the json file, don't say anything else and have 9 entries. "
    )

    try:
        response_1 = get_chatgpt_response(prompt_1)
        response_2 = get_chatgpt_response(prompt_2)
    except Exception as e:
        print(f"Error in getting responses from GPT: {e}")
        return render(request, 'error.html', {'error': 'Unable to get responses from GPT'})

    response_2 = response_2[8:-3]  # Adjust slicing as needed
    #print(response_1)
    response_2_keys = get_keys_from_response(response_2)
    response_3_urls = []
    for key in response_2_keys:
        prompt_3 = (
            f"You are the best drawer for children's books. Generate a photo with {key} "
            f"in the portrait orientation, realistic, simple"
        )
        try:
            response_3 = get_dalle_response(prompt_3)
            response_3_urls.append(response_3)
            print("photo generated successfully")
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
    #print(response_3_urls)
    #this is the response_3_urls: ['https://dalleproduse.blob.core.windows.net/private/images/65d971e1-a19c-4872-9747-13568a1fc6cb/generated_00.png?se=2024-05-27T07%3A00%3A29Z&sig=tYUHnLQVpAU3jd1U65kwNQn%2FiI8S4ybPLVJw%2FLJ0dTc%3D&ske=2024-05-29T12%3A38%3A41Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-22T12%3A38%3A41Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/3d95377c-c7de-4e2b-9a70-2a9c107b3508/generated_00.png?se=2024-05-27T07%3A00%3A42Z&sig=0pJPJaTSZstxab3LK6ikB8tW6g4hBWFChdQzmS%2Bx0ZQ%3D&ske=2024-06-01T13%3A36%3A00Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-25T13%3A36%3A00Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/c97ee8b1-b719-4386-b272-f8700bc9fb63/generated_00.png?se=2024-05-27T07%3A00%3A54Z&sig=qVr88rF1CteyQdDWexNqaL14VGdb7o2NsGswPc6YXLc%3D&ske=2024-05-29T12%3A38%3A41Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-22T12%3A38%3A41Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/259deac9-a667-4ebe-9aca-69937b537350/generated_00.png?se=2024-05-27T07%3A01%3A31Z&sig=OffBFqddnez5IL696OJQnvUNCgpfPyyk7gCLJY0tres%3D&ske=2024-06-01T13%3A36%3A00Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-25T13%3A36%3A00Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/7113893b-da37-42c1-9d8b-89ccbeb73cab/generated_00.png?se=2024-05-27T07%3A01%3A44Z&sig=wvETB9K1MkElBmqH%2FueghfCv9O8OET4d1Q30OJv49Yw%3D&ske=2024-06-01T13%3A36%3A00Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-25T13%3A36%3A00Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/d7785d17-d22f-4e04-9c42-cd05723ea28f/generated_00.png?se=2024-05-27T07%3A01%3A58Z&sig=41hPnWEYVwAS2PHkBk5OS5FIZj41m4rgUgAj2Ci4xz4%3D&ske=2024-05-29T12%3A38%3A41Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-22T12%3A38%3A41Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/d89aed10-5f85-4efd-9956-c85fadf2b923/generated_00.png?se=2024-05-27T07%3A02%3A33Z&sig=Xxql4cGcsJ0eOKI2Oh6RYML3%2BrB1%2FrzG3Dj4bUhieXk%3D&ske=2024-05-29T08%3A06%3A31Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-22T08%3A06%3A31Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/c684ddeb-a535-4ba5-9ded-16997247811b/generated_00.png?se=2024-05-27T07%3A02%3A43Z&sig=wVXKLmnTLohs70EuZnT%2FECbu22cEss6CJNUEGXOoRiM%3D&ske=2024-05-29T12%3A38%3A41Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-22T12%3A38%3A41Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', 'https://dalleproduse.blob.core.windows.net/private/images/60bc9c77-167b-43f0-bc1b-32f60d38e07e/generated_00.png?se=2024-05-27T07%3A02%3A58Z&sig=Vr5K4uGCkSbn4nA69xVMdMuAbshyDEH74vISag6m6Mc%3D&ske=2024-06-01T13%3A36%3A00Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-05-25T13%3A36%3A00Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02']
    #make it so response_1 transfers each row to a list by the separator \n
    print(response_1)
    response_1_list = response_1.split('\n')
    mid_index = len(response_1_list)//2
    first_half = response_1_list[:mid_index]
    second_half = response_1_list[mid_index:]
    print(first_half)
    print(second_half)
    return render(request, 'response.html', {
        'response_1': first_half,
        'response_1_2': second_half,
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
