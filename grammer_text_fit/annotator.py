import coloredlogs
from ometa.runtime import ParseError

from grammer_text_fit.grammartester import GrammarTests

coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--multiprocessing', nargs='?', default=False, const=True)

args = parser.parse_args()
print(args.multiprocessing)

import pickle
import multiprocessing

from helpers import os_tools
from helpers.time_tools import timeit_context

from grammer_text_fit.config import *
from grammer_text_fit.probsyntgreed_parsing import probsyntgreed_parser
from grammer_text_fit.token_parsing import prepare_text, prepare_labels

from grammer_text_fit.alexandria_wrapper import *


alexandria = alexandria_api()


dump_files = '**/*.dump'

grammartester = GrammarTests()


class AnnotateDistinctions:
    """ Process parsed html_file to produce a annotated text_tokenized
    """
    def __init__(self):
        self.GreedySearchParser = probsyntgreed_parser()

    def prepare_text_and_match_dict(self, distinction_patterns:list=None, text:str=None):
        ''' Creates structured data from a text and a list of dicts, that will matched on the text

        :param distinction_patterns: list of dicts of labels of the strings to be matched
        :param text: string with the text to
        :return: None
        :raises: ValueError
        '''

        self.text = text
        self.distinction_patterns = distinction_patterns
        self.path = str(hash(text))
        self.text_tokenized = prepare_text(self.text)
        self.distinction_patterns_tokenized = prepare_labels(self.distinction_patterns)

        if not self.text_tokenized and self.distinction_patterns_tokenized:
            raise ValueError('There must be a text and some patterns!')

    def load(self, path):
        ''' Load pickled data from a path, it reveals a dict with a 'difference_text' key plus text,
            and dictinction patterns, that should be annotated.

        :param path: path as string to the location of a pickle dump file

        '''
        self.path = path
        with open(path, 'rb') as f:
            try:
                logging.info("loading '%s'" % path)
                html_information = pickle.load(f)
                text = html_information['difference_text']
                distinction_patterns = html_information['distinction_patterns']
                self.prepare_text_and_match_dict(distinction_patterns=distinction_patterns, text=text)
            except EOFError:
                logging.error('pickle file cant be loaded.')
                return None


    def process (self, rule='text', commit_to_alexandria=False):
        """Tokenizing, parsing and annotation of the text at main level"""
        logging.info(str(self.text))

        self.all_annotated = self.GreedySearchParser.match(self.text_tokenized, self.distinction_patterns_tokenized, rule=rule)

        self.annotated_texts = self.GreedySearchParser.annotate_conll03_single(
            tokens_to_annotate=self.all_annotated,
            grammar_tester=grammartester,
            text=self.text)
        grammartester.writedown()
        logging.info(str(self.annotated_texts))

        if commit_to_alexandria:
            self.annotated_texts = self.GreedySearchParser.annotate_tagml(self.all_annotated)
            self.annotated_tagml_texts = tagml_writer.wrap_with_tagml_tags(keys=['TAGML'], content=self.annotated_texts)

            tagml_path = 'tagml/' + os_tools.get_filename_from_path(self.path) + '.tagml'
            dot_path   = 'tagml/' + os_tools.get_filename_from_path(self.path) + '.tagml.dot'
            with open(tagml_path, 'w') as f:
                f.write(self.annotated_texts)
                alexandria.add(tagml_path)
                alexandria.commit(tagml_path)
                alexandria.commit(args='-a')
                alexandria.export(format='dot', where=dot_path, what=alexandria.checkout_name_from_path(tagml_path))

                try:
                    with open(dot_path, 'r') as f:
                            dot = f.readlines()
                    dot.insert(1,"rankdir=LR;\n")
                    with open(dot_path, 'w') as f:
                        f.writelines(dot)
                    os.system("dot -Tsvg '{dotpath}' > '{svgpath}'".format(dotpath=dot_path, svgpath=dot_path+'.svg'))
                except FileNotFoundError:
                    logging.error('no dot file generated because of TAGML grammar error')

        return self.annotated_texts


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
numberOfThreads = 4


def process_all():

    def process(annotator, out_conll_path, path):
        annotator.load(path=path)
        try:
            with timeit_context('Parsing') as t:
                annotated_text = annotator.process()
            with open(out_conll_path, 'a') as f:
                f.write(annotated_text)
                f.write('\n')
                f.write('\n')
        except ParseError:
            logging.error('Parse Error for file %s' % path)

    out_conll_path = output_dir+'conll03.txt'
    with open(out_conll_path, 'w+') as f:
        f.write('-DOCSTART- -X- -X- O\n\n')
    annotator = AnnotateDistinctions()

    if args.multiprocessing:

        processes = []
        for path in list(os_tools.get_files_from_recursive_path(process_dir + dump_files)):
            p = multiprocessing.Process(target=process, args=(annotator, out_conll_path, path))
            processes.append(p)
            p.start()

    else:
        for path in list(os_tools.get_files_from_recursive_path(process_dir + dump_files)):
            process(annotator, out_conll_path, path)
            #except:
            #    logging.error(sys.exc_info()[0])


if __name__ == '__main__':
    process_all()
