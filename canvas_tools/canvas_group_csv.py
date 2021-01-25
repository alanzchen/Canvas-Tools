#!/usr/bin/env python3
import requests

def get_groups(domain, course_id, token):
    try:
        response = requests.get(
            url="https://{}/api/v1/courses/{}/groups".format(domain, course_id),
            headers={
                "Authorization": "Bearer {}".format(token)
            },
        )
        grps = response.json()
        return {i['id']: i['name'] for i in grps}
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def get_group_people(domain, grp, token):
    try:
        response = requests.get(
            url="https://{}/api/v1/groups/{}/users".format(domain, grp),
            headers={
                "Authorization": "Bearer {}".format(token)
                },
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def write_csv(domain, course_id, token, filename=None):
    if not filename:
        filename = '{}.csv'.format(course_id)
    grps = get_groups(domain, course_id, token)
    cnt = 0
    with open(filename, 'w') as f:
        f.write('Pre-assign Room Name,Email Address\n')
        for i, name in grps.items():
            grp = get_group_people(domain, i, token)
            for j in grp:
                f.write(name + ',' + j['login_id'] + '\n')
                cnt += 1
        print('Successfully exported {} groups with {} students in total. CSV written to {}'.format(str(len(grps)), str(cnt), filename))

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Export Canvas Group Assignment to CSV.')
    parser.add_argument('domain', metavar='domain', type=str,
                        help='The canvas domain. Example: canvas.umn.edu')
    parser.add_argument('course_id', metavar='course_id', type=str,
                        help='The canvas course id. Should be a number.')
    parser.add_argument('--token', metavar='token', type=str,
                        help='Your Canvas Access Token. See https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273 "Get Access Token" section.')
    parser.add_argument('--output', metavar='output', type=str,
                        help='File name for output CSV. (Optional)', default=None)
    args = parser.parse_args()
    write_csv(args.domain, args.course_id, args.token, args.output)


