# quiz/views.py
import json
import random
from openai import AzureOpenAI
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Question, UserResponse
# from .forms import QuizForm
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                         api_key=os.environ["AZURE_OPENAI_API_KEY"],
                         api_version="2024-02-01")


def generate_quiz(request):
    response = request.session.get('chatgpt_response', '')
    if not response:
        return redirect('ask_chatgpt')

    questions = generate_quiz_from_response(response)
    request.session['quiz_questions']['question'] = [q.question_text for q in questions]
    request.session['quiz_questions']['options'] = [q.questio_options for q in questions]
    request.session['quiz_questions']['correct_answer'] = [q.correct_answer for q in questions]

    return redirect('start_quiz')


# def start_quiz(request):
#     question_ids = request.session.get('quiz_questions', [])
#     if not question_ids:
#         return redirect('ask_chatgpt')
#
#     # question = get_object_or_404(Question, id=question_ids[0])
#     # form = QuizForm(question=question)
#     print(question_ids)
#     return render(request, 'quiz.html',
#                   # {
#                   #     'form': form,
#                   #     'question': question
#                   # }
#                   )


def generate_quiz_from_response(response):
    global client
    response = client.chat.completions.create(
        model=os.environ["DEPLOYMENT_NAME"],
        messages=[
            {"role": "system", "content": f"Content: {response}"},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Create a quiz from Content with multiple questions and each should have a, b, c answers and one correct answer. Return the answer in json."}
        ]
    )
    # print(response.choices[0].message.content)
    # return response.choices[0].message.content

    js = response.choices[0].message.content
    j = json.loads(js)
    q = Question(**j)
    print(q)

    for i, sentence in enumerate(js):
        question_text = f"{sentence}"



    # return response.choices[0].message.content
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

from django.shortcuts import render, redirect
from .models import Question, Answer

def quiz_view(request):
    questions = Question.objects.all()
    return render(request, 'quiz.html', {'questions': questions})

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        total_questions = Question.objects.count()

        for question in Question.objects.all():
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

        return render(request, 'result.html', {
            'score': score,
            'total_questions': total_questions,
        })

    return redirect('quiz')
