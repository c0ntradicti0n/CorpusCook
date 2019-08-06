import coloredlogs
coloredlogs.install()
import logging
logging.getLogger().setLevel(logging.INFO)
from grammer_text_fit.token_parsing import matching_function, matching_functions
import unittest


def subordinate_clause(x):
    return len(list(x['tokens'][0]['spacy'].head.subtree))-1


def match_from (hay, vocab, key='lemma_'):
    for phrase in vocab:
        i = 0
        # spacy sometimes does not lower the lemma !?!
        while i < len(phrase) and  i < len(hay) and phrase[i] == hay[i][key].lower():
            i += 1
        if i == len(phrase):
            return len(phrase)
    return False


def test_rule (text, match_dict, rule):

    logging.info("testing 'rule_%s'" % rule)
    import pprint

    from grammer_text_fit.token_parsing import prepare_text, prepare_labels
    from grammer_text_fit.probsyntgreed_parsing import probsyntgreed_parser

    tokens = prepare_text(text)
    match_dict = prepare_labels([match_dict])

    parser = probsyntgreed_parser(tokens)
    solution = parser.match(match_dict=match_dict, rule=rule)

    if rule == 'differential_sentence':
        solution = parser.best_of(solution[0])

    logging.info(text)
    logging.info(pprint.pformat(solution, indent=4))

    return solution

@matching_function(['while', 'whereas'])
def while_(tokens):
    '''
    >>> match_dict = \
            ({'subject': ['Ask'], 'contrast': ['sellers'], 'aspect': ['users']}, \
             {'subject': ['Bid'], 'contrast': ['buyers'], 'aspect': ['users']})

    >>> text = 'whereas'
    >>> rule = 'while'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'while', 'tokens': ['whereas'], 'conf': 1}]

    'while'-subortdinate clause
    ===========================
    >>> text = 'while bids are made by buyers'
    >>> rule = 'in_while_S_A_C'
    >>> test_rule (text, match_dict, rule)
    [([], {'difference': [[{'start': 0, 'stop': 5, 'conf': 0.52, 'side': 0, 'what': 'subject', 'tokens': ['bids', 'are', 'made', 'by', 'buyers']}, {'start': 0, 'stop': 1, 'conf': 1.0, 'side': 1, 'what': 'subject', 'tokens': ['bids']}], [{'start': 4, 'stop': 5, 'conf': 0.8, 'side': 0, 'what': 'contrast', 'tokens': ['buyers']}, {'start': 4, 'stop': 5, 'conf': 1.0, 'side': 1, 'what': 'contrast', 'tokens': ['buyers']}], [{'start': 1, 'stop': 5, 'conf': 0.43, 'side': 0, 'what': 'aspect', 'tokens': ['are', 'made', 'by', 'buyers']}, {'start': 1, 'stop': 5, 'conf': 0.43, 'side': 1, 'what': 'aspect', 'tokens': ['are', 'made', 'by', 'buyers']}]], 'expansion': [{'marker': 'while', 'tokens': ['while'], 'conf': 1}]})]

    'while' inside a sentence
    =========================

    >>> text = "Asks or offers are done by sellers while bids are made by buyers"
    >>> rule = 'differential_sentence'
    >>> test_rule (text, match_dict, rule)
    (0, 0, 0, ({'start': 0, 'stop': 2, 'conf': 0.74, 'side': 0, 'what': 'subject', 'tokens': ['Asks', 'or']}, {'start': 6, 'stop': 7, 'conf': 1.0, 'side': 0, 'what': 'contrast', 'tokens': ['sellers']}, {'start': 1, 'stop': 7, 'conf': 0.48, 'side': 0, 'what': 'aspect', 'tokens': ['or', 'offers', 'are', 'done', 'by', 'sellers']}), [(1, ({'start': 0, 'stop': 1, 'conf': 1.0, 'side': 1, 'what': 'subject', 'tokens': ['bids']}, {'start': 4, 'stop': 5, 'conf': 1.0, 'side': 1, 'what': 'contrast', 'tokens': ['buyers']}, {'start': 1, 'stop': 5, 'conf': 0.43, 'side': 1, 'what': 'aspect', 'tokens': ['are', 'made', 'by', 'buyers']}))], [{'marker': 'while', 'tokens': ['while'], 'conf': 1}])

    '''
    return match_from(tokens, while_.vocab)

