# quiz/views.py
import json
import random
from openai import AzureOpenAI
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, UserResponse
from .forms import QuizForm
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                         api_key=os.environ["AZURE_OPENAI_API_KEY"],
                         api_version="2024-02-01")


# def generate_quiz_from_response(response):
#     sentences = response.split('.')
#     questions = []
#
#     for i, sentence in enumerate(sentences):
#         if len(sentence.strip()) > 10:  # simple check to avoid very short sentences
#             question_text = f"What is this sentence about? '{sentence.strip()}'"
#             correct_answer = sentence.split()[0]
#             wrong_answers = [sent.split()[0] for j, sent in enumerate(sentences) if j != i and len(sent.split()) > 0]
#             wrong_answers = random.sample(wrong_answers, min(2, len(wrong_answers)))  # take 2 wrong answers
#
#             question = Question.objects.create(question_text=question_text, correct_answer=correct_answer)
#             Answer.objects.create(question=question, answer_text=correct_answer)
#             for answer in wrong_answers:
#                 Answer.objects.create(question=question, answer_text=answer)
#
#             questions.append(question)
#             if len(questions) >= 3:  # limit to 3 questions for simplicity
#                 break
#
#     return questions


def generate_quiz(request):
    response = request.session.get('chatgpt_response', '')
    if not response:
        return redirect('ask_chatgpt')

    questions = generate_quiz_from_response(response)
    request.session['quiz_questions'] = [q.id for q in questions]

    return redirect('start_quiz')


def start_quiz(request):
    question_ids = request.session.get('quiz_questions', [])
    if not question_ids:
        return redirect('ask_chatgpt')

    question = get_object_or_404(Question, id=question_ids[0])
    form = QuizForm(question=question)

    return render(request, 'quiz/quiz.html', {'form': form, 'question': question})


def submit_quiz(request):
    if request.method == 'POST':
        question_id = request.POST.get('question')
        question = get_object_or_404(Question, id=question_id)
        form = QuizForm(request.POST, question=question)
        if form.is_valid():
            user_response = form.save(user=request.user)
            result = "Correct!" if user_response.is_correct else "Incorrect!"

            question_ids = request.session.get('quiz_questions', [])
            if question_ids:
                question_ids.pop(0)
                request.session['quiz_questions'] = question_ids

            return render(request, 'result.html', {'result': result, 'next': bool(question_ids)})

    return redirect('start_quiz')


def generate_quiz_from_response(response):
    global client
    response = client.chat.completions.create(
        model=os.environ["DEPLOYMENT_NAME"],
        messages=[
            {"role": "system", "content": f"You are the best teacher. {response}"},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Create a quiz with a, b, c answers and one correct answer. Return the answer in json."}
        ]
    )
    print(response.choices[0].message.content)
    # return response.choices[0].message.content

    js = response.choices[0].message.content
    j = json.loads(js)
    q = Question(**j)
    print(j)
    return response.choices[0].message.content
    #
    #
    # sentences = response.split('.')
    # questions = []
    #
    # for i, sentence in enumerate(sentences):
    #     if len(sentence.strip()) > 20:  # simple check to avoid very short sentences
    #         # question_text = f"What is this sentence about? '{sentence.strip()}'"
    #         question_text = f"What is this sentence about? '{sentence}'"
    #         correct_answer = sentence.split()[0]
    #         wrong_answers = [sent.split()[0] for j, sent in enumerate(sentences) if j != i and len(sent.split()) > 0]
    #         wrong_answers = random.sample(wrong_answers, min(2, len(wrong_answers)))  # take 2 wrong answers
    #
    #         question = Question.objects.create(question_text=question_text, correct_answer=correct_answer)
    #         Answer.objects.create(question=question, answer_text=correct_answer)
    #         for answer in wrong_answers:
    #             Answer.objects.create(question=question, answer_text=answer)
    #
    #         questions.append(question)
    #         if len(questions) >= 3:  # limit to 3 questions for simplicity
    #             break

    # return questions





# def ask_chatgpt_question(request):
#     response = request.session.get('chatgpt_response', 'unknown chatgpt response')
#     response = generate_quiz_from_response(response)
#
#     request.session['chatgpt_response'] = response
#
#     return render(request, 'quiz.html', {'response': response, 'chatgpt_response': response })
#     # return redirect('start_quiz')
