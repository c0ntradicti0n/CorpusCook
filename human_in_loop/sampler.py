from HTMLParser import DifferenceBetweenHtmlParser
from config import input_dir, process_dir, output_dir, input_html_file_filter


class Sampler:
    def __init__(self, sample_file):
        self.sample_file = sample_file
        self.htmler = DifferenceBetweenHtmlParser(input_dir, process_dir, output_dir, input_html_file_filter)
        self.read_library_f = self.start_reading_library()


    def add_to_library(self, text):
        with open(self.sample_file, 'a') as f:
            f.write(text)
            f.write('\n')

    def start_reading_library(self):
        with open(self.sample_file, 'r') as f:
            content = f.read()
            text = str(content).split(sep='\n')
            for line in text:
                print ('sample:', line)
                yield line

    def deliver_sample(self):
        return next(self.read_library_f)

    def complicated_sample(self, text):
        with open("./server_complicated.txt", 'a+') as f:
            f.writelines([text])

    def next_page(self):
        yield from self.htmler.process_generator()