@matching_function([])
def as_(tokens):
    '''
    >>> text = 'as'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'as'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'as', 'tokens': ['as'], 'conf': 1}]
    '''
    return match_from(tokens, as_.vocab)

@matching_function(['than', 'compared to', 'compared with'])
def than_(tokens):
    '''
    >>> text = 'than'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'than'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'than', 'tokens': ['than'], 'conf': 1}]
    '''
    return match_from(tokens, than_.vocab)

"""
@matching_function(['more'])
def more_(tokens):
    '''
    >>> text = 'more'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'more'
    >>> test_rule (text, match_dict, rule)
    [['more']]
    '''
    return match_from(tokens, more_.vocab)
"""

@matching_function(["unlike", "except", "in contrast to", 'compared to'])
def except_(tokens):
    '''
    >>> text = 'compared to'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'except'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'except', 'tokens': ['compared', 'to'], 'conf': 1}]
    '''
    return match_from(tokens, except_.vocab)

@matching_function(['on the other hand', 'on the other side', 'On the other hand'])
def other_hand_(tokens):
    '''
    >>> text = 'on the other hand'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'other_hand'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'on_the_other_hand', 'tokens': ['on', 'the', 'other', 'hand'], 'conf': 1}]

    Sentence
    ========

    >>> text = 'On the other hand, a graduated cylinder is laboratory ' \
               'equipment used to measure the volume of liquids'
    >>> match_dict = \
                          ({'aspect': 'definition', \
                            'contrast': 'is a cylindrical container with a ' \
                                        'small pouring lip that is used for ' \
                                        'transporting and mixing solutions', \
                            'subject': 'Beaker'}, \
                           {'aspect': 'definition', \
                            'contrast': 'is laboratory equipment used to ' \
                                        'measure the volume of liquids', \
                            'subject': 'Graduated Cylinder'})
    >>> rule = 'differential_sentence'
    >>> from pprint import pprint
    >>> pprint (test_rule (text, match_dict, rule))
    (0,
     0,
     0,
     ({'conf': 0.36,
       'side': 0,
       'start': 13,
       'stop': 14,
       'tokens': ['liquids'],
       'what': 'subject'},
      {'conf': 0.88,
       'side': 0,
       'start': 0,
       'stop': 14,
       'tokens': [',',
                  'a',
                  'graduated',
                  'cylinder',
                  'is',
                  'laboratory',
                  'equipment',
                  'used',
                  'to',
                  'measure',
                  'the',
                  'volume',
                  'of',
                  'liquids'],
       'what': 'contrast'},
      {'conf': 0.45,
       'side': 0,
       'start': 4,
       'stop': 13,
       'tokens': ['is',
                  'laboratory',
                  'equipment',
                  'used',
                  'to',
                  'measure',
                  'the',
                  'volume',
                  'of'],
       'what': 'aspect'}),
     [(None, None)],
     [{'conf': 1,
       'marker': 'on_the_other_hand',
       'tokens': ['On', 'the', 'other', 'hand']}])


    Sentence Junction
    =================

    >>> text = 'A beaker is a cylindrical container with a small pouring ' \
               'lip that is used for transporting and mixing solutions. ' \
               'On the other hand, a graduated cylinder is laboratory ' \
               'equipment used to measure the volume of liquids.'
    >>> rule = 'text'

    >>> from pprint import pprint
    >>> pprint (test_rule (text, match_dict, rule))
    [{'d0': {'s0': {'aspect': {'annotations': ['lip', 'that', 'that', 'is'],
                               'conf': 0.43},
                    'contrast': {'annotations': ['is',
                                                 'a',
                                                 'cylindrical',
                                                 'container',
                                                 'with',
                                                 'a',
                                                 'small',
                                                 'pouring',
                                                 'lip',
                                                 'that',
                                                 'that',
                                                 'is',
                                                 'used',
                                                 'for',
                                                 'transporting',
                                                 'and'],
                                 'conf': 1.0},
                    'subject': {'annotations': ['beaker'], 'conf': 1.0}},
             's1': {'aspect': {'annotations': ['is',
                                               'laboratory',
                                               'equipment',
                                               'used',
                                               'to',
                                               'measure',
                                               'the',
                                               'volume',
                                               'of'],
                               'conf': 0.45},
                    'contrast': {'annotations': ['is',
                                                 'laboratory',
                                                 'equipment',
                                                 'used',
                                                 'to',
                                                 'measure',
                                                 'the',
                                                 'volume',
                                                 'of',
                                                 'liquids'],
                                 'conf': 1.0},
                    'subject': {'annotations': ['graduated', 'cylinder'],
                                'conf': 1.0}}},
      'markers': [{'conf': 1,
                   'marker': 'on_the_other_hand',
                   'tokens': ['On', 'the', 'other', 'hand']}]}]
    '''
    return match_from(tokens, other_hand_.vocab)

