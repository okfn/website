import re

from django.http import JsonResponse

from foundation.organisation.models import NowDoing


def get_activity(text):
    options = '|'.join([a[0] for a in NowDoing.ACTIVITIES])
    pattern = '^#({}).*'.format(options)
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    return None


def fail_json(message, status_code=400):
    response = JsonResponse({'success': False,
                             'message': message})
    response.status_code = status_code
    return response
