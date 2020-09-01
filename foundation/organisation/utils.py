import re
from opengraph import opengraph

from django.http import JsonResponse

from foundation.organisation.models import NowDoing


def extract_ograph_title(text):
    text_without_hashtag = ' '.join(text.split(' ')[1:])
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]' \
                  + r'|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text_without_hashtag)
    if urls:
        content = opengraph.OpenGraph(url=urls[0])
        title = content.get('title', text_without_hashtag)
        return urls[0], title
    return None, text_without_hashtag


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
