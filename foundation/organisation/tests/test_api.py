from unittest import TestCase

from ..utils import get_activity


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
