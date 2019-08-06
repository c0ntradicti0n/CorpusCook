import pprint
from grammer_text_fit.tok import tok_list_to_string

import signal
import sys
def signal_handler(sig, frame):
        print('You pressed Ctrl+C! Wait for debugging statistics!')
        GrammarTests.writedebugstatistics()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

from collections import Counter


class GrammarTests:
    def __init__(self, path='./grammartests.py'):
        GrammarTests.comments = []
        GrammarTests.path = path
        with open(GrammarTests.path, 'w') as f:
            f.write(self.body)

        self.tests = []

    body  = """
# Automatically generated unittests for grammar

import unittest
import coloredlogs
coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)        

def test_rule (text, match_dict, rule):

    logging.info("testing 'rule_%s'" % rule)
    import pprint

    from token_parsing import prepare_text, prepare_labels
    from probsyntgreed_parsing import probsyntgreed_parser

    tokens = prepare_text(text)
    match_dict = prepare_labels([match_dict])

    parser = probsyntgreed_parser()
    solution = parser.match(tokens=tokens, match_dict=match_dict, rule=rule)

    if rule == 'differential_sentence':
        solution = parser.best_of(solution[0])

    logging.info("\\n" + text)
    logging.info("\\n" + pprint.pformat(solution, indent=4))

    return solution
    
class TestGrammar(unittest.TestCase):
"""

    def add_sample(self, text, match_dict, rule='text', number=0):
        test = []
        test_name = "".join([
                             "".join(tok_list_to_string(match_dict[0]['subject'])),
                             "".join(tok_list_to_string(match_dict[1]['subject'])),
                             str(number)
                            ]
                           )
        test_header = "".join(["\tdef test", test_name, "(self):"])
        test.append("".join(['text = """', text,'"""']))
        test.append("".join(['match_dict = ', pprint.pformat(match_dict, indent=4)]))
        test.append("".join(['rule = "', rule, '"']))
        test.append("self.assertTrue(test_rule (text, match_dict, rule))")
        self.tests.append(test_header + "\n\t\t".join(["\t\t", *test, '\n']))

    def add_comment(self, comment=""):
        # TODO inserting '#' where there are long lines
        GrammarTests.comments.append(comment)
        comment = "".join(['\n\t', '# ', comment])
        self.tests[-1] = "\n".join([comment, self.tests[-1]])

    def writedown(self):
        pyfile = "\n".join([*self.tests])
        with open(GrammarTests.path, 'a', 1) as f:
            f.write(pyfile)

    def writedebugstatistics():
        counter = Counter(GrammarTests.comments)
        stats = ["%3d %s" % comment_freq[::-1] for comment_freq in counter.most_common()]
        statistics = "\n\t# " + "\n\t# ".join(stats)
        with open(GrammarTests.path, 'a', 1) as f:
            f.write(statistics)



