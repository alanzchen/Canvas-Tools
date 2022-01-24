#!/usr/bin/env python3
from canvasapi import Canvas

def write_csv(domain, course_id, token, filename=None):
    canvas = Canvas('https://' + domain, token)
    course = canvas.get_course(course_id)
    paginated_groups = course.get_groups()
    grps = list(paginated_groups)
    cnt = 0
    if not filename:
        filename = '{}.csv'.format(course_id)
    with open(filename, 'w') as f:
        f.write('Pre-assign Room Name,Email Address\n')
        for grp in grps:
            ppl = list(grp.get_users())
            for j in ppl:
                f.write(grp.name + ',' + j.login_id + '\n')
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


