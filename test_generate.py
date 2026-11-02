"""Exercise the feed generator as a script, without network requests."""
import json
import os
import pathlib
import runpy
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

SCRIPT = pathlib.Path(__file__).with_name('generate.py')
PREVIOUS = {'urls': ['https://example.com/previous/']}


def response(status, body):
    result = Mock(spec=requests.Response)
    result.status_code = status
    result.json.return_value = body
    if status >= 400:
        result.raise_for_status.side_effect = requests.HTTPError(str(status))
    return result


class FeedGenerationTests(unittest.TestCase):
    def generate(self, responses, failure=False):
        with tempfile.TemporaryDirectory() as directory:
            before = pathlib.Path.cwd()
            os.chdir(directory)
            try:
                feed = pathlib.Path('posts.json')
                feed.write_text(json.dumps(PREVIOUS), encoding='utf-8')
                with patch('requests.get', side_effect=responses):
                    if failure:
                        with self.assertRaises(requests.HTTPError):
                            runpy.run_path(str(SCRIPT), run_name='__main__')
                    else:
                        runpy.run_path(str(SCRIPT), run_name='__main__')
                return json.loads(feed.read_text(encoding='utf-8'))
            finally:
                os.chdir(before)

    def test_first_page_bad_request_preserves_previous_feed(self):
        self.assertEqual(self.generate([response(400, {'code': 'rest_invalid_param'})], True), PREVIOUS)

    def test_first_page_invalid_page_is_an_error(self):
        self.assertEqual(self.generate([response(400, {'code': 'rest_post_invalid_page_number'})], True), PREVIOUS)

    def test_later_unexpected_bad_request_preserves_previous_feed(self):
        pages = [response(200, [{'link': 'https://example.com/new/'}]), response(400, {'code': 'rest_invalid_param'})]
        self.assertEqual(self.generate(pages, True), PREVIOUS)

    def test_server_error_with_empty_body_preserves_previous_feed(self):
        self.assertEqual(self.generate([response(503, [])], True), PREVIOUS)

    def test_wordpress_end_of_pagination_keeps_all_urls(self):
        pages = [response(200, [{'link': 'https://example.com/one/'}]), response(200, [{'link': 'https://example.com/two/'}]), response(400, {'code': 'rest_post_invalid_page_number'})]
        self.assertEqual(self.generate(pages), {'urls': ['https://example.com/one/', 'https://example.com/two/']})

    def test_successful_empty_page_ends_pagination(self):
        pages = [response(200, [{'link': 'https://example.com/one/'}]), response(200, [])]
        self.assertEqual(self.generate(pages), {'urls': ['https://example.com/one/']})


if __name__ == '__main__':
    unittest.main()