@matching_function(['the same'])
def the_same_(tokens):
    '''

    >>> text = 'the same'
    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'the_same'
    >>> test_rule (text, match_dict, rule)
    [{'marker': 'the_same', 'tokens': ['the', 'same'], 'conf': 1}]
    '''
    return match_from(tokens, the_same_.vocab)


def not_anything_special(tokens):
    ''' Checking, that it is not one of the defined markers

    >>> match_dict = [({'subject': 'something'})]
    >>> rule = 'unmarked_token'

    >>> text = 'except'
    >>> test_rule(text, match_dict, rule)    # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ometa.runtime.EOFError:

    >>> text = 'blub'
    >>> test_rule(text, match_dict, rule)
    [['blub']]

    >>> text = 'blub blob . '
    >>> rule = 'pseudo_sentence'
    >>> test_rule(text, match_dict, rule)
    [(['blub', 'blob'], ['.'])]

    :param tokens:
    :return:
    '''

    for i in range(len(tokens)):
        first_starts = [f(tokens[i:]) for f in matching_functions]
        if any(first_starts):
            if i == 0:
                return False
            return i
    return True

@matching_function(['.', ':', '...'])
def punct_(tokens):
    return match_from(tokens, punct_.vocab)



class TestGrammar(unittest.TestCase):
    def test_subject (self):
        text = 'something'
        match_dict = [({'subject': 'something'})]
        rule = 'subject'
        self.assertTrue(test_rule (text, match_dict, rule))

    def test_except(self):
        text = 'except something'
        match_dict = [({'subject': 'something'})]
        rule = 'except_S'
        self.assertTrue(test_rule(text, match_dict, rule))

    def test_while(self):
        text = "Asks or offers are done by sellers while bids are made by buyers . "
        match_dict  = \
            ({'subject': ['Ask'], 'contrast': ['sellers'], 'aspect': ['users']},
             {'subject': ['Bid'], 'contrast': ['buyers'], 'aspect': ['users']})
        rule = 'text'
        self.assertTrue(test_rule(text, match_dict, rule=rule))


    def test_the_same_A_as_S(self):
        text = "the same medications as cardiomyopathy"
        match_dict  =  (
            {
                'subject': ['Cardiomyopathy'],
                'contrast': ['medication', 'not', 'usually', 'diuretics', 'or', 'nitrates', ',', 'and', 'sometimes',
                             'an', 'implantable', 'cardioverter-', 'defibrillator'],
                'aspect': ['medication']
            }, {
                'subject': ['Heart', 'Failure'],
                'contrast': ['medication', 'including', 'diuretics', 'and', 'nitrates', ',', 'heart', 'transplant',
                             'and', 'implantable', 'cardioverter-', 'defibrillator'],
                'aspect': ['treatment']
            }
        )
        rule = 'the_same_A_as_S'
        logging.info(test_rule(text, match_dict, rule=rule))

        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_comparison_than(self):
        text = "Mary is taller than the bed is long"
        rule = 'differential_sentence'
        match_dict  =  (
            {
                'subject':  ['Mary'],
                'contrast': ['four', 'inches', 'tall'],
                'aspect':   ['height']
            }, {
                'subject':  ['bed'],
                'contrast': ['three', 'inches', 'long'],
                'aspect':   ['length']
            }
        )
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_comparison_more_than(self):
        text = "We bought more milk than wine"
        rule = 'differential_sentence'
        match_dict = (
            {
                'subject': ['milk'],
                'contrast': ['more'],
                'aspect': ['mass', 'volume']
            }, {
                'subject': ['wine'],
                'contrast': ['less'],
                'aspect': ['mass', 'volume']
            }
        )
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_compared_to(self):
        text = "The bed is 1 inch smaller compared to Mary"
        rule = 'differential_sentence'
        match_dict = (
            {
                'subject': ['Mary'],
                'contrast': ['four', 'inches', 'tall'],
                'aspect': ['height']
            }, {
                'subject': ['bed'],
                'contrast': ['three', 'inches', 'long'],
                'aspect': ['length']
            }
        )
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_the_same_as_S_but_also_C(self):
        text = "Heart failure can be treated with the same medications as cardiomyopathy but also nitrates and diuretics, " \
               "and sometimes a cardioverter-defibrillator or a transplanted heart may be necessary for survival "
        match_dict = (
            {
                'subject': ['Cardiomyopathy'],
                'contrast': ['medication', 'not', 'usually', 'diuretics', 'or', 'nitrates', ',', 'and', 'sometimes',
                             'an', 'implantable', 'cardioverter-', 'defibrillator'],
                'aspect': ['treatment']
            }, {
                'subject': ['Heart', 'Failure'],
                'contrast': ['medication', 'including', 'diuretics', 'and', 'nitrates', ',', 'heart', 'transplant',
                             'and', 'implantable', 'cardioverter-', 'defibrillator'],
                'aspect': ['treatment']
            }
        )
        rule = 'differential_sentence'
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_cardiomyopathy_risk(self):
        #text = 'Cardiomyopathy risk factors include having a family history of the condition and having a viral ' \
        """infection. Heart failure risk factors include a history of heart problems, including cardiomyopathy, ' \
        'having a family history of cardiac issues and having diabetes."""
        text = 'Cardiomyopathy risk factors include having a family history of the condition and having a viral ' \
                'infection'
        match_dict = \
            ({'subject': ['Cardiomyopathy'],
              'contrast': ['family', 'history', ',', 'certain', 'viruses', 'or', 'parasites'],
              'aspect': ['risk', 'factors']},
             {'subject': ['Heart', 'Failure'],
              'contrast': ['family', 'history', ',', 'certain', 'heart', 'conditions',
                           ',', 'hypertension', 'and', 'diabetes'],
              'aspect': ['risk', 'factors']})
        rule = 'text'
        rule = 'differential_sentence'

        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_coref(self):
        text = "This is not always the case with a negative skin test"
        rule = 'differential_sentence'
        match_dict = \
            ({'subject': 'positive tb skin test',
               'contrast': 'always present',
               'aspect': 'raised area'},
              {'subject': 'negative tb skin test',
               'contrast': 'rarely present',
               'aspect': 'raised area'})
        gold = "(0, 0, 0, ({'start': 8, 'stop': 11, 'conf': 0.89, 'side': 0, 'what': 'subject', " \
               "'tokens': ['negative', 'skin', 'test']}, " \
               "{'start': 1, 'stop': 5, 'conf': 2.61, 'side': 0, 'what': 'contrast', " \
               "'tokens': ['is', 'not', 'always', 'the']}, " \
               "{'start': 1, 'stop': 10, 'conf': 0.40599999999999997, 'side': 0, 'what': 'aspect', " \
               "'tokens': ['is', 'not', 'always', 'the', 'case', 'with', 'a', 'negative', 'skin']}), [], [])"
        self.assertEqual(str(gold), str(test_rule(text, match_dict, rule=rule)))

    def test_multiple_sentences (self):
        text = "A positive TB skin test is when the Mantoux tuberculin skin test indicates that a person has the " \
               "bacteria or has been exposed to M. tuberculosis. A negative TB skin test indicates that a person " \
               "has not been exposed to M. tuberculosis."
        match_dict = \
            ({'subject': 'positive tb skin test',
               'contrast': 'this is when the mantoux tuberculin skin test shows that a person has my tuberculosis bacteria '
                           'present or has been exposed to these bacteria',
               'aspect': 'definition'},
              {'subject': 'negative tb skin test',
               'contrast': 'this is when the mantoux tuberculin skin test shows that a person does not have my tuberculosis '
                           'bacteria present or has not been exposed to these bacteria',
               'aspect': 'definition'})

        rule = 'text'
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_cardiomyopathy_symptoms(self):
        text = "Heart failure can cause symptoms such as swollen ankles , fatigue , trouble breathing , lower cardiac " \
               "output , palpitations and a feeling of faintness , which is not limited to exercise"
        match_dict = \
            ({'subject':    ['Cardiomyopathy'],
              'contrast':   ['short', 'of', 'breath', ',', 'chest', 'pain', ',', 'fainting', 'during', 'exercise', ',',
                             'palpitations', ',', 'arrhythmias', ',', 'difficulty', 'breathing', 'at', 'night', '.'],
              'aspect':     ['symptoms']},
             {'subject':    ['Heart', 'Failure'],
              'contrast':   ['in', 'right', 'ventricular', 'failure', ':', 'ankles', 'and',
                             'abdomen', 'swell', '.', 'in', 'left', 'ventricular', 'failure',
                             'patients', 'have', 'a', 'decreased', 'cardiac', 'output', 'and',
                             'trouble', 'breathing', '.', 'symptoms', 'are', 'not', 'limited',
                             'to', 'exercise', 'or', 'at', 'night', '.'],
               'aspect':    ['symptoms']})
        rule = 'differential_sentence'
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_cardiomyopathy_causes(self):
        text = "There are many causes of heart failure including having had a myocardial infarction, having " \
               "hypertension, heart valve problems, cardiomyopathy, coronary artery disease and diabetes "
        match_dict = \
            ({'subject': ['Cardiomyopathy'],
              'contrast': ['most', 'often', 'genetic', ',', 'or', 'else', 'from', 'a', 'viral', 'infection', 'or', 't',
                           ',', 'cruzi'],
              'aspect': ['causes']},
             {'subject': ['Heart', 'Failure'],
              'contrast': ['cardiomyopathy', ',', 'coronary', 'artery', 'problems', ',', 'heart', 'attack', ',',
                           'hypertension', ',', 'valve', 'conditions'],
              'aspect': ['causes']})
        rule = 'differential_sentence'
        self.assertTrue(test_rule(text, match_dict, rule=rule))

    def test_other_hand_sentence(self):
        text = 'On the other hand, a graduated cylinder is laboratory ' \
                    'equipment used to measure the volume of liquids '
        match_dict = \
            ({'aspect': 'definition', \
              'contrast': 'is a cylindrical container with a ' \
                          'small pouring lip that is used for ' \
                          'transporting and mixing solutions', \
              'subject': 'Beaker'}, \
             {'aspect': 'definition', \
              'contrast': 'is laboratory equipment used to ' \
                          'measure the volume of liquids', \
              'subject': 'Graduated Cylinder'})
        rule = 'differential_sentence'
        print(test_rule(text, match_dict, rule))

    def test_other_hand_text (self):
        match_dict = \
            ({'aspect': 'definition', \
              'contrast': 'is a cylindrical container with a ' \
                          'small pouring lip that is used for ' \
                          'transporting and mixing solutions', \
              'subject': 'Beaker'}, \
             {'aspect': 'definition', \
              'contrast': 'is laboratory equipment used to ' \
                          'measure the volume of liquids', \
              'subject': 'Graduated Cylinder'})
        text = 'A beaker is a cylindrical container with a small pouring ' \
               'lip that is used for transporting and mixing solutions. ' \
               'On the other hand, a graduated cylinder is laboratory ' \
               'equipment used to measure the volume of liquids.'
        rule = 'text'

        from pprint import pprint
        pprint(test_rule(text, match_dict, rule))
        self.assertTrue(test_rule(text, match_dict, rule=rule))



if __name__ == '__main__':
    unittest.main()

