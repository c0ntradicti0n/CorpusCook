import os
import random
from glob import iglob
from pathlib import Path

from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner


def get_files_from_path(path):
    paths = list(iglob(path, recursive=True))
    random.shuffle(paths)
    for f in paths:
        if os.path.isfile(f):
            yield str(Path(f).resolve())

class WebPageParser:
    def __init__(self, path_to_htmls=None):
        self.html_paths = get_files_from_path(path_to_htmls + WebPageParser.recursive_html_indexes_path)
        next(self.html_paths)

    recursive_html_indexes_path = '**/*.html'

    def html_path_to_html_page(self, path):
        with open(path, 'r+') as f:
            return f.read()

    def html_to_text(self, html):
        soup = BeautifulSoup(html, features="lxml")
        post = soup.find('div', class_='post')
        clear_html = self.sanitize_html(str(post))
        clear_soup = BeautifulSoup(clear_html, features="lxml")
        text_with_correct_beginning = clear_soup.text

        correct_end = text_with_correct_beginning.find("About Latest Posts")
        if correct_end == -1:
            return None
        text = text_with_correct_beginning[:correct_end]
        text = self.clean_text(text)
        return text

    def sanitize_html(self, dirty_html):
        ''' clean superfluous tags '''
        cleaner = Cleaner(
            page_structure=True,
            meta=True,
            embedded=True,
            links=True,
            style=True,
            processing_instructions=True,
            inline_style=True,
            scripts=True,
            javascript=True,
            comments=True,
            frames=True,
            forms=True,
            annoying_tags=True,
            remove_unknown_tags=True,
            safe_attrs_only=True,
            safe_attrs=frozenset(['src', 'color', 'href', 'title', 'class', 'name', 'id']),
            remove_tags=(
            'span', 'font', 'ul', 'li', 'ol', 'div', 'a', 'label', 'p', 'header', 'ins', 'time',
            'article', 'aside')
            )

        return cleaner.clean_html(dirty_html)

    def clean_text(self, text):
        text = text.replace('\n\n', '\n')
        return text


    def next_text(self):
        html_path = next(self.html_paths)
        html = self.html_path_to_html_page(html_path)
        text = self.html_to_text(html)

        if not text:
            return self.next_text()
        return text



import unittest

class TestHtmlParser(unittest.TestCase):
   def testPage(self):
       wpp = WebPageParser("../../")

       try:
           while True:
               text = wpp.next_text()
               self.assertIsInstance(text, str)
       except StopIteration:
           assert True
           return None
       assert False



if __name__ == '__main__':
    unittest.main()
