from canvasapi import Canvas
from bs4 import BeautifulSoup
import pandas as pd

def download_quiz_questions(domain, course_id, quiz_id, token):
    canvas = Canvas('https://' + domain, token)
    course = canvas.get_course(course_id)
    quiz = course.get_quiz(quiz_id)
    questions = list(quiz.get_questions())
    questions_ = []
    for i in questions:
        q = {
            "id": i.id,
            "question": get_text(i.question_text),
            "answers": ""
        }
        for j in i.answers:
            q['answers'] = q['answers'] + str(j['weight']) + ":" + get_text(j['text']) + "\n"
        questions_.append(q)
    fname = str(course_id) + '_' + str(quiz_id) + '.csv'
    pd.DataFrame(questions_).to_csv(fname, index=False)
    print("CSV file written to", fname)

def get_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.text

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Export a CSV file from a quiz with questions and answers.')
    parser.add_argument('domain', metavar='domain', type=str,
                        help='The canvas domain. Example: canvas.umn.edu')
    parser.add_argument('course_id', metavar='course_id', type=int,
                        help='The canvas course id. Should be a number.')
    parser.add_argument('quiz_id', metavar='assignment_id', type=int,
                        help='The canvas quiz id. Should be a number.')
    parser.add_argument('--token', metavar='token', type=str,
                        help='Your Canvas Access Token. See https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273 "Get Access Token" section.')
    args = parser.parse_args()
    download_quiz_questions(args.domain, args.course_id, args.quiz_id, args.token)