from HTMLParser import DifferenceBetweenHtmlParser
from config import input_dir, process_dir, output_dir, input_html_file_filter


class Sampler:
    def __init__(self, sample_file):
        self.sample_file = sample_file
        self.htmler = DifferenceBetweenHtmlParser(input_dir, process_dir, output_dir, input_html_file_filter)

    def add_to_library(self, text):
        with open(self.sample_file, 'a+') as f:
            f.write(text)
            f.write('\n')

    def complicated_sample(self, text):
        with open("./server_complicated.txt", 'a+') as f:
            f.writelines([text])

    def next_page(self):
        yield from self.htmler.process_generator()

