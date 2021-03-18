#!/usr/bin/env python3
import requests
def get_submission(domain, course_id, assignment_id, token):
    try:
        response = requests.get(
            url="https://{}/api/v1/courses/{}/assignments/{}/submissions".format(domain, course_id, assignment_id),
            headers={
                "Authorization": "Bearer {}".format(token)
            },
        )
        submission = response.json()
        return submission
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def download_annotated_pdfs(domain, course_id, assignment_id, token):
    subs = get_submission(domain, course_id, assignment_id, token)
    for i in subs:
        uid = i['user_id']
        if 'attachments' in i:
            for file in i['attachments']:
                if file['content-type'] == 'application/pdf':
                    preview_url = file['preview_url']
                    _ = 'https://{}{}'.format(domain, preview_url)
                    r = requests.get(_, headers={"Authorization": "Bearer {}".format(token)}, allow_redirects=False)
                    loc = r.headers['Location'].replace('/view?theme=dark', '') + '/annotated.pdf'
                    post = requests.post(loc)
                    while (True):
                        ready = requests.get(loc + '/is_ready').json()
                        if 'ready' in ready and ready['ready']:
                            break
                    r = requests.get(loc)
                    fname = course_id + '_' + assignment_id + '_' + str(uid) + '_' + file['filename']
                    with open(fname, 'wb') as f:
                        f.write(r.content)
                        print('Downloading ' + fname)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Download annotated PDFs from an assignment to the current directory.')
    parser.add_argument('domain', metavar='domain', type=str,
                        help='The canvas domain. Example: canvas.umn.edu')
    parser.add_argument('course_id', metavar='course_id', type=str,
                        help='The canvas course id. Should be a number.')
    parser.add_argument('assignment_id', metavar='assignment_id', type=str,
                        help='The canvas assignment id. Should be a number.')
    parser.add_argument('--token', metavar='token', type=str,
                        help='Your Canvas Access Token. See https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273 "Get Access Token" section.')
    args = parser.parse_args()
    download_annotated_pdfs(args.domain, args.course_id, args.assignment_id, args.token)