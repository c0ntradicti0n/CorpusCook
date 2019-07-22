import pickle
import random

from nltk import flatten

from config import output_dir, process_dir, dump_files
from helpers import os_tools
from helpers.time_tools import timeit_context
import logging

from tok import Tok
from token_parsing import prepare_text, prepare_labels

logging.getLogger().setLevel(logging.INFO)

# TODO
# while in front
# , while
# however
#

class CorpusCook:
    def __init__(self):
        sentence_connectors = ['.', 'while', '. while', ', while', 'however', 'whereas', '. Whereas ', 'in cntrast', '. In contrast to this', 'compared to', 'in comparison to', '. On the other hand']
        self.sentence_connectors = [prepare_text(t) for t in sentence_connectors]
        self.stop_tokens = sentence_connectors
        self.dot = prepare_text('.')

    def it_is_randomly_the_case(self):
        return random.choice([True, False])

    def build_annotation(self, pattern):
        solution = []
        conector = random.choice(self.sentence_connectors)

        if self.it_is_randomly_the_case(): # put noise between
            connector = prepare_text('.') + self.noise_text([]) + [conector]

        if self.it_is_randomly_the_case(): # side 1 before side 2
            solution.append(self.build_pattern_for_side(pattern[0]))
            solution.append(conector)
            solution.append(self.build_pattern_for_side(pattern[1]))
        else:                              # side 2 before side 1
            solution.append(self.build_pattern_for_side(pattern[0]))
            solution.append(conector)
            solution.append(self.build_pattern_for_side(pattern[1]))

        solution.append(self.dot)
        return solution

    def noise_text(self, pattern):
        solution = []
        for _ in range(20):
            position1 = random.randint(0, len(self.text_tokenized))
            length = random.randint(1, 30)
            solution = self.text_tokenized[position1:position1+length]
            if any(t in solution for t in pattern):
                continue
            if any(t['text'] == '.' for t in solution):
                continue
            break
        return solution

    def build_pattern_for_side(self, pattern):
        ''' Construct randomly a sentence for a side

        :param pattern:
        :return:
        '''
        solution = []
        if self.it_is_randomly_the_case():  # between?
            if self.it_is_randomly_the_case(): # before/after?
                solution.append(pattern['contrast'])
                solution.append(pattern['subject'])
            else: # put subject before
                solution.append(pattern['subject'])
                solution.append(pattern['contrast'])
        else:
            position = random.randint(0, len(pattern['contrast']))
            between = pattern['contrast'][:]
            between.insert(position, pattern['subject'])
            solution.append(between)

        if self.it_is_randomly_the_case():  # before
            solution = self.noise_text(solution) + solution
        if self.it_is_randomly_the_case():  # after
            solution = solution + self.noise_text(solution)


        #if self.it_is_randomly_the_case(): # put aspect somewhere
        #    position = random.randint(0, len(flatten(solution)))
        #    solution.insert(position, pattern['aspect'])
        return solution

    def load(self, path:str):
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


    def relabel_annotations(self, side=None, extra_label=None):
        diffd = side
        old_diffd_items = list(diffd.items())
        # copying, because iteration over modified dict won't work

        for key, annotation in old_diffd_items:
            new_key = key + extra_label
            diffd[new_key] = diffd[key]
            del diffd[key]
        return diffd

    def say_annotate_to_tokens(self, tokens):
        Tok.conll03_layer_repr.dependenceA = False
        Tok.conll03_layer_repr.dependenceB = False
        conll_line = "\n".join([t.conll03_layer_repr() for t in tokens if t] + ['\n'])
        return conll_line

    def process(self, rule='text', commit_to_alexandria=False):
        """Tokenizing, randomly building and annotating based on the tables and pictures"""
        logging.info(str(self.text))

        annotations = [flatten(self.build_annotation(pattern))
                    for pattern in self.distinction_patterns_tokenized]

        for difference_set in self.distinction_patterns_tokenized:
            self.relabel_annotations(side=difference_set[0], extra_label='_A')
            self.relabel_annotations(side=difference_set[1], extra_label='_B')
            for side in difference_set:
                for kind, tokens in side.items():
                    if tokens:
                        for tok in tokens:
                            if isinstance(tok, list):
                                x=1
                            tok.update_token(start_end=True, keys=[kind])

        annotation_texts = [self.say_annotate_to_tokens(tokens) for tokens in annotations]
        annotations = "\n\n".join(annotation_texts)
        logging.info(annotations)
        return annotations


def process_all(root_path='../'):

    def process(cook, out_conll_path, path):
        cook.load(path=path)

        with timeit_context('Parsing') as t:
            annotated_text = cook.process()
        with open(out_conll_path, 'a') as f:
            f.write(annotated_text)
            f.write('\n')
            f.write('\n')

    out_conll_path = output_dir + 'conll03.txt'
    with open(out_conll_path, 'w+') as f:
        f.write('-DOCSTART- -X- -X- O\n\n')
    cook = CorpusCook()

    for path in list(os_tools.get_files_from_recursive_path(root_path + process_dir + dump_files)):
        process(cook, out_conll_path, path)


if __name__ == '__main__':
    process_all()