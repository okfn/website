from unittest import TestCase

from ..utils import get_activity, extract_ograph_title


class HelpersTest(TestCase):
    def test_get_activity_extracts_type(self):
        text = '#reading http://goodreads.com/123'
        self.assertEqual(get_activity(text), 'reading')

        text2 = '#watching http://goodreads.com/123'
        self.assertEqual(get_activity(text2), 'watching')

        text3 = '#eating http://goodreads.com/123'
        self.assertEqual(get_activity(text3), 'eating')

        text4 = '#working http://goodreads.com/123'
        self.assertEqual(get_activity(text4), 'working')

    def test_get_activity_returns_none_when_no_match(self):
        text = '#foobaring http://goodreads.com/123'
        self.assertEqual(get_activity(text), None)

    def test_extract_ograph_title(self):
        link = 'http://www.goodreads.com/book/show/486625.Close_to_the_Machine'
        text = '#reading {}'.format(link)
        url, title = extract_ograph_title(text)
        self.assertEqual(url, link)
        self.assertEqual(title, 'Close to the Machine')

    def test_extract_ograph_title_without_url(self):
        text = '#working Making the world more open'
        url, title = extract_ograph_title(text)
        self.assertIsNone(url)
        self.assertEqual(title, 'Making the world more open')
